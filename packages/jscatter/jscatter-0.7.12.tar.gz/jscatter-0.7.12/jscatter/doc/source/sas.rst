smallanglescattering (sas)
==========================

.. automodule:: jscatter.smallanglescattering
    :noindex:

Smear/desmear 1D
----------------
.. autosummary::
    smear
    desmear
    resFunct
    prepareBeamProfile
    getBeamWidth
    plotBeamProfile
    transmissionCorrection
    waterXrayScattering
    AgBeReference

2D sasImage
-----------
.. automodule:: jscatter.sasimagelib
.. autosummary::
    sasImage
    sasImage.maskRegion
    sasImage.maskFromImage
    sasImage.maskRegion
    sasImage.maskRegions
    sasImage.maskbelowLine
    sasImage.maskTriangle
    sasImage.mask4Polygon
    sasImage.maskCircle
    sasImage.save
    sasImage.setDetectorDistance
    sasImage.findCenterOfIntensity
    sasImage.radialAverage
    sasImage.linearAverage
    sasImage.recalibrateDetDistance
    sasImage.gaussianFilter
    sasImage.showPolar
    sasImage.reduceSize
    sasImage.show
    sasImage.getfromcomment
    sasImage.array

2D sasImage convenience
-----------------------
.. currentmodule:: jscatter.sasimagelib
.. autosummary::
    createLogPNG
    createImageDescriptions
    readImages


Housekeeping
------------
.. currentmodule:: jscatter.smallanglescattering
.. autosummary::
    readpdh
    autoscaleYinoverlapX
    removeSpikesMinmaxMethod
    removeSpikes
    locateFiles
    copyFiles
    addXMLParameter
    moveSAXSPACE


---------

.. automodule:: jscatter.smallanglescattering
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: jscatter.sasimagelib
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: jscatter.sas.sasImage
    :members:
    :undoc-members:

   
   