"""
Gets list of asteroids from the given parameters in the input file
"""
import requests
import pandas as pd
import re

from indiv_ast import Asteroid

url = "https://ssd.jpl.nasa.gov/api/horizons.api"


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
            line = lines.split(":")
            parameters[line[0]] = line[1].strip("\n")
        if start in lines:
            check = True
    return parameters



def write_list_data(output, data):
    file = open(output, "w")
    for k,v in data.items():
        file.write(f"{k}: {v}\n")



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
            line = lines.split(":")
            parameters[line[0]] = line[1].strip("\n")
        if start in lines:
            check = True
    return parameters


def search_asts(df,params):
    print("There are {len} asteroids in the list".format(len=len(df)))
    count = int(input("How many asteroids would you like to query: "))
    i = 0
    while True:
        while i < count:
            for desig in df["Primary Desig"].head(count):
                ast = Asteroid(desig,df["Name"][i])
                ast.set_params(params)
                response = requests.get(url,data=ast.params)
                data = response.json()
                ast.get_ephem(data)
                ast.get_header(data)
                ast.set_df()  
                eval_df(ast)
                i += 1
        answer = input("Would you like to observe more asteroid info? Y/N: ")
        if answer == "Y":
            count += int(input("How many more asteroids would you like to observe: "))
        else:
            break


def eval_df(ast):
    print("Values on {date} for asteroid {name}:".format(date=ast.df["Date__(UT)__HR:MN"][0],name=ast.name))
    df = ast.df.apply(pd.to_numeric, errors='coerce')
    means = df.mean()
    for col,value in means.items():
        print("{col}: {value}".format(col=col,value=value)+'\n')



def main():
    
    list_params = get_list_params("Input_Parameters.txt")
    list_response = requests.get(url, params=list_params)
    list_data = list_response.json()
    list, header = get_lists(list_data)

    params = indiv_params("Input_Parameters.txt")
    df = gen_panda(list, header)
    search_asts(df, params)
    #df.to_csv("Asteroid_List.csv", index=False)
    #write_list_data("Asteroid_List.txt", list_data)

if __name__ == "__main__":
    main()