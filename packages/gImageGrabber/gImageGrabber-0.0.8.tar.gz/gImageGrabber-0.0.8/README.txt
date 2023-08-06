
Google Image Grabber
-------------------------


It provides tools to grab images from a google search by extracting the links of
the images and downloading full resolution images.

This program written in Python is tested on windows 10 64bit processor.
It uses selenium to open a browser so as to scroll down to get more images than
possible otherwise. Thus it need a browser to work correctly. This is on default
set to use chrome browser. The package comes with chromedriver with it.

To **Install** gImageGrabber do as follow:

.. code:: console
   $ pip install gImageGrabber --upgrade

There are 2 python files *imgScrape* and *imgTools*
*imgScrape* has all the utilities needed to run the script but
if you want to have additional control functions you could explore *imgTools*

This how you can **Import** files:

.. code:: python
   from gimagegrabber import imgScrape
   from gimagegrabber import imgTools
