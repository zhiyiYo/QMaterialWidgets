Quick start
-----------

Install
~~~~~~~

To install Community version:

.. code:: shell

   pip install PySide6-Material-Widgets -i https://pypi.org/simple/

The Community version only provides basic components, while the more advanced ones are available in the `Premium version <https://afdian.net/a/zhiyiYo?tab=shop>`__.


If you are using PySide2, you can download the code in `PySide2 <https://github.com/zhiyiYo/QMaterialWidgets/tree/PySide2>`__ branch.

.. warning:: Don't install PySide6-Material-Widgets and PySide2-Material-Widget, because their package names are all ``qmaterialwidgets``.

Run example
~~~~~~~~~~~
After installing PySide6-Material-Widgets package using pip, you can run the
demo in the examples directory, for example:

.. code:: python

   cd examples/community/button
   python demo.py

.. note:: If you encounter ``ImportError: cannot import name 'XXX' from 'qmaterialwidgets'``, it indicates that the imported components are only available in the Premium version.
