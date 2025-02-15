import requests
import json

url = "https://ssd.jpl.nasa.gov/api/horizons.api"

def read_parameters(input):
    parameters = {}
    file = open(input, 'r')
    for lines in file:
        if check_line(lines):
            line = lines.split(":")
            parameters[line[0]] = line[1].strip()
    return parameters

def check_line(line):
    b = True
    illegal_char = ['*','-','|']
    for c in illegal_char:
        if c in line and "'" not in line:
            b = False
    if len(line) < 1 or line == "\n":
        b = False
    return b

def sift_data(data):
    return

def write_data(output, data):
    file = open(output, "w")
    for k,v in data.items():
        file.write(f"{k}: {v}\n")

def main():
    input_param = "Input_Parameters.txt"
    params = read_parameters(input_param)
    print(params)
    response = requests.post(url,data=params)
    data = response.json()
    output_file = "output.txt"
    write_data(output_file, data)
    print(data)
main()