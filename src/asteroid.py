import re
import pandas as pd


class Asteroid:
    def __init__(self,name,data,desig=None):
        self.desig = desig
        self.name = name
        self.data = data
        self._ephem = []
        self._header = []
        self.setup()


    def setup(self):
        self.ephem
        self.header

    @property
    def ephem(self):
        results = self.data['result']
        lines = results.split("\n")
        start = "$$SOE"; end = "$$EOE"
        add = False
        for line in lines:
            if start in line:
                add = True
            elif end in line:
                add = False
            elif add:
                line = re.split(r"\s{2,}", line)
                if line[1] == 'm':
                    line[0] = f"{line[0]} {line[1]}"
                    line.pop(1)
                self._ephem.append(line)
        return self._ephem

    @property
    def header(self):
        results = self.data['result']
        lines = results.split("\n")
        i = 0
        check = "$$SOE"
        while i < len(results):
            if check in lines[i]:
                start = i-2
                break
            i += 1
        header_line = lines[start:i-1][0]
        self._header = re.split(r"\s+", header_line)
        self._header.pop(0)
        return self._header

    @property
    def df(self):
        return pd.DataFrame(self._ephem, columns=self._header)
