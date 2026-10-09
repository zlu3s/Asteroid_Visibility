import os, sys
import argparse
from datetime import datetime, timedelta

home = os.getenv('AST_HOME')
sys.path.insert(0, f"{home}/src")

from observer import Observer
from configure import Config
from interface import SB_Interface, IP_Interface
from asteroid import Asteroid

params_file = f"{home}/cfg/Input_Parameters.txt"
sb_url = "https://ssd-api.jpl.nasa.gov/sb_ident.api" 
hz_url ="https://ssd.jpl.nasa.gov/api/horizons.api"

def sb_query(obs_time):
    cfg = Config(params_file)
    cfg.SBP['obs-time'] = obs_time
    lat = cfg.SBP['lat']
    lon = cfg.SBP['lon']
    height = cfg.SBP['alt']
    vmag = cfg.SBP['vmag-lim']
    obs = Observer(lat, lon, obs_time, vmag, height)
    inter = SB_Interface(sb_url, cfg.SBP, obs)
    return inter.data


def ip_query(start_time, stop_time, name):
    cfg = Config(params_file)
    cfg.IP['START_TIME'] = start_time
    cfg.IP['STOP_TIME'] = stop_time
    cfg.IP['COMMAND'] = name
    if cfg.IP['CENTER'].upper() == 'TUCSON':
        cfg.IP['CENTER'] = "'G37'"
    inter = IP_Interface(hz_url, cfg.IP)
    return inter.data


def output_data(df):
    df = df.drop(columns=['Dist from RA', 'Dist from Dec', 'Dist from Norm'])
    if args.print:
        import pandas as pd
        pd.set_option("display.max_rows", None)
        print(df)
    else:
        with open(f"{home}/dat/output.txt", 'w') as f:
            f.write(df)


def valid_time(input_time):
    valid_formats = ["%Y-%m-%d_%H:%M:%S"]
    for f in valid_formats:
        try:
            return datetime.strptime(input_time, f)
        except:
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the JPL Horizons system")
    parser.add_argument('start_time', type=valid_time,               \
                        help="Start Time of Query")
    parser.add_argument('-a','--asteroids', nargs="*", default=None, \
                        help="List of asteroid names")
    parser.add_argument('-l', '--length', type=float, default=12,    \
                        help="Hours")
    parser.add_argument('-p', '--print', action='store_true',        \
                        help="Print to terminal")
    args = parser.parse_args()

    start_time = args.start_time.strftime("%Y-%m-%d %H:%M:%S")
    stop_time = (args.start_time+timedelta(hours=args.length)) \
                 .strftime("%Y-%m-%d %H:%M:%S")
    
    if not args.asteroids:
        data = sb_query(start_time)
        output_data(data)
    else:
        for name in args.asteroids:
            output = ip_query(start_time, stop_time, name)
            ast = Asteroid(name, output)
            data = ast.df
            print(data)
