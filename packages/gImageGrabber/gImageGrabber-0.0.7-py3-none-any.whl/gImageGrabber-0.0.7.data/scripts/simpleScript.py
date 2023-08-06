from gimagegrabber import imageScrapeBrowser as imgScrape

# Search term
search = 'Python Language'
fType = ' '  # make sure if you dont want anything then a space is there
debug = True

data = imgScrape.get_images(imgScrape.build_url(search), debug)
imgScrape.save_images(data, search, fType)
