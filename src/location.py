class Location():
    def __init__(self, lat, long, tzid):
        self.lat = lat
        self.long = long
        self.tzid = tzid
    def __repr__(self):
        return f"{self.__class__.__name__}(lat={self.lat}, long={self.long}, tzid={self.tzid})"
