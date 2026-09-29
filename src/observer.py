from datetime import datetime
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
import astropy.units as u

class Observer:
    def __init__(self, lat, lon, time, vmag=0, height=0, az=0, alt=90, name=None):
        self.lat = float(lat)
        self.lon = float(lon)
        self.time = time

        self.vmag = float(vmag)
        self.height = float(height)
        self.az = float(az)
        self.alt = float(alt)
        self.name = str(name)

    @property
    def location(self):
        return EarthLocation( \
                lat=self.lat * u.deg, \
                lon=self.lon * u.deg, \
                height=self.height * u.m
                )
    @property
    def altaz(self):
        return AltAz( \
                az=self.az*u.deg, \
                alt=self.alt*u.deg, \
                obstime=Time(self.time), \
                location=self.location \
                )
    @property
    def RA_Dec(self):
        return SkyCoord(self.altaz).icrs
    @property
    def ra(self):
        return self.RA_Dec.ra
    @property
    def dec(self):
        return self.RA_Dec.dec

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, val):
        if type(val) == str:
            try:
                self._time = datetime.strptime(val, "%Y-%m-%d_%H:%M:%S")
            except:
                print(f"Invalid format from time {val}. Must be Y-m-d H:M:S")
        elif type(val) == datetime:
            self._time = val
        else:
            print(f"Invalid type {type(val)} for time {val}")
