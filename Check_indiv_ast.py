import requests
import pandas as pd
import re

url = "https://ssd.jpl.nasa.gov/api/horizons.api"



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


def write_ast_data(output, data):
    file = open(output, "w")
    for k,v in data.items():
        file.write(f"{k}: {v}\n")



def get_ephem(data):
    results = data['result']
    lines = results.split("\n")
    ephem = []
    lock = False
    start = "$$SOE"; end = "$$EOE"
    for line in lines:
        if lock:
            ephem.append(line)
        if start in line:
            lock = True
        if end in line:
            lock = False
    ephem.pop(-1)
    return ephem

def get_header(data):
    results = data['result']
    lines = results.split("\n")
    header = []
    i = 0
    check = "$$SOE"
    while i < len(results):
        if check in lines[i]:
            start = i-2
            break
        i += 1
    header = re.split(r"\s+",lines[start:i-1][0])
    header.pop(0)
    return header

def gen_panda(ephem,header):
    data = {}
    i = 0
    while i < len(ephem):
        line = re.split(r"\s{2,}", ephem[i])
        ephem[i] = line
        i += 1
    for i in range(len(header)):
        data[header[i]] = [line[i] for line in ephem]
    df = pd.DataFrame(data)
    return df

def write_df(df, output):
    df.to_csv(output, index=False)


def main():
    params = indiv_params("Input_Parameters.txt")
    response = requests.post(url,data=params)
    data = response.json()

    ephem = get_ephem(data)
    header = get_header(data)
    df = gen_panda(ephem,header)
    write_df(df, "ephem.txt")

    write_ast_data("Asteroid_Data.txt", data)
main()