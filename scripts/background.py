from astroquery.gaia import Gaia
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
import argparse


def get_stars_gaia(ra, dec, r):
    radius = r/60
    query = f"SELECT source_id, ra, dec, phot_g_mean_mag       \
              FROM gaiadr3.gaia_source                         \
              WHERE 1 = contains(point('ICRS', ra, dec),       \
                        circle('ICRS', {ra}, {dec}, {radius})) \
              AND phot_g_mean_mag < 18"
    job = Gaia.launch_job_async(query)
    stars = job.get_results()
    return stars

def get_stars_simbad(ra, dec, r):
    coord = SkyCoord(ra=ra, dec=dec, unit='deg')
    result = Simbad.query_region(coord, radius=r*u.arcmin)
    return result

def get_coords(RA, Dec):
    coord = SkyCoord(RA, Dec, frame="icrs")
    return coord.ra.deg, coord.dec.deg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for getting background information of a given RA and Dec")
    parser.add_argument('RA', type=str,                                    \
                        help="Sexadesimal format (Example: 24h30m10.01s)")
    parser.add_argument('Dec', type=str,                                   \
                        help="Sexadesimal format (Example: 19d30m10.01s)")
    parser.add_argument('--stars', action='store_true',                    \
                        help="Flag for background star search")
    parser.add_argument('-r', type=float, default=6.87,                    \
                        help="Radius of cone in arcminutes")
    parser.add_argument('-g', '--gaia', action='store_true',                         \
                        help='Use GAIA instead of SIMBAD')
    args = parser.parse_args()

    ra, dec = get_coords(args.RA, args.Dec)
    if args.stars:
        if args.gaia:
            print(get_stars_gaia(ra, dec, args.r))
        else:
            print(get_stars_simbad(ra, dec, args.r))

