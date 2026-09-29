import os

class Config:
    def __init__(self, cfg):
        self.params = {}
        if os.path.exists(cfg):
            self.get_params(cfg)
        elif type(cfg) == dict:
            self.params = cfg

    def __getattr__(self, name):
        try:
            return self.params[name]
        except KeyError:
            return f"{name} not in {self._params}"
    
    def get_params(self, file):
        valid = False
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if "*" in line:
                    group_params = {}
                    l = line.strip().split()
                    group_name = " ".join(l[1:])
                elif line.strip() == "&&":
                    valid = False
                    self.params[group_name] = group_params
                elif valid:
                    l = line.strip().split(':', 1)
                    group_params[l[0]] = l[1].strip().strip("'")
                elif line.strip() == "&":
                    valid = True
                else:
                    continue
