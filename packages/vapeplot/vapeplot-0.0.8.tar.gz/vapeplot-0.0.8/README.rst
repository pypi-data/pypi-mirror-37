vapeplot
========

--------------

matplotlib extension for vaporwave aesthetics

--------------

install
-------

::

    pip install vapeplot

--------------

demo
----

view all palettes
^^^^^^^^^^^^^^^^^

::

    import vapeplot
    %matplotlib inline

    vapeplot.available()

.. figure:: https://raw.githubusercontent.com/dantaki/vapeplot/master/vapeplot.png
   :alt: vapeplot palettes

   alt text

view specific palettes
^^^^^^^^^^^^^^^^^^^^^^

::

    vapeplot.view_palette("cool",'sunset')

.. figure:: https://raw.githubusercontent.com/dantaki/vapeplot/master/view_palette.png
   :alt: cool sunset

   alt text

set the color palette
^^^^^^^^^^^^^^^^^^^^^

::

    import numpy as np
    import matplotlib.pyplot as plt

    vapeplot.set_palette('vaporwave')
    for i in range(10):
        plt.plot(range(100),np.random.normal(i,1,100))
    vapeplot.despine(plt.axes()) #remove right and top axes

.. figure:: https://raw.githubusercontent.com/dantaki/vapeplot/master/vaporwave.png
   :alt: vaporwave palette

   alt test

make a colormap
^^^^^^^^^^^^^^^

::

    cmap = vapeplot.cmap('crystal_pepsi')
    A = np.random.rand(25, 25)
    plt.imshow(A,cmap=cmap)
    # remove all axes
    vapeplot.despine(plt.axes(),True)
    plt.show()

.. figure:: https://raw.githubusercontent.com/dantaki/vapeplot/master/vapeplot_colormaps.png
   :alt: crystal_pepsi colormap

   alt text

access a palette
^^^^^^^^^^^^^^^^

::

    # cool is a list of colors
    cool = vapeplot.palette("cool")

    # reverse the order of colors
    seapunk_r = vapeplot.reverse("seapunk")

--------------

api
---

-  ``vapeplot.available(show=True)``

   -  function to plot all vapeplot palettes
   -  ``show=False`` prints palette names

-  ``vapeplot.cmap(palname)``

   -  returns a colormap object
   -  ``palname`` is the name of the color palette

-  ``vapeplot.despine(ax,all=False)``

   -  removes figure axes
   -  default action: remove right and top axes
   -  ``all=True`` removes all axes

-  ``vapeplot.font_size(s)``

   -  change the font size globally

-  ``vapeplot.palette(palname)``

   -  returns a list of colors
   -  if no ``palname`` is given, a dict of all the palettes is returned

-  ``vapeplot.reverse(palname)``

   -  returns a list of colors in reverse

-  ``vapeplot.set_palette(palname)``

   -  change the color palette globally

-  ``vapeplot.view_palette(*args)``

   -  view individual palettes
   -  arguments: one or more palette names

--------------

more to come :wink:
-------------------
