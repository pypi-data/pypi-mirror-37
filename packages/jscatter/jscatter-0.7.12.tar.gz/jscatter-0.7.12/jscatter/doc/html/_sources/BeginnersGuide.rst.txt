Beginners Guide / Help
======================

.. autosummary::
    jscatter.showDoc


Some places to start :

- `Python-Numpy-Tutorial <http://cs231n.github.io/python-numpy-tutorial/>`_ A **crash course** with contents as :
 - Basic data types, Containers (Lists, Dictionaries, Sets, Tuples), Functions, Classes
 - Numpy, Arrays, indexing, Datatypes, Array math, Broadcasting
- `The Python Tutorial <https://docs.python.org/3/tutorial/>`_
- `Numpy Quickstart tutorial <https://docs.scipy.org/doc/numpy/user/quickstart.html>`_
- `Scipy : high-level scientific computing <https://www.scipy-lectures.org/intro/scipy.html>`_

**How to get help and command expansion**

In a shell as (I)python two simple things help the user.
 - The Python docstring of a function can be retrieved by *help(command)*
 - The 'TAB' can be used to expand a command or get the list of possilbe mehtods/attributes
::

 # try with some data from below
 help(i5.fit)
 i5.a    # write this and press *TAB* to get *append, aslist, attr*

Reading ASCII files
-------------------
- dataArray (js.dA) reads **one** dataset from a file.

- dataList  (js.dL) reads **all** datasets from one/multiple files (may differ in shape) ::

   # one dataarary
   data=js.dL('../data/latest_0001.dat',index=2)  # take the second dataset in the file
   # read multiple files
   data=js.dL('../data/latest_*.dat')             # reads all '.dat' files starting with 'latest'
   # same with glob (using name patterns as *,? )
   import glob
   data=js.dL()  # empty dataList
   for filename in glob.glob('../data/latest*.dat'):
      data.append(filename)                       # you may add options
   for dat in data:
      dat.Temp=float(data.filename.split('_')[2])  # extract attribute from filename


****

A common problem is how to read ASCII files with data as the format is often not
very intuitive designed. Often there is additional metadata before or after a matrix like block or in the filename.

Jscatter uses a simple concept to classify lines :
 * 2 numbers at the beginning of a line are data (matrix like data block).
 * a name followed by a number (and more) is an attribute with name and content.
 * everything else is comment (but can later be converted to an attribute).

Often it is just necessary to replace some characters to fit into this concept.
This can be done during reading using some simple options in dataArray/dataList creation:
 * replace={‘old’:’new’,’,’:’.’}     ==>  replace char and strings
 * skiplines=lambda words: any(w in words for w in [‘’,’ ‘,’NAN’,’‘*])  ==> skip complete bad lines
 * takeline='ATOM'   ==> select specific lines
 * ignore ='#'       ==> skip lines starting with this character
 * usecols =[1,2,5]  ==> select specific columns
 * lines2parameter=[2,3,4]  ==> use these data lines as comment and not as data.

See :py:func:`jscatter.dataarray.dataArray` for all options and how to use them.

If there is more information in comments or filename this can be extracted by using the comment lines.
 * data.getfromcomment('nameatfirstcolumn') ==> extract a list of words in this line
 * data.name  ==> filename, see below examples.

**How to extract information fromm comment lines** ::

 # lines as 'pressure 1013 14' are used automatically to set an attribute as .pressure
 # if data.name is a string as 'adh_Temp273_conc02.dat' extract Temp and conc like
 temp=data.name.split('_')
 data.Temp=float(temp[1][4:])
 data.conc=float(temp[2][4:6])
 #
 # if same line is in comment use
 temp=data.comment[0].split('_')
 # or use data.getfromComment(...)



**Some examples and how to read them**

filename: data1_273K_10mM.dat (e.g. Instrument JNSE@MLZ, Garching) ::

 this is just a comment or description of the data
 temp     293
 pressure 1013 14
 detectorsetting up
 name     temp1bsa
 0.854979E-01  0.178301E+03  0.383044E+02
 0.882382E-01  0.156139E+03  0.135279E+02
 0.909785E-01  0.150313E+03  0.110681E+02
 0.937188E-01  0.147430E+03  0.954762E+01
 0.964591E-01  0.141615E+03  0.846613E+01
 0.991995E-01  0.141024E+03  0.750891E+01
 0.101940E+00  0.135792E+03  0.685011E+01
 0.104680E+00  0.140996E+03  0.607993E+01

Read by ::

 data=js.dA('data1_273K_10mM.dat')
 data.getfromComment('detectorsetting')           # creates attribute detectorsetting with string value 'up' found in comments
 data.Temp=float(data.name.split('_')[1][:-1])    # extracts the temperature from filename
 data.conc=float(data.name.split('_')[2][:-2])    # same for concentration
 data.pressure[0]                                 # use pressure value 1013 # this was created automatically
 data.Temp                                        # use temperature value   # this was created explicit

aspirin.pdb: Atomic coordinates for aspirin (`AIN <http://ligand-expo.rcsb.org/reports/A/AIN/AIN_ideal.pdb>`_ from `Protein Data Bank, PDB <http://www.rcsb.org/ligand/AIN>`_ )::

 Header
 Remarks blabla
 Remarks in pdb files are sometimes more than 100 lines
 ATOM      1  O1  AIN A   1       1.731   0.062  -2.912  1.00 10.00           O
 ATOM      2  C7  AIN A   1       1.411   0.021  -1.604  1.00 10.00           C
 ATOM      3  O2  AIN A   1       2.289   0.006  -0.764  1.00 10.00           O
 ATOM      4  C3  AIN A   1      -0.003  -0.006  -1.191  1.00 10.00           C
 ATOM      5  C4  AIN A   1      -1.016   0.010  -2.153  1.00 10.00           C
 ATOM      6  C5  AIN A   1      -2.337  -0.015  -1.761  1.00 10.00           C
 ATOM      7  C6  AIN A   1      -2.666  -0.063  -0.416  1.00 10.00           C
 ATOM      8  C1  AIN A   1      -1.675  -0.085   0.544  1.00 10.00           C
 ATOM      9  C2  AIN A   1      -0.340  -0.060   0.168  1.00 10.00           C
 ATOM     10  O3  AIN A   1       0.634  -0.083   1.111  1.00 10.00           O
 ATOM     11  C8  AIN A   1       0.314   0.035   2.410  1.00 10.00           C
 ATOM     12  O4  AIN A   1      -0.824   0.277   2.732  1.00 10.00           O
 ATOM     13  C9  AIN A   1       1.376  -0.134   3.466  1.00 10.00           C
 ATOM     14  HO1 AIN A   1       2.659   0.080  -3.183  1.00 10.00           H
 ATOM     15  H4  AIN A   1      -0.765   0.047  -3.203  1.00 10.00           H
 ATOM     16  H5  AIN A   1      -3.119   0.001  -2.505  1.00 10.00           H
 ATOM     17  H6  AIN A   1      -3.704  -0.082  -0.117  1.00 10.00           H
 ATOM     18  H1  AIN A   1      -1.939  -0.123   1.591  1.00 10.00           H
 ATOM     19  H91 AIN A   1       0.931  -0.004   4.453  1.00 10.00           H
 ATOM     20  H92 AIN A   1       1.807  -1.133   3.391  1.00 10.00           H
 ATOM     21  H93 AIN A   1       2.158   0.610   3.318  1.00 10.00           H
 CONECT    1    2   14 may apear at the end
 HETATOM lines may apear at the end
 END

Read by (several methods): ::

 # 1.
 # take 'ATOM' lines, but only column 6-8 as x,y,z coordinates.
 js.dA('AIN_ideal.pdb',takeline='ATOM',replace={'ATOM':'0'},usecols=[6,7,8])
 # 2.
 # replace 'ATOM' string by number and set XYZ for convenience
 js.dA('AIN_ideal.pdb',replace={'ATOM':'0'},usecols=[6,7,8],XYeYeX=[0,1,None,None,2])
 # 3.
 # only the Oxygen atoms
 js.dA('AIN_ideal.pdb',takeline=lambda w:(w[0]=='ATOM') & (w[2][0]=='O'),replace={'ATOM':'0'},usecols=[6,7,8])
 # 4.
 # using regular expressions we can decode the atom specifier into a scattering length
 import re
 rHO=re.compile('HO\d') # 14 is HO1
 rH=re.compile('H\d+')  # represents somthing like 'H11' or 'H1' see regular expressions
 rC=re.compile('C\d+')
 rO=re.compile('O\d+')
 # replace atom specifier by number and use it as last column
 ain=js.dA('AIN_ideal.pdb',replace={'ATOM':'0',rC:1,rH:5,rO:2,rHO:5},usecols=[6,7,8,2],XYeYeX=[0,1,None,None,2])
 # 5.
 # read only atoms and use it to retrieve atom data from js.formel.ELements
 atoms=js.dA('AIN_ideal.pdb',replace={'ATOM':'0'},usecols=[2],XYeYeX=[0,1,None,None,2])[0].array
 al=[js.formel.Elements[a[0].lower()] for a in atoms]

data2.txt::

 # this is just a comment or description of the data
 # temp     ;    293
 # pressure ; 1013 14  bar
 # name     ; temp1bsa
 &doit
 0,854979E-01  0,178301E+03  0,383044E+02
 0,882382E-01  0,156139E+03  0,135279E+02
 0,909785E-01  *             0,110681E+02
 0,937188E-01  0,147430E+03  0,954762E+01
 0,964591E-01  0,141615E+03  0,846613E+01
 nan           nan           0

Read by ::

 # ignore is by default '#', so switch it of
 # skip lines with non numbers in data
 # replace some char by others or remove by replacing with empty string ''.
 js.dA('data2.txt',replace={'#':'',';':'',',':'.'},skiplines=[‘*’,'nan'],ignore='' )


pdh format used in some SAXS instruments (first real data point is line 4)::

 SAXS BOX
       2057         0         0         0         0         0         0         0
   0.000000E+00   3.053389E+02   0.000000E+00   1.000000E+00   1.541800E-01
   0.000000E+00   1.332462E+00   0.000000E+00   0.000000E+00   0.000000E+00
 -1.069281E-01   2.277691E+03   1.168599E+00
 -1.037351E-01   2.239132E+03   1.275602E+00
 -1.005422E-01   2.239534E+03   1.068182E+00
 -9.734922E-02   2.219594E+03   1.102175E+00
 ......

Read by::

 # this saves the prepended lines in attribute line_2,...
 empty=js.dA('exampleData/buffer_averaged_corrected_despiked.pdh',usecols=[0,1],lines2parameter=[2,3,4])
 # next just ignores the first lines (and last 50) and uses every second line,
 empty=js.dA('exampleData/buffer_averaged_corrected_despiked.pdh',usecols=[0,1],block=[5,-50,2])

Read csv data by (comma separated list) ::

 js.dA('data2.txt',replace={',':' '})
 # If tabs separate the columns
 js.dA('data2.txt',replace={',':' ','\t':' '})

Get a list of files in a folder with specific names ::

 import glob
 files=glob.glob('latest*.dat')     # files statrting with 'latest' and ending '.dat'
 files=glob.glob('latest???.dat')     # files statrting with 'latest' and ending '.dat' and 3 char in between



Creating from numpy arrays
--------------------------
This demonstrates how to create dataArrays form calculated data with error::

 #
 x=np.r_[0:10:0.5]                 # a list of values
 D,A,q=0.45,0.99,1.2               # parameters
 data=js.dA(np.vstack([x,  np.exp(-q**2*D*x)+np.random.rand(len(x))*0.05,  x*0+0.05]))
 data.diffusiocoefficient=D
 data.amplitude=A
 data.wavevector=q

 # alternative (diffusion with noise and error )
 data=js.dA(np.c_[x,np.exp(-q**2*D*x)*0.05,x*0+0.05].T)
 f=lambda xx,DD,qq,e:np.exp(-qq**2*DD*xx)+np.random.rand(len(x))*e
 data=js.dA(np.c_[x,f(x,D,q,0.05),np.zeros_like(x)+0.05].T)

Manipulating dataArray/dataList
-------------------------------
Changing values uses the same syntax as in numpy arrays with all availible methods and additional .X,.Y .

dataList elements should be changed individually as dataArray (this can be done in loops) ::

 i7=js.dL(js.examples.datapath+'/polymer.dat')
 for ii in i7:
    ii.X/=10          # change scale
    ii.Y/=ii.conc     # normalising by concentration
    ii.Y=-np.log(ii.Y)*2
 i1=js.dA(js.examples.datapath+'/a0_336.dat')
 # all the same to multiply .X by 2
 i1.X*=2
 i1[0]*=2
 i1[0]=i1[0]*2        # most clear writing
 # multiply each second Y value by 2 (using advanced numpy indexing)
 i1[1,::2]=i1[1,::2]*2
 # now more strange: each second gets the value from following *2+1
 # unlimited possibilities to manipulate data :-)
 i1[1,::2]=i1[1,1::2]*2+1 + i1[2,1::2]

 # making a Kratky plot
 p=js.grace()
 i1k=i1.copy()
 i1k.Y=i1k.Y*i1k.X**2
 p.plot(i1k)
 # or
 p.plot(i1.X*10,i1.Y*i1.X**2)

Indexing dataArray/dataList and reducing
----------------------------------------
Basic **Slicing** and Indexing/Advanced Indexing/Slicing works as described at
`numpy <https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html>`_

This means accessing parts of the dataArray/dataList by indexing with integers, boolean masks or arrays
to extract a subset of the data (returning a copy)

[A,B,C] in the following describes A dataList, B dataArray columns and C values in columns.

::

 i5=js.dL(js.examples.datapath+'/iqt_1hho.dat')
 # remove first 2 and last 2 datapoints in all dataArrays
 i6=i5[:,:,:2:-2]
 # remove first column and use 1,2,3 columns in all dataArrays
 i6=i5[:,1:4,:]
 # use each second elelemt in datalist and remove last 2 datapoints in all dataArrays
 i6=i5[::2,:,:-2]
 # You can loop over the dataArrays
 for dat in i5:
    dat.X=dat.X*10
 # select a subset by explicit list
 i7=i5[[2,3,5,6,]]


**Reducing data** to a lower number of values is done by data.prune (see :py:class:`~.dataList` )

prune reduces e.g by 2000 points by averaging in intervalls to get 100 points.

::

 i7=js.dL(js.examples.datapath+'/a0_336.dat')
 # mean values in interval [0.1,4] with 100 points distributed on logscale
 i7_2=i7.prune(lower=0.1,upper=4,number=100,kind='log') #type='mean' is default

dataList can be **filtered** to use a subset e.g. with restricted attribute values as  .q>1 or temp>300 .

::

 i5=js.dL(js.examples.datapath+'/iqt_1hho.dat')
 i6=i5.filter(lambda a:a.q<2)
 i6=i5.filter(lambda a:a.q in [1,2,3,4,5])
 i6=i5.filter(temp=300)         # automatically sorted for these attributes

This demonstrates how to filter data values according to some rule. ::

 x=np.r_[0:10:0.5]
 D,A,q=0.45,0.99,1.2               # parameters
 rand=np.random.randn(len(x))      # the noise on the signal
 data=js.dA(np.vstack([x,np.exp(-q**2*D*x)+rand*0.05,x*0+0.05,rand])) # generate data with noise
 # select like this
 newdata=data[:,data[3]>0]         # take only positive noise in column 3
 newdata=data[:,data.X>2]          # X>2
 newdata=data[:,data.Y<0.9]        # Y<0.9

Fitting experimental data
-------------------------
We need:

- **Data** need to be read and prepared.
 - Data may be a single dataset (usually in a *dataArray*) or several of these (in a *dataList*) like
   multiple measurements with same or changing parameters (e.g. wavevectors).
   Coordinates are in *.X* and values in *.Y*
 - 2D data (e.g. a detector image with 2 dimensions) need to be transfomed to coordinates
   *.X*,*.Z* with values in *.Y*. This also gives pixels coordinates in an image a physical
   interpretation as e.g. wavevectors.
   See last example in :ref:`Some Sinusoidal fits with different kinds to use data atrributes`
 - Attributes need to be extracted from read data (from Comments or filename or from a list..)
   In the below example the Temperature is stored in the data.

- A **model**, which can be defined in different ways.
  See below or in :ref:`How to build simple models` for different ways.

  Please avoid using lists as parameters as list are used to discriminate
  between common parameters (a single float) and individual fit parameters
  (a list of float for each) in dataList.

- **Fit algorithm**
  We use methods from the scipy.optimize module that are incorporated in the *.fit*
  method of *dataArray/dataList*. *.fit* supports different fit algorithms
  (see dataList.fit Examples how to choose and about speed differences):
 - method='leastsq' (default) is a wrapper around MINPACK’s lmdif and lmder, which is a modification
   of the `Levenberg-Marquardt <https://en.wikipedia.org/wiki/Levenberg-Marquardt_algorithm>`_ algorithm.
   This is what you usually expect by "fitting" including error bars (and a covariance matrix for experts....).
   Errors are *1-sigma* errors as they are calculated from the covariance matrix and not directly depend
   on the errors of the *.eY*. Still the relative weight of values according to *.eY* is relevant.
 - method='differential_evolution' is a global optimization method using iterative improving candidate solutions.
   In general it needs a large number of function calls but may find a global minimum and gives error bars.
 - method=‘BFGS’, ‘Nelder-Mead’, ..... other optimization methods.
   These are slower converging than 'leastsq' and give no error bars.
   Some require a gradient function ore more.
   They are more for advanced users if someone realy knows why using it in special cases.

.. Warning:: **Save results !!!**

             The resulting parameters with errors are in *.lastfit*. **Save the fit result !!!**
             I regularly have to ask PhD students "What are the errors ?" and they
             repeat all their work again.

             Fit results without Errors are meaningless.


**If the fit finishes it tells if there was success or if it failed.
For error messages the final parameters are no valid fit results!!! Please always check this.**

A typical example of several datasets from a SAXS measurement (polymer solution)
::

 import jscatter as js
 import numpy as np

 # read data
 data=js.dL(js.examples.datapath+'/polymer.dat')
 # merge equal Temperatures each measured with two detector distances
 data.mergeAttribut('Temp',limit=0.01,isort='X')

 # define model
 # q will get the X values from your data as numpy ndarray.
 def gCpower(q,I0,Rg,A,beta,bgr):
     """Model Gaussian chain  + power law and background"""
     gc=js.ff.gaussianChain(q=q,Rg=Rg)
     # add power law and background
     gc.Y=I0*gc.Y+A*q**beta+bgr
     # add attributes for later documentation, these are additional content of lastfit (see below)
     gc.A=A
     gc.I0=I0
     gc.bgr=bgr
     gc.beta=beta
     gc.comment=['gaussianChain with power law and bgr','a second comment']
     return gc

 data.makeErrPlot(yscale='l',xscale='l')    # additional errorplot with intermediate output
 data.setlimit(bgr=[0,1])                   # upper and lower soft limit

 # here we use individual parameter ([]) for all except a common beta ( no [] )
 # please try removing the [] and play with it :-)
 # mapNames tells that q is *.X* (maps model names to data names )
 # condition limits the range to fit (may also contain something like (a.Y>0))
 data.fit(model=gCpower,
          freepar={'I0':[0.1],'Rg':[3],'A':[1],'bgr':[0.01],'beta':-3},
          fixpar={},
          mapNames={'q':'X'},
          condition =lambda a:(a.X>0.05) & (a.X<4))

 # to fix a parameter move it to fixpar dict (bgr is automatically extended)
 data.fit(model=gCpower,
          freepar={'I0':[0.1],'Rg':[3],'A':[1]},
          fixpar={'bgr':[0.001, 0.0008, 0.0009],'beta':-4},
          mapNames={'q':'X'},
          condition =lambda a:(a.X>0.05) & (a.X<4))

 # result parameter and error (example)
 data.lastfit.Rg
 data.lastfit.Rg_err
 # as result dataArray
 result=js.dA(np.c_[data.Tempmean,data.lastfit.Rg,data.lastfit.Rg_err].T)
 # plot it
 p=js.grace()
 p.plot(result)

 # save the fit result including parameters, errors and covariance matrix
 # and your model description
 data.lastfit.save('polymer_fitDebye.dat')

Why Fits may fail
-----------------

If your fit fails it is most not an error of the fit algorithm.
Read the message at the end of the fit it gives a hint what happend.

- If your fit results in a not converging solution or maximum steps reached then its not a valid fit result.
  Decrease tolerance, increase maxstep or reduce number of parameter to get a valid result.
  Try more reasonable start parameters.
- Your model may have dependent parameters. Then the gradient cannot be evaluated.
  Think of it as a valley with a flat ground. Then you have a line as minimum but you ask for a point.
- Your starting parameters are way of and within the first try the algorithm finds no improvement.
  This may happen if you have a dominating function of high power and bad starting parameters.
  Choose better ones.
- You may run into a local minimum which also depends on the noise in your data.
  Try different start parameter or a global optimization method.
- Play with the starting parameters and get an idea how parameters influence your function.
  This helps to get an idea what goes wrong.

And finally :

- You have choosen the wrong model ( not correlated to your measurement),
  units are wrong by orders of magnitude, missing contributions, .....
  So read the docs of the models and maybe choose a better one.


Plot experimental data and fit result
-------------------------------------
::

 # plot data
 p=js.grace()
 p.plot(data,legend='measured data')
 p.xaxis(min=0.07,max=4,scale='l',label='Q / nm\S-1')
 p.yaxis(scale='l',label='I(Q) / a.u.')
 # plot the result of the fit
 p.plot(data.lastfit,symbol=0,line=[1,1,4],legend='fit Rg=$radiusOfGyration I0=$I0')
 p.legend()

 p1=js.grace()
 # Tempmean because of previous mergeAttribut; otherwise data.Temp
 p1.plot(data.Tempmean,data.lastfit.Rg,data.lastfit.Rg_err)
 p1.xaxis(label='Temperature / C')
 p1.yaxis(label='Rg / nm')

Save data and fit results
-------------------------
jscatter saves files in a ASCII format including attributes that can be
reread including the attributes (See first example above and dataArray help).
In this way no information is lost. ::

 data.save('filename.dat')
 # later read them again
 data=js.dA('filename.dat')  # retrieves all attributes

If needed, the raw numpy array can be saved (see numpy.savetxt).
All attribute information is lost. ::

 np.savetxt('test.dat',data.array.T)

Save fit results by saving the .lastfit attribut (it is in general NOT automatically saved with the above) ::

 data.lastfit.save('fitresult.filename.dat')



Additional stuff
----------------

**Creating grids** as list of points in 3D [Nx3]
e.g. for 2D scattering images or for integration ::

 # inspect the later grids by
 js.mpl.scatter3d(qxyz)
 #
 N=10  # number of points
 d=0.1 # distance between grid points

 # create 2D lattice and append 3rd dimension (2N+1 points in each direction)
 qxy=np.mgrid[-d:d:N*1j, -d:d:N*1j].reshape(2,-1).T    # traditional numpy way
 qxyz=np.c_[qxy,np.zeros(qxy.shape[0])]

 # Use
 qxyz=js.sf.sqLattice(d,[N,N]).XYZ     # 2D lattice from square lattice
 qxyz=js.sf.scLattice(d,[N,N,0]).XYZ   # 3D lattice
 qxyz=js.sf.hexLattice(d,[N,N,0]).XYZ  # 3D lattice hexagonal with z dimension as one layer
 # cube grid with second point in unit cell (2.5D if second point has Z dimension)
 qxyz=js.sf.rhombicLattice([[1,0,0],[0,1,0],[0,0,1]],[3,3,0],[[-0.1,-0.1,0],[0.1,0.1,0]],[1,2]).XYZ
 # 3D grid
 qxyz=js.sf.scLattice(d,[N,N,N]).XYZ

 # grid of pseudorandom points
 qxyz=js.formel.randomPointsInCube(100)  # 3D
 qxyz=np.c_[js.formel.randomPointsInCube(N**2,dim=2),np.zeros(N**2)]  # 2D plane in 3D
 points=js.parallel.randomPointsOnSphere(1500)
 qxyz=js.formel.rphitheta2xyz(points[points[:,1]>0])  # select half sphere

 # rotate if needed
 rotaxis=[0,0,1]       # rotation around y axis
 R=js.formel.rotationMatrix(rotaxis,np.deg2rad(-120))    # -120° rotation matrix
 Rqxyz=np.einsum('ij,kj->ki',R,qxyz)



