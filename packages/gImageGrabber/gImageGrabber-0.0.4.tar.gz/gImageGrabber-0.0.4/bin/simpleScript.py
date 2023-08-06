from gImageGrabber import imageScrapeBrowser as imgScrape

# Search term
search = 'Python Language'
fType = ' '  # make sure if you dont want anything then a space is there
testRun = False

data = imgScrape.get_images(imgScrape.build_url(search), testRun)
imgScrape.save_images(data, search, fType)
