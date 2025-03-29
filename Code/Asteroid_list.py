"""
Gets list of asteroids from the given parameters in the input file
"""
import requests
import pandas as pd
import re

from indiv_ast import Asteroid

from skyfield.api import load, Topos
from skyfield.almanac import find_discrete, dark_twilight_day, sunrise_sunset

url = "https://ssd.jpl.nasa.gov/api/horizons.api"

locations = {
    #Tucson
    "G37": Topos(latitude_degrees=32.2226, longitude_degrees=-110.9747),
    #UKIRT
    "V38": Topos(latitude_degrees=19.825, longitude_degrees=-155.4717, elevation_m=4192)
}


def get_list_params(input):
    parameters = {}
    file = open(input, 'r')
    start = "&"
    stop = "&&"
    check = False
    for lines in file:
        if stop in lines:
            break
        if check:
            line = lines.split(": ")
            parameters[line[0]] = line[1].strip("\n")
        if start in lines:
            check = True
    return parameters



def get_lists(data):
    results = data['result']
    list = []
    lines = results.split("\n")
    start = "Matching small-bodies:"
    end = "********************************"
    check = False
    for line in lines:
        if start in line:
            check = True
        if check:
            if end in line:
                break
            list.append(line)
    list,header = clean(list)
    return list, header



def clean(list):
    """
    Can be updated to include the given parameters in the input file, but right
    now just uses record #, Epoch year, Name, and primary desig in header
    """
    list = list[2:-2]
    list.pop(1)
    i = 0
    while i < len(list):
        line = re.split(r"\s{2,}", list[i])
        list[i] = line
        i += 1
    for line in list:
        for param in line:
            if param == "":
                line.remove(param)
    header = list[0][0:4]
    list.pop(0)
    return list,header



def gen_panda(list, header):
    data = {}
    # just takes the first 4 parameters for now (can be updated later)
    for i in range(len(header)):
        data[header[i]] = [line[i] for line in list]
    df = pd.DataFrame(data)
    return df



def indiv_params(input):
    parameters = {}
    file = open(input, 'r')
    start = "$"
    stop = "$$"
    check = False
    for lines in file:
        if stop in lines:
            break
        if check:
            line = lines.split(": ")
            parameters[line[0]] = line[1].strip("\n")
        if start in lines:
            check = True

    if parameters["CENTER"] == "'UKIRT'":
        parameters["CENTER"] = "'V38'"
    elif parameters["CENTER"].upper() == "'TUCSON'":
        parameters["CENTER"] = "'G37'"
    return parameters



def sort_ast(df, params):
    print("Begin Asteroid Sorting Process. There are {} total asteroids in the list.".format(len(df)))
    valid_ast = {}
    for i, desig in enumerate(df["Primary Desig"]):
        name = df["Name"].iloc[i]
        ast = Asteroid(desig, name) 
        ast.set_params(params)
        print("\n{}: Gathering data for {}...".format(i, name))
        response = requests.get(url, data=ast.params)
        data = response.json()
        ast.get_ephem(data)
        ast.get_header(data)
        ast.set_df()
        
        add = True
        # Sort for airmass
        for index, value in ast.df['a-mass'].items():
            if value == "n.a.":
                add = False
                print("Does not constrain to air mass")
                break
        if add: valid_ast[ast.desig] = ast.df
    return valid_ast



def get_sun(params):
    start = params["START_TIME"].strip("'").split("-")
    end = params["STOP_TIME"].strip("'").split("-")

    # Load ephemeris
    eph = load('de421.bsp')
    ts = load.timescale()
    dusk_dawn = {}

    place = params['CENTER'].strip("'")
    location = locations[place]
    if place == "G37": noon = 19
    elif place == "V38": noon = 22

    # Define time range
    start_time = ts.utc(int(start[0]), int(start[1]), int(start[2]), noon)
    end_time = ts.utc(int(end[0]), int(end[1]), int(end[2]), noon)

    g = dark_twilight_day(eph, location)

    astro_times, astro_events = find_discrete(start_time, end_time, g)

    for t,e in zip(astro_times, astro_events):
        if e == 0: dusk_dawn["Dusk"] = t.utc_datetime()
        elif e == 1: dusk_dawn["Dawn"] = t.utc_datetime()

    dusk_dawn["Dusk"] = dusk_dawn["Dusk"].strftime("%Y-%m-%d %H:%M:%S")
    dusk_dawn["Dawn"] = dusk_dawn["Dawn"].strftime("%Y-%m-%d %H:%M:%S")
    params["START_TIME"] = "'{}'".format(dusk_dawn["Dusk"])
    params["STOP_TIME"] = "'{}'".format(dusk_dawn["Dawn"])
    return params



def print_valid_ast(valid_ast):
    for k,v in valid_ast.items():
        print("{}\n{}\n".format(k,v))


def main():
    
    list_params = get_list_params("C:/Users/Research/Asteroid Project/in_out/Input_Parameters.txt")
    list_response = requests.get(url, params=list_params)
    list_data = list_response.json()
    list, header = get_lists(list_data)

    params = indiv_params("C:/Users/Research/Asteroid Project/in_out/Input_Parameters.txt")
    df = gen_panda(list, header)

    adjusted_params = get_sun(params)
    valid_ast = sort_ast(df, adjusted_params)
    print_valid_ast(valid_ast)


if __name__ == "__main__":
    main()