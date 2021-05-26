# to test Bearing and Distance btn 2 coordinates


def haversine(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, asin, sqrt, atan2, degrees

    """
    Calculate the great distance in nm and the bearing in degrees
    between two points on the earth (specified in decimal degrees).
    Takes Lat1 Lon1, Lat2 Lon2.  Returns:  distance bearing
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3440.065  # Radius of earth in nm.
    distance = c * r

    # bearing calc:
    bearing = atan2(sin(lon2-lon1)*cos(lat2), cos(lat1) *
                    sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360

    return round(distance, 0), round(bearing, 0)


lat1, lon1 = [10.889, -74.781]  # BAQ
lat2, lon2 = [11.526, -72.926]  # RCH
dist, bear = haversine(lat1, lon1, lat2, lon2)
print(dist)
print(bear)
