from app.library.web import send_http_request, parse_html_response


class BaseGrabber:
    def __init__(self, name, icon=None):
        self.name = name
        self.icon = icon


class HtmlGrabber(BaseGrabber):
    def __init__(self, *, url_mask, search_xpath, **kwargs):
        self.url_mask = url_mask
        self.search_xpath = search_xpath
        super().__init__(**kwargs)

    def grab(self, url):
        response = await send_http_request(url, debug=True)
        result = parse_html_response(response.body, pattern=self.search_xpath)
