import re
import pandas as pd


class Asteroid:
    def __init__(self,desig,name):
        self.desig = desig
        self.name = name
        self.params = {}
        self.ephem = []
        self.header = []
        self.df = None
    
    def get_ephem(self, data):
        results = data['result']
        lines = results.split("\n")
        lock = False
        start = "$$SOE"; end = "$$EOE"
        for line in lines:
            if lock:
                self.ephem.append(line)
            if start in line:
                lock = True
            if end in line:
                lock = False
        if len(self.ephem) == 0:
            print("Empty asteroid ephemeris")
        else:
            self.ephem.pop(-1)

    def get_header(self, data):
        results = data['result']
        lines = results.split("\n")
        i = 0
        check = "$$SOE"
        while i < len(results):
            if check in lines[i]:
                start = i-2
                break
            i += 1
        self.header = re.split(r"\s+",lines[start:i-1][0])
        self.header.pop(0)
    
    def set_params(self,params):
        params['COMMAND'] = "'NAME={f.desig}'".format(f=self)
        self.params = params

    def set_df(self):
        data = {}
        i = 0
        while i < len(self.ephem):
            line = re.split(r"\s{2,}", self.ephem[i])
            self.ephem[i] = line
            i += 1
        for i in range(len(self.header)):
            data[self.header[i]] = [line[i] for line in self.ephem]
        self.df = pd.DataFrame(data)