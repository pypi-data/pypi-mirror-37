dataList
========

.. currentmodule:: jscatter.dataarray

.. include:: ../../dataarray.py
    :start-after: **dataList**
    :end-before: _end_


Class
-----
.. autosummary::
    dataList

- dataList creating by dataL=js.dL('filename.dat') or from numpy arrays.
- List columns can be accessed as automatic generated attributes like *.X,.Y,.eY* (see protectedNames).
  or by incexing as *dataL[:,0] -> .X * for all list elements.
- Corrsponding column indices are set by :py:meth:`dataList.setColumnIndex` (default X,Y,eY = 0,1,2).
- .Y are used as function values at coordinates [.X,.Z,.W] in fitting.
- Attributes can be set like:  dataL.aName= 1.2345 or dataL[2].aName= 1.2345
- Individual elements and dataArray methods can be accessed by indexing data[2].bName

Attributes
----------
.. autosummary::

      dataList.attr
      dataList.commonAttr
      dataList.dtype
      dataList.names
      dataList.whoHasAttributes
      dataList.showattr

Fitting
-------
.. autosummary::
       
      dataList.fit
      dataList.modelValues
      dataList.setLimit
      dataList.hasLimit
      dataList.setConstrain
      dataList.hasConstrain
      dataList.makeErrPlot
      dataList.makeNewErrPlot
      dataList.detachErrPlot
      dataList.killErrPlot
      dataList.showlastErrPlot
      dataList.errPlot
      dataList.savelastErrPlot
      dataList.interpolate
      dataList.polyfit
      dataList.extrapolate
      dataList.bispline

Housekeeping
------------
.. autosummary::
      
      dataList.setColumnIndex
      dataList.append
      dataList.extend
      dataList.insert
      dataList.prune
      dataList.savetxt
      dataList.sort
      dataList.reverse
      dataList.delete
      dataList.extractAttribut
      dataList.filter
      dataList.index
      dataList.merge
      dataList.mergeAttribut
      dataList.pop
      dataList.copyattr2elements
      dataList.getfromcomment
      dataList.transposeAttribute

  
-----
   
.. autoclass:: jscatter.dataarray.dataList
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:
  
  