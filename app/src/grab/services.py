
class BaseGrabber:
    def __init__(self, name, icon=None, url_mask=None, search_xpath=None):
        self.name = name
        self.icon = icon
        self.url_mask = url_mask
        self.search_xpath = search_xpath

