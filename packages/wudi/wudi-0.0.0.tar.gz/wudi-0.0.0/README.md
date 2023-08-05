Info
====
`zprint 2018-08-20`

`Author: Zhao Mingming <471106585@qq.com>`

`Copyright: This module has been placed in the public domain.`

`version:0.0.4`
- `add func zprint, print out the function list and time into stdout`
- `add func eprint, print out the function list and time into stderr`
- `add func zhelp, print demo script`
`version:0.0.7`
- `add func zprintr`
`version:0.0.7`
- `add func sys.stdout.flush()`


Functions:

- `add func zprint, print out the function list and time into stdout`
- `add func eprint, print out the function list and time into stderr`

How To Use This Module
======================
.. image:: funny.gif
   :height: 100px
   :width: 100px
   :alt: funny cat picture
   :align: center

1. example code:


.. code:: python

from  zprint  import *   

def fun2():
    zprint(" I am in fun2",0)

def fun1():
    zprint(" I am in fun1")
    fun2()



if __name__=="__main__":
   print 1
   fun1()



Refresh
========
20180820
