import imgScrape

# Search term
search = 'Python Language'
fType = ''  # if you want all the files them make it empty string
debug = True

html = imgScrape.browser(imgScrape.build_url(search), debug)
data = imgScrape.imageLink(html)
imgScrape.saveImages(data, search, fType)
