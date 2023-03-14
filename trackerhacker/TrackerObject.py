class TrackerObject:
    def __init__(self, datapoints, browsers, query_urls, adtrack_blocklists, default, headless):
        self.datapoints = datapoints
        self.browsers = browsers
        self.query_urls = query_urls
        self.adtrack_blocklists = adtrack_blocklists
        self.default  = default
        self.headless = headless 
