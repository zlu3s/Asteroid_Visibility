import os, sys

home = os.getenv('AST_HOME')
sys.path.insert(0, f"{home}/src")

from observer import Observer
from configure import Config
from interface import SB_Interface

params_file = f"{home}/cfg/Input_Parameters.txt"
sb_url = "https://ssd-api.jpl.nasa.gov/sb_ident.api" 
hz_url ="https://ssd.jpl.nasa.gov/api/horizons.api"

def sb_observer(cfg):
    lat = cfg.SBP['lat']
    lon = cfg.SBP['lon']
    height = cfg.SBP['alt']
    time = cfg.SBP['obs-time']
    vmag = cfg.SBP['vmag-lim']
    return Observer(lat, lon, time, vmag, height)

def main():
    cfg = Config(params_file)
    obs = sb_observer(cfg)
    inter = SB_Interface(sb_url, cfg.SBP, obs)
    return inter.data

if __name__ == "__main__":
    print("Getting data...")
    out = main()
    print(out)
