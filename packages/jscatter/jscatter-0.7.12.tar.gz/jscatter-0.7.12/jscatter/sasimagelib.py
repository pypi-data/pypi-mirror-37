# -*- coding: utf-8 -*-
# written by Ralf Biehl at the Forschungszentrum Jülich ,
# Jülich Center for Neutron Science 1 and Institute of Complex Systems 1
#    Jscatter is a program to read, analyse and plot data
#    Copyright (C) 2015  Ralf Biehl
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Read 2D image files (TIFF) from SAXS cameras and extract the corresponding data.

The sasImage is a 2D array that allows direct subtraction and multiplication (e.g. transmission)
respecting given masks in operations. E.g. ::

 sample=js.sas.sasImage('sample.tiff')
 solvent=js.sas.sasImage('solvent.tiff')
 corrected = sample/sampletransmission - solvent/solventtransmission

Calibration of detector distance, radial average, size reduction and more.
.showPolar allows sensitive detection of the beamcenter.

An example is shown in :py:class:`~.sasimagelib.sasImage` .


------

"""

import os
import glob
import copy
import numpy as np
import numpy.ma as ma
import scipy
import scipy.linalg as la
from scipy import ndimage
import PIL
import PIL.ImageOps
import PIL.ExifTags
import PIL.ImageSequence
from xml.etree import ElementTree

from . import formel
from .dataarray import dataArray as dA
from .dataarray import dataList as dL
from . import mpl

try:
  basestring
except NameError:
  basestring = str

# normalized gaussian function
_gauss=lambda x,A,mean,sigma,bgr:A*np.exp(-0.5*(x-mean)**2/sigma**2)/sigma/np.sqrt(2*np.pi) + bgr

def shortprint(values,threshold=6,edgeitems=2):
    """
    Creates a short handy representation string for array values.

    Parameters
    ----------
    values : object
        Values to print.
    threshold: int default 6
        Number of elements to switch to reduced form.
    edgeitems : int default 2
        Items at the edge.

    """
    opt = np.get_printoptions()
    np.set_printoptions(threshold=threshold,edgeitems=edgeitems)
    valuestr=np.array_str(values)
    np.set_printoptions(**opt)
    return valuestr

def _w2f(word):
    """
    Converts strings if possible to float.
    """
    try:
        return float(word)
    except ValueError:
        return word

def parseXML(text):
    root = ElementTree.fromstring(text)
    r=etree_to_dict(root)
    return r

def etree_to_dict(root):
    #d = {root.tag : map(etree_to_dict, root.getchildren())}
    d={ child.attrib['name']:child.text for child in root.iter() if child.text is not None}
    return d

def phase(phases):
    """Transform to [-pi,pi] range."""
    return ( phases + np.pi) % (2 * np.pi ) - np.pi

# calc peak positions of AgBe
#q=np.r_[0.5:10:0.0001]
#iq=js.sas.AgBeReference(q,data.wavelength[0]/10,n=np.r_[1:15])
#iq.iX[scipy.signal.argrelmax(iq.iY,order=3)[0]]

#: AgBe peak positions
AgBepeaks=[ 1.0753, 2.1521, 3.2286, 4.3049, 5.3813, 6.4576, 7.5339, 8.6102, 9.6865, 10.7628]

#: Create AgBe peak positions profile
def _agbpeak(q, center=0, fwhm=1, lg=1, asym=0, amplitude=1, bgr=0):
    peak=formel.voigt(x=q, center=center, fwhm=fwhm,lg=lg,asym=asym, amplitude=amplitude)
    peak.Y+=bgr
    return peak

# While reading the image file, data are extracted from XML string or text in the EXIF data of the image.
# The following describe what to extract in an line/entry and how to replace:
# 1 name to look for
# 2 the new attribute name (to have later unique names from different detectors)
# 3 a dictionary of char to replace in the line before looking for the keyword/content
# 4 factor to convert to specific units
# 5 return value 'list' or 'string', default list with possible conversion to float
# Not extracted information is in .artist or .imageDescription
exchangekeywords = []
exchangekeywords.append(['Wavelength', 'wavelength', None,1,None])
exchangekeywords.append(['Flux', 'flux', None,1,None])
exchangekeywords.append(['det_exposure_time','exposure_time', None,1,None])
exchangekeywords.append(['det_pixel_size','pixel_size', None,1,None])
exchangekeywords.append(['beamcenter_actual','beamcenter',None,1,None])
exchangekeywords.append(['detector_dist','detector_distance',None,0.001,None]) # conversion to m
exchangekeywords.append(['Meas.Description','description',None,1,'string'])    # return a string
exchangekeywords.append(['wavelength', 'wavelength', None,1,None])
exchangekeywords.append(['Exposure_time' ,   'exposure_time', None,1,None])
exchangekeywords.append(['Pixel_size',    'pixel_size', {'m':'','x ':''},1,None])
exchangekeywords.append(['Detector_distance','detector_distance',None,1,None])


class SubArray(np.ndarray):
    # Defines a generic np.ndarray subclass, that stores some metadata
    # in attributes
    # It seems to be the default way for subclassing maskedArrays
    #  to have the array_finalize from this subclass.

    def __new__(cls,arr):
        x = np.asanyarray(arr).view(cls)
        x.comment=[]
        return x

    def __array_finalize__(self, obj):
        if callable(getattr(super(SubArray, self),'__array_finalize__', None)):
            super(SubArray, self).__array_finalize__(obj)
        if hasattr(obj,'attr'):
            for attribut in obj.attr:
                self.__dict__[attribut]=getattr(obj,attribut)
        try:
            # copy tags from reading
            self._tags=getattr(obj,'_tags')
        except:pass
        return

    @property
    def array(self):
        return self.view(np.ndarray)

    def setattr(self,objekt,prepend='',keyadd='_'):
        """
        Set (copy) attributes from objekt.

        Parameters
        ----------
        objekt : objekt with attr or dictionary
            Can be a dictionary of names:value pairs like {'name':[1,2,3,7,9]}
            If object has property attr the returned attribut names are copied.
        prepend : string, default ''
            Prepend this string to all attribute names.
        keyadd : char, default='_'
            If reserved attributes (T, mean, ..) are found the name is 'T'+keyadd

        """
        if hasattr(objekt,'attr'):
            for attribut in objekt.attr:
                try:
                    setattr(self,prepend+attribut,getattr(objekt,attribut))
                except AttributeError:
                    self.comment.append('mapped '+attribut+' to '+attribut+keyadd)
                    setattr(self,prepend+attribut+keyadd,getattr(objekt,attribut))
        elif type(objekt)==type({}):
            for key in objekt:
                try:
                    setattr(self,prepend+key,objekt[key])
                except AttributeError:
                    self.comment.append('mapped '+key+' to '+key+keyadd)
                    setattr(self,prepend+key+keyadd,objekt[key])

    @property
    def attr(self):
        """
        Show specific attribute names as sorted list of attribute names.

        """
        if hasattr(self,'__dict__'):
            return sorted([key for key in self.__dict__ if key[0]!='_'])
        else:
            return []

    def showattr(self,maxlength=None,exclude=['comment']):
        """
        Show specific attributes with values as overview.

        Parameters
        ----------
        maxlength : int
            Truncate string representation after maxlength char.
        exclude : list of str
            List of attribute names to exclude from result.

        """
        for attr in self.attr:
            if attr not in exclude:
                values=getattr(self,attr)
                try:
                    valstr=shortprint(values.split('\n'))
                    print(  '{:>24} = {:}'.format(attr, valstr[0]))
                    for vstr in valstr[1:]:
                        print(  '{:>25}  {:}'.format('', vstr))
                except:
                    print(  '%24s = %s' %(attr,str(values)[:maxlength]))


subarray = SubArray

class sasImage(SubArray,np.ma.MaskedArray):

    def __new__(cls, file,detector_distance=None):
        """
        Creates sasImage as maskedArray from a detector image for evaluation.

        Reads a .tif file including the information in the EXIF tag.
         - All methods of maskedArrays including masking of invalid areas work.
         - Masked areas are automatically masked for all math operations.
         - Arithmetic operations for sasImages work as for numpy arrays
           e.g. to subtract background image or multiplying with transmission.

        Parameters
        ----------
        file : string
            Filename to open.
        detector_distance : float, sasImage
            Detector distance from calibration measurement or calibrated image.
            Overwrites value in the image EXIF tag.

        Returns
        -------
            image : sasImage with attributes
             - .beamcenter : beam center
             - .iX : X pixel position
             - .iY : Y pixel position
             - .filename
             - .artist : Additional attributes from EXIF Tag Artist
             - .imageDescription : Additional attributes from EXIF Tag ImageDescription

        Notes
        -----

        - Unmasked data can be accessed as .data
        - The mask is .mask and initial set to all negative values.
        - Masking of a pixel is done as image[i,j]=np.ma.masked.
          Use mask methods as implemented.
        - TIFF tags with index above 700 are ignored.

        - Tested for reading tiff image files from Pilatus detectors as given from our
          metal jet SAXS machines Ganesha and Galaxi at JCNS, Jülich.
        - Additional SAXSpace TIFF files are supported which show frames per pixel on the Y axis.
          THis allows to examine the time evolution of the measurement on these line collimation cameras
          (Kratky camera).
          Instead of the old PIL the newer fork Pillow is needed for the multi page TIFFs.
          Additional the pixel_size is set to 0.024 (µm) as for the JCNS CCD camera.



        Examples
        --------
        ::

         import jscatter as js
         #
         # Look at calibration measurement
         calibration = js.sas.sasImage(js.examples.datapath+'/calibration.tiff')
         # Check beamcenter
         # For correct beamcenter it should show straight lines (change beamcenter to see change)
         calibration.showPolar(beamcenter=[122,254],scaleR=3)
         # Recalibrate with previous found beamcenter (calibration sets it already)
         calibration.recalibrateDetDistance(showfits=True)
         iqcal=calibration.radialAverage()
         # This might be used to calibrate detector distance for following measurements as
         # empty.setDetectorDistance(calibration)
         #
         empty = js.sas.sasImage(js.examples.datapath+'/emptycell.tiff')
         # Mask beamstop (not the same as calibration, unluckily)
         empty.mask4Polygon([92,185],[92,190],[0,233],[0,228])
         empty.maskCircle(empty.beamcenter, 9)
         empty.show()
         buffer = js.sas.sasImage(js.examples.datapath+'/buffer.tiff')
         buffer.maskFromImage(empty)
         buffer.show()
         bsa = js.sas.sasImage(js.examples.datapath+'/BSA11mg.tiff')
         bsa.maskFromImage(empty)
         bsa.show() # by default a log scaled image
         #
         # subtract buffer (transmission factor is just a guess here, sorry)
         new=bsa-buffer*0.2
         new.show()
         #
         iqempty=empty.radialAverage()
         iqbuffer=buffer.radialAverage()
         iqbsa=bsa.radialAverage()
         #
         p=js.grace(1,1)
         p.plot(iqempty,le='empty cell')
         p.plot(iqbuffer,le='buffer')
         p.plot(iqbsa,le='bsa 11 mg/ml')
         p.title('raw data, no transmission correction')
         p.yaxis(min=1,max=1e3,scale='l',label='I(q) / a.u.')
         p.xaxis(scale='l',label='q / nm\S-1')
         p.legend()

        References
        ----------
        .. [1] Everything SAXS: small-angle scattering pattern collection and correction
               Brian Richard Pauw J. Phys.: Condens. Matter 25,  383201 (2013)
               DOI https://doi.org/10.1088/0953-8984/25/38/383201

        """
        # open file
        if isinstance(file,str):
            # read tiff image
            image=PIL.Image.open(file)
        else:
            # try if this was an opened image
            image=file
        try:
            # try im we have multiple frames as for SAXSpace
            # seek(1) returns error for single frame
            image.seek(1)
            image.seek(0)
            if hasattr(PIL,'__version__'):
                # squeeze for single columns
                im=np.asarray([np.asarray(image) for _ii in PIL.ImageSequence.Iterator(image)]).squeeze()
            else:
                raise ImportWarning('Current version of PIL does not support multi frame images. Install Pillow>=5.2.0 ')

        except EOFError:
            # tif to array conversion for single frame
            im  = np.asarray(image)
        # set it to writable
        im.flags.writeable=True
        # create the maskedArray from the base class as view
        # create default mask from negative values
        # Pilatus detectors have negative values outside sensitive detector area.
        sub_im = SubArray(im)
        data = np.ma.MaskedArray.__new__(cls, data=sub_im, mask=sub_im<0)

        # default values
        data.imageDescription=[]
        data.artist=[]
        # the EXIF tags contain all meta information.
        # Take them as dictionary and add to artist, imageDescription or respective name from PIL.ExifTags.TAGS.
        try:
            data._tags=image.tag_v2
        except AttributeError:
            try:
                data._tags=image.tag
            except AttributeError:
                print('To tags with image information found.')
        data._getEXIF()

        # set attributes from exif and extract some of these data
        data.filename=file
        data.description='---'
        # keywords to replace
        data._extractAttributes_(exchangekeywords)

        if hasattr(data,'beamcenter'):
            data.beamcenter=[data.beamcenter[1],data.beamcenter[0]]
        if detector_distance is not None:
            data.setDetectorDistance(detector_distance)
        data._issasImage=True
        return data

    def _extractAttributes_(self,attriblist):
        # extract attributes from EXIF entries
        # first words in comments
        firstwords=[line.split()[0]  for line in self.imageDescription+self.artist if len(line.strip()) >0]
        for attribs in attriblist:
            if attribs[0] in firstwords:
                self.getfromcomment(attribs[0],replace=attribs[2],newname=attribs[1])
                if attribs[4]=='string':
                    setattr(self, attribs[1],' '.join([str(v) for v in getattr(self, attribs[1])]))
                else:
                    setattr(self,attribs[1],[v*attribs[3] if isinstance(v,(float,int)) else v for v in  getattr(self,attribs[1])])

    def _getEXIF(self):
        # extract EXIF data and save them in artist and imageDescription
        for k,v in dict(self._tags).items():
            if k > 700:
                continue
            elif k==270:
                # TAGS[270] = 'ImageDescription'
                # from Galaxy or Ganesha
                self.setattr({'imageDescription':[ vv[1:].strip() if vv[0]=='#' else vv.strip() for vv in v.splitlines()]})
            elif k==315:
                # TAGS[315] =  'Artist'
                # in XML tag from Ganesha. Throws error if not a XML tag as for Galaxy
                try:
                    self.entriesXML=parseXML(self._tags[315])
                    self.setattr({'artist':[str(k)+' '+str(v) for k,v in self.entriesXML.items()]})
                except ElementTree.ParseError:
                    if isinstance(self._tags[315],basestring):
                        # catch if it is a single string as for SAXSPACE
                        self.setattr({'artist':[self._tags[315]]})
                    else:
                        self.setattr({'artist':[]})
            else:
                if k in PIL.ExifTags.TAGS:
                    self.setattr({PIL.ExifTags.TAGS[k]: v if isinstance(v, (list, set)) else [v]})
        if self.artist[0] == 'Anton Paar GmbH':
            # catches SAXSPACE TIFF files
            # iv are specific for SAXSPACE
            for k,iv in dict({'wavelength':65024,'detector_distance':65060}).items():
                v=self._tags[iv]
                self.setattr({k: v if isinstance(v, (list, set)) else [v]})
            self.pixelSize=0.024 # 24 µm
        return

    def _setEXIF(self):
        # set Exif entries according to attributes if these were changed
        # see PIL.TiffTags.TYPES for types
        # we add anything new to TAGS[270]
        for k,v in dict(self._tags).items():
            if k > 700:
                continue
            elif k==270:
                # TAGS[270] = 'ImageDescription'
                content=['processed by Jscatter']
                content+= self.imageDescription
                for ekw in exchangekeywords:
                    if ekw[1] == 'beamcenter':
                        # beamstop as y,x
                        bs=getattr(self, ekw[1])
                        content.append(ekw[0] + ' ' + str(bs[1]) + ' ' + str(bs[0]) )
                    else:
                        try:
                            content.append(ekw[0]+' '+' '.join([str(a) for a in getattr(self,ekw[1])]))
                        except:pass
                self._tags[k]='\n'.join(content)
            elif k==315:
                # TAGS[315] = 'Artist'
                self._tags[k]='\n'.join(self.artist)
            else:
                if k in PIL.ExifTags.TAGS:
                    content=getattr(self,PIL.ExifTags.TAGS[k])[0]
                    type=self._tags.tagtype[k]
                    if type==2:
                        self._tags[k] = ' '.join(content)
                    elif type in [3,4,8,9]:
                        self._tags[k] = content
                    else:
                        self._tags[k] = content
        return


    @property
    def iX(self):
        return np.repeat(np.r_[0:self.shape[1]][None,:],self.shape[0],axis=0)

    @property
    def iY(self):
        return np.repeat(np.r_[0:self.shape[0]][:,None], self.shape[1], axis=1)

    @property

    def array(self):
        """
        Strip of all attributes and return a simple array without mask.
        """
        return self.data.array

    def getfromcomment(self, name, replace=None, newname=None):
        """
        Extract name from .artist or .imageDescription with attribute name in front.

        If multiple names start with parname first one is used.
        Used line is deleted from .artist or .imageDescription.

        Parameters
        ----------
        name : string
            Name of the parameter in first place.
        replace : dict
            Dictionary with pairs to replace in all lines.
        newname : string
            New attribute name

        """
        if newname is None:
            newname=name
        #first look in imageDescription
        for i,line in enumerate(self.imageDescription):
            if isinstance(replace, dict):
                for k,v in replace.items():
                    line=line.replace(k,str(v))
            words=line.split()
            if len(words)>0 and words[0]==name:
                setattr(self,newname,[_w2f(word) for word in words[1:]])
                del self.imageDescription[i]
                return
        # then in artist
        for i, line in enumerate(self.artist):
            if isinstance(replace, dict):
                for k, v in replace.items():
                    line = line.replace(k, str(v))
            words = line.split()
            if len(words) > 0 and words[0] == name:
                setattr(self, newname, [_w2f(word) for word in words[1:]])
                del self.artist[i]
                return

    def setDetectorDistance(self,detector_distance):
        """
        Set detector distance.

        Parameters
        ----------
        detector_distance : float, sasImage
            New value for detector distance.
            If sasImage the detector_distance is copied.


        """
        if isinstance(detector_distance,(float,int)):
            self.detector_distance=[detector_distance]
        elif isinstance(detector_distance,(list,set)):
            self.detector_distance=list(detector_distance)
        else:
            self.detector_distance = detector_distance.detector_distance

    def maskFromImage(self,image):
        """
        Use/copy mask from image.

        Parameters
        ----------
        image : sasImage
            sasImage to use mask for resetting mask.
            image needs to have same dimension.

        """
        if image.shape==self.shape:
            self.mask=image.mask

    def maskRegion(self,xmin,xmax,ymin,ymax):
        """
        Mask rectangular region.

        Parameters
        ----------
        xmin,xmax,ymin,ymax : int
            Corners of the region to mask

        """
        self[xmin:xmax,ymin:ymax]=ma.masked

    def maskRegions(self,regions):
        """
        Mask several regions.

        Parameters
        ----------
        regions : list
            List of regions as in maskRegion.

        """
        for region in regions:
            self.maskRegion(*region)

    def maskbelowLine(self,p1,p2):
        """
        Mask points at one side of line.

        The masked side is left looking from p1 to p2.

        Parameters
        ----------
        p1, p2 : list of 2x float
            Points in pixel coordinates defining line.


        """
        points=np.stack([self.iX,self.iY])
        pp1=np.array(p1)
        pp2 = np.array(p2)
        d = np.cross((pp2-pp1)[:,None,None], pp1[:,None,None]-points,axis=0)
        self[d>0]=ma.masked

    def maskTriangle(self,p1,p2,p3,invert=False):
        """
        Mask inside triangle.

        Parameters
        ----------
        p1,p2,p3 : list of 2x float
            Edge points of triangle.
        invert : bool
            Invert region. Mask outside circle.

        """
        points=np.stack([self.iX,self.iY], axis=2)
        pp1 = np.array(p1)
        pp2 = np.array(p2)
        pp3 = np.array(p3)
        # cross to get sides of lines
        d1 = np.sign(np.cross((pp2 - pp1)[ None, None,:], points - pp1[ None, None,:], axis=2).reshape(points.shape[0],-1))
        d2 = np.sign(np.cross((pp3 - pp2)[ None, None,:], points - pp2[ None, None,:], axis=2).reshape(points.shape[0],-1))
        d3 = np.sign(np.cross((pp1 - pp3)[ None, None,:], points - pp3[ None, None,:], axis=2).reshape(points.shape[0],-1))
        # equal side if sign equal sign of 3rd point
        mask=((d1 == d1[p3[1], p3[0]]) & (d2 == d2[p1[1], p1[0]]) & (d3 == d3[p2[1], p2[0]]))
        if invert:
            self[~mask]=ma.masked
        else:
            self[mask] = ma.masked

    def mask4Polygon(self,p1,p2,p3,p4, invert=False):
        """
        Mask inside polygon of 4 points.

        Points need to be given in right hand order.

        Parameters
        ----------
        p1,p2,p3,p4 : list of 2x float
            Edge points.
        invert : bool
            Invert region. Mask outside circle.

        """
        points=np.stack([self.iX,self.iY], axis=2)
        pp1 = np.array(p1,dtype=np.int32)
        pp2 = np.array(p2,dtype=np.int32)
        pp3 = np.array(p3,dtype=np.int32)
        pp4 = np.array(p4,dtype=np.int32)
        # cross to get sides of lines
        d1 = np.sign(np.cross((pp2 - pp1)[ None, None,:], points - pp1[ None, None,:], axis=2).reshape(points.shape[0],-1))
        d2 = np.sign(np.cross((pp3 - pp2)[ None, None,:], points - pp2[ None, None,:], axis=2).reshape(points.shape[0],-1))
        d3 = np.sign(np.cross((pp4 - pp3)[ None, None,:], points - pp3[ None, None,:], axis=2).reshape(points.shape[0],-1))
        d4 = np.sign(np.cross((pp1 - pp4)[None, None, :], points - pp4[None, None, :], axis=2).reshape(points.shape[0], -1))
        # equal side if sign equal sign of 3rd point
        mask=((d1 == d1[pp3[1], pp3[0]]) & (d2 == d2[pp4[1], pp4[0]]) & (d3 == d3[pp1[1], pp1[0]]) & (d4 == d3[pp2[1], pp2[0]]) )
        if invert:
            self[~mask]=ma.masked
        else:
            self[mask] = ma.masked

    def maskCircle(self,center,radius,invert=False):
        """
        Mask points inside circle.

        Parameters
        ----------
        center : list of 2x float
            Center point.
        radius : float
            Radius in pixel units
        invert : bool
            Invert region. Mask outside circle.


        """
        points=np.stack([self.iX,self.iY])
        distance=la.norm(points-np.array(center)[:, None, None],axis=0)
        mask=distance<radius
        if invert:
            self[~mask]=ma.masked
        else:
            self[mask] = ma.masked

    def findCenterOfIntensity(self,beamcenter=None,size=None):
        """
        Find beam center as center of intensity.

        Only values above the mean value are used.

        Parameters
        ----------
        beamcenter : 2x int
            First estimate of beamcenter.
            If not given preliminary beamcenter is estimated as center of intensity of full image.
        size : int
            Defines size of rectangular region of interest (ROI) around the beamcenter to look at.

        Returns
        -------
            Adds (replaces) .beamcenter as attribute.

        Notes
        -----
        If ROI is to large the result may be biased due to asymmetry of
        the intensity distribution inside of ROI.

        """
        if isinstance(size,float):
            size=np.rint(size).astype(np.int)
        if beamcenter is None:
            # as first guess
            beamcenter = ndimage.measurements.center_of_mass( ma.masked_less(self, self.mean(), copy=True) )
        if size is not None:
            # take smaller portion to reduce bias from image size
            bc=np.rint(beamcenter).astype(np.int)
            data=self[bc[0]-size:bc[0]+size,bc[1]-size:bc[1]+size]
            # mask values smaller than mean and take centerofmass
            center = ndimage.measurements.center_of_mass( ma.masked_less(data, data.mean(), copy=True) )
            beamcenter=[center[0]+bc[0]-size,center[1]+bc[1]-size]
        self.beamcenter= beamcenter

    def _findCenterAgBe(self,beamcenter=None,size=40):
        """
        Currently not working!!

        Find beamcenter as center of Debye-Scherrer rings of AgBe powder.

        Parameters
        ----------
        beamcenter : 2x int
            Estimate of center.
            If not given findCenterOfIntensity is used to estimate center.
        size : int
            Rectangular region around the beamcenter to look at.

        Returns
        -------
            Adds .beamcenter as attribute.

        """
        if beamcenter is None:
            if not hasattr(self,'beamcenter'):
                self.findCenterOfIntensity(size=size)
                print('Found new beamcenter at ',self.beamcenter)
            else:
                print('Use beamcenter at ', self.beamcenter)
            beamcenter=self.beamcenter
        # get original mask
        orgmask=self.mask
        X=self.iX-beamcenter[0]
        Y=self.iY-beamcenter[1]
        mean=self.mean()

        # calc approximate radial wavevectors in real coordinates
        xxyy=((X*self.pixel_size[0])**2+(Y*self.pixel_size[1])**2)**0.5
        phi=np.arctan2(X,Y)
        # scattering angle
        angle=np.arctan(xxyy/self.detector_distance[0])
        wl=self.wavelength[0]/10.        # conversion to nm
        q=4*np.pi/wl*np.sin(angle/2)
        dq=0.3  # around peak positions

        nn=20
        dphi=np.pi/nn
        bc=[]
        # AgBepeaks contains a list of AgBe peak positions to test for
        print(beamcenter)
        for agp in AgBepeaks:
            qmask=(q>agp-dq) & (q<agp+dq)
            centers = []
            print('-----------------------------------')
            for i,a1 in enumerate(np.r_[0:nn]*dphi):
                # symmetric side is -pi
                a2=a1-np.pi
                # make masks
                pi1 = qmask & ((phi > a1 ) & (phi < (a1 + dphi))) & ~orgmask
                pi2 = qmask & ((phi > a2 ) & (phi < (a2 + dphi))) & ~orgmask
                # only proceed if sizes of both sides are equal (no mask involved)
                # print('#1 ',a1,pi1.sum(),a2,pi2.sum() )
                if pi1.sum() == pi2.sum() and pi1.sum()>10:

                    # only above mean
                    pi1max = pi1 & (self>mean)
                    # X and Y mean
                    Xpi1mean = np.mean(X[pi1max].astype(np.float64))# * self[pi1max]) / self[pi1max].sum()
                    Ypi1mean = np.mean(Y[pi1max].astype(np.float64))# * self[pi1max]) / self[pi1max].sum()
                    # same for other side
                    pi2max = pi2 & (self > mean)
                    Xpi2mean = np.mean(X[pi2max].astype(np.float64))# * self[pi2max]) / self[pi2max].sum()
                    Ypi2mean = np.mean(Y[pi2max].astype(np.float64))# * self[pi2max]) / self[pi2max].sum()
                    centers.append([(Xpi1mean+Xpi2mean)/2,(Ypi1mean+Ypi2mean)/2,abs(Xpi1mean-Xpi2mean),abs(Ypi1mean-Ypi2mean)])
                    print('pi1 ',["%0.2f" % i for i in [pi1.sum(),Xpi1mean,Ypi1mean,Xpi2mean,Ypi2mean]])
            if len(centers)>nn*0.7:

                centers=np.array(centers).T
                # use only better 45 degree
                choose=(centers[2]/(centers[2] ** 2 + centers[3] ** 2) ** 0.5) >0.5**0.5
                bc = [np.mean(centers[0,~choose]),np.mean(centers[1,choose])]
                print(bc)
        # self.beamcenter= centers
        print(centers)
        # restore original mask
        self.mask=ma.nomask
        self[orgmask]=ma.masked

    def radialAverage(self, beamcenter=None, number=500):
        """
        Radial average of image and conversion to wavevector q.

        Remember to set .detector_distance to calibrated value.

        Parameters
        ----------
        beamcenter : list 2x float
            Sets beam center or radial center in data and uses this.
            If not given the attribut beamcenter in the data is used.
        number : int, default 500
            Number of intervals on new X scale.

        Returns
        -------
            dataArray

        Notes
        -----
        - Correction for flat detector projected to Ewald sphere included.

        """
        if beamcenter is not None:
            self.beamcenter=beamcenter
        X=(self.iX-self.beamcenter[0])*self.pixel_size[0]
        Y=(self.iY-self.beamcenter[1])*self.pixel_size[1]
        # calc radial wavevectors
        r=np.linalg.norm([X,Y],axis=0)
        angle=np.arctan(r/self.detector_distance[0])
        wl=self.wavelength[0]/10.        # conversion to nm
        self.q=4*np.pi/wl*np.sin(angle/2)
        # correction for flat detector with pixel area
        lpl0=1./np.cos(angle)
        data=self.data*lpl0**3

        mask=self.mask
        radial=dA(np.stack([self.q[~mask],data[~mask]]))
        radial.isort() # sorts along X by default
        # return lower number of points from prune
        result = radial.prune(number=number,kind='mean+') # makes averages with errors
        result.filename=self.filename
        result.detector_distance=self.detector_distance
        result.description=self.description
        return result

    def getPixelQ(self):
        """
        Get scattering vector along pixel dimension around beamcenter.

        Returns
        -------
            qx,qy with image x and y dimension


        """
        wl=self.wavelength[0]/10.        # conversion to nm
        dd=self.detector_distance[0]
        # pixel distances
        X=(np.r_[0:self.shape[1]]-self.beamcenter[0])*self.pixel_size[0]
        Y=(np.r_[0:self.shape[0]]-self.beamcenter[1])*self.pixel_size[1]

        # q from pixel
        qfp=lambda r: 4*np.pi/wl*np.sin(0.5 * np.arctan( r / dd ))

        return qfp(X),qfp(Y)

    def linearAverage(self, beamcenter=None, number=None,minmax='auto',show=False):
        """
        Linear average of image and conversion to wavevector q for line collimation cameras.

        Remember to set .detector_distance to calibrated value.

        Parameters
        ----------
        beamcenter : float
            Sets beam center in data and uses this.
            If not given the beam center is determined from semitransparent beam.
        number : int, default None
            Number of intervals on new X scale. None means all pixels.
        minmax : [int,int], 'auto'
            Interval for determination of beamcenter.
        show : bool
            Show the fit of the primary beam.

        Returns
        -------
            dataArray
             - .filename
             - .detector_distance
             - .description
             - .beamcenter

        Notes
        -----
        - Detector distance in attributes is used.
        - The primary beam is automatically detected.
        - Correction for flat detector projected to Ewald sphere included.

        """
        if beamcenter is None:
            # take average
            imageav=dA(np.c_[np.r_[0:self.shape[1]],self.mean(axis=0)].T)
            # find minima from argmax if not given explicitly
            if minmax[0]=='a': # auto
                # for normal empty cell or buffer measurement the primary beam is the maximum
                imax=imin=imageav.Y.argmax()
                while imageav.Y[imax+1]<imageav.Y[imax]:      imax+=1
                while imageav.Y[imin-1]<imageav.Y[imin]:      imin-=1
                xmax=imageav.X[imax]
                xmin=imageav.X[imin]
            else:
                xmin=minmax[0]
                xmax=minmax[1]
            # prune to smaller interval
            primarybeam=imageav.prune(lower=xmin,upper=xmax)
            # subtract min value , which is basically dark current
            primarybeam.Y-=primarybeam.Y.min()
            norm=   scipy.integrate.simps(primarybeam.Y, primarybeam.X)
            primarybeam.Y/=norm
            # fit mean position and width
            primarybeam.fit(_gauss,{'mean':imageav.Y.argmax(),'sigma':0.015,'bgr':0,'A':1},{},{'x':'X'})
            beamcenter=primarybeam.mean
            self.primarybeam_hwhm=primarybeam.sigma*np.sqrt(np.log(2.0))
            self.primarybeam_peakmax=primarybeam.modelValues(x=primarybeam.mean).Y[0]*norm
            if show:
                primarybeam.showlastErrPlot()
        self.beamcenter=beamcenter
        r=(self.iX[0]-self.beamcenter)*self.pixelSize # µm pixel size
        # calc radial wavevectors
        angle=np.arctan(r/self.detector_distance[0])
        wl=self.wavelength[0]
        self.q=4*np.pi/wl*np.sin(angle/2)
        # correction for flat detector with pixel area
        lpl0=1./np.cos(angle)
        data  = self.mean(axis=0) * lpl0   # because of line collimation only power 1
        error = self.std(axis=0) * lpl0  # because of line collimation only power 1
        result=dA(np.stack([self.q,data,error]))
        if number is not None:
            # return lower number of points from prune
            result = result.prune(number=number,kind='mean+') # makes averages with errors
        result.filename=self.filename
        result.detector_distance=self.detector_distance
        result.description=self.description
        return result

    def recalibrateDetDistance(self, beamcenter=None, number=500,showfits=False):
        """
        Recalibration of detectorDistance by AgBe reference for point collimation.

        Use only for AgBe reference measurements to determine the correction factor.
        For non AgBe measurements set during reading or .detector_distance to the new value.
        May not work if the detector distance is totally wrong.

        Parameters
        ----------
        beamcenter : list 2x float
            Sets beam center or radial center in data and uses this.
            If not given the attribut beamcenter in the data is used.
        number : int, default 1000
            number of intervals on new X scale.
        showfits : bool
            Show the AgBe peak fits.


        Notes
        -----
        - .distanceCorrection will contain factor for correction.
        Repeating this results in a .distanceCorrection close to 1.

        """
        # do radial average
        iq=self.radialAverage(beamcenter=beamcenter, number=number)
        # later distance corrections
        self.distanceCorrection=[]
        dq=0.3  # around peak positions
        for agp in AgBepeaks:
            # AgBepeaks contains a list of AgBe peak positions to test for
            # we fit each with a voigt function and take later the average
            if iq.X.max()>agp+dq and iq.X.min()<agp-dq:
                # cut between lower and upper and fit Voigt function for peak
                iqq=iq.prune(lower=agp-dq,upper=agp+dq)
                if iqq.shape[1]<5:
                    continue
                iqq.setLimit(amplitude=[0],bgr=[0],fwhm=[0.001,agp])
                iqq.fit(_agbpeak, {'center':agp, 'amplitude': iqq.Y.max() / 4., 'fwhm':0.1, 'asym':1, 'bgr': iqq.Y.min() / 2.},
                        {}, {'q':'X'}, output=False)
                if showfits :
                    iqq.showlastErrPlot()
                self.distanceCorrection+=[iqq.center/agp]
        corfactor=np.mean(self.distanceCorrection)
        corstd=np.std(self.distanceCorrection)/corfactor
        # set new detectorDistance
        self.detector_distance[0]*=corfactor
        print('\nCorrection factor %.4f to new distance %.4f (rel error : %.4f )' %(corfactor, self.detector_distance[0], corstd) )

    def show(self,scale=None,levels=8):
        """
        Show image.

        Parameters
        ----------
        scale : 'norm', default 'log',
            If log the image is first log scaled
        levels : int
            Number of countour levels.

        Returns
        -------
            image handle

        """
        if scale is None or scale[0]=='l':
            return mpl.contourImage(np.ma.log(self),levels=levels)
        else:
            return 

    def gaussianFilter(self,sigma=2):
        """
        Gaussian filter in place.

        Uses ndimage.filters.gaussian_filter with default parameters except sigma.

        Parameters
        ----------
        sigma : float
            Gaussian kernel sigma.

        """
        self[self.mask]=ndimage.filters.gaussian_filter(self.data,sigma)[self.mask]

    def reduceSize(self,size=2):
        """
        Reduce size of image using uniform average in box.

        XResolution,YResolution are scaled correspondingly.

        Parameters
        ----------
        size : int
            Pixel size of the box to average.
            Also factor for reduction.

        Returns
        -------
            sasImage

        """
        data=copy.deepcopy(self)
        data[data.mask]=ndimage.filters.uniform_filter(data.data,size=size)[data.mask]
        smalldata=data[::size,::size]
        try:
            # increase pixel size
            smalldata.pixel_size = [pz * size for pz in smalldata.pixel_size]
            smalldata.beamcenter = [bc / size for bc in smalldata.beamcenter]
        except:pass
        # set pixel coordinates
        smalldata._setXY()
        smalldata.ImageWidth=[smalldata.shape[1]]
        smalldata.ImageLength = [smalldata.shape[0]]
        smalldata.XResolution[0]=data.XResolution[0]*float(size)
        smalldata.YResolution[0]=data.YResolution[0]*float(size)
        smalldata._setEXIF()
        return smalldata

    def showPolar(self,beamcenter=None,scaleR=1):
        """
        Show image transformed to polar coordinates around beamcenter.

        Parameters
        ----------
        beamcenter : [int,int]
            Beamcenter
        scaleR : float
            Scaling factor for radial component to zoom the beamcenter.

        Returns
        -------
            Handle to figure

        """
        if beamcenter is not None:
            self.beamcenter=beamcenter

        # transform from polar coordinates to cartesian with bc shift and scaling of radial component to magnify
        def transform(rp,bc,shape,scale):
            phi=rp[0]/shape[0]*2*np.pi-np.pi
            r=rp[1]/scale
            return r * np.cos(phi) + bc[1] , r * np.sin(phi) + bc[0]
        newimage=np.zeros_like(self.data)
        ndimage.geometric_transform(self,mapping=transform,output=newimage,
                                    extra_keywords={'bc':self.beamcenter,'shape':self.shape,'scale':scaleR})

        f= mpl.contourImage(newimage)
        f.axes[0].set_ylabel('azimuth ')
        f.axes[0].set_xlabel('radial ')
        mpl.pyplot.show(block=False)

        return f

    def save(self,file,format=None,**params):
        """
        Saves image under the given filename.

        If no format is specified, the format to use is determined from the filename extension.
        See PIL save for formats and options.

        Parameters
        ----------
        file : string
            Filename to save to.
        format :
            Optional format override. If omitted, the format to use is determined from
            the filename extension. If a file object was used instead of a filename,
            this parameter should always be used.
        params : -
            Additional parameters.

        Returns
        -------

        """
        #create image
        image=PIL.Image.fromarray(self.data)
        # write image
        params.update({'tiffinfo':self._tags})
        image.save(fp=file,format=format,**params)


def readImages(filenames):
    """
    Read a list of images returning sasImage`s.

    Parameters
    ----------
    filenames : string
        Glob pattern to read

    Returns
    -------
        list of sasImage`s

    Notes
    -----
    To get a list of image descriptions::

     images=js.sas.readImages(path+'/latest*.tiff')
     [i.description for i in images]



    """
    try:
        filelist=glob.glob(filenames)
    except AttributeError:
        raise AttributeError('No filename pattern in ', filenames)
    else:
        data=[]
        for ff in filelist:
           data.append(sasImage(ff))
    return data

def createImageDescriptions(images):
    """
    Create text file with image descriptions as list of content.

    Parameters
    ----------
    images : list of sasImages or glob pattern
        List of images

    Returns
    -------


    """
    if not isinstance(images,(list,set)):
        images=readImages(filenames)
    commonprefix = os.path.commonprefix([i.filename for i in images])
    description=[i.filename[len(os.path.dirname(commonprefix))+1:]+'   '+i.description for i in images]
    description.sort()
    commonname=os.path.split(commonprefix)[-1]
    if commonname=='':
        commonname='--'
    with open('ContentOf_'+commonname+'.txt', 'w') as f:
        f.writelines("%s\n" % l for l in ['Content of dir '+os.path.dirname(commonprefix),' '])
        f.writelines("%s\n" % l for l in description)

def createLogPNG(filenames,center=None,size=None,colormap='jet',equalize=False,contrast=None):
    """
    Create .png files from grayscale images with log scale conversion to values between [1,255].

    This generates images viewable in simple image viewers as overview.
    The new files are stored in the same folder as the original files.

    Parameters
    ----------
    filenames : string
        Filename with glob pattern as 'file*.tif'
    center : [int,int]
        Center of crop region.
    size : int
        Size of crop region as around center as 2*size.
        If center is None the border is cut by size.
    colormap : string, None
        Colormap from matplotlib or None for grayscale.
        For standard colormap names look in mpl.showColors().
    equalize : bool
        Equalize the images.
    contrast : None, float
        Autocontrast for the image.
        The value (0.1=10%) determines how much percent are cut from the intensity histogram before linear
        spread of intensities.

    """
    if colormap is not None:
        cmap=mpl.pyplot.get_cmap(colormap)
    else:
         cmap=None
    i1=i3=0
    i2=i4=100000
    if size is not None:
        # set box around center or from border
        if center is not None :
            i1 = center[1] - size
            i2 = center[1] + size
            i3 = center[0] - size
            i4 = center[0] + size
        else:
            i1 =   size
            i2 = - size
            i3 =   size
            i4 = - size
    try:
        filelist=glob.glob(filenames)
    except AttributeError:
        raise AttributeError('No filename pattern in ', filenames)
    else:
        for ff in filelist:
            image=PIL.Image.open(ff)
            # crop image arary
            image2=np.array(image)[max(i1,0):min(i2,image.height),max(i3,0):min(i4,image.width)]
            # log scale mapped to 0-255
            image2[image2<1]=1
            image2 = np.log(image2)
            image2 = image2 / np.max(image2) * 255
            if cmap is None:
                newimage=PIL.Image.fromarray(image2.astype(np.uint8)).convert('L')
                if contrast is not None:
                    newimage=PIL.ImageOps.autocontrast(newimage,contrast)
                if equalize:
                    newimage=PIL.ImageOps.equalize(newimage)
                newimage.save(ff+'.png')
            else:
                # cmap needs uint to work properly
                image2=cmap(image2.astype(np.uint8),bytes=True)
                newimage=PIL.Image.fromarray(image2[:,:,:-1],mode='RGB')
                if contrast is not None:
                    newimage=PIL.ImageOps.autocontrast(newimage,contrast)
                if equalize:
                    newimage=PIL.ImageOps.equalize(newimage)
                newimage.save(ff + '.png')
    return


