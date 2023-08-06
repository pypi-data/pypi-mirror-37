======================
Google Image Grabber
======================

**Documentation Under Construction**

Towel Stuff provides tools to grab images from a google search by extracting the links of
the images and downloading full resolution images.
Below is a sample on how to use it ::

    #!/usr/bin/env python

    from gImageGrabber import imageScrapeBrowser as imgScrape

    search = 'Python Language'

    data = imgScrape.get_images(imgScrape.build_url(search))
    imgScrape.save_images(data, search, fType)
