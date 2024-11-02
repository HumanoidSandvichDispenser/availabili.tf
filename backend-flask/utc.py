from datetime import timedelta, tzinfo

delta_zero = timedelta(0)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return delta_zero

    def dst(self, dt):
        return delta_zero

    def tzname(self, dt):
        return "UTC"

utc = UTC()
