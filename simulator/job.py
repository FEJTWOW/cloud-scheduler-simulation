import numpy as np
import pandas as pd
from time import time
class job:
    def __init__(self, duration, resources, constraints={}):
        self.duration = int(duration)
        self.resources = int(resources)
        self.stress_lvl = 0
        
    def is_running(self):
        self.duration -= 1
        return self.duration>0
        
    @staticmethod
    def create_n_jobs(cls, n, lam_duration=8, lam_resources=1):
        params = [
                    [np.random.poisson(lam_duration),np.random.poisson(lam_resources)%3]
                    for _ in range(n)
        ]
        to_save = pd.DataFrame(params)
        to_save.columns = ['duration','resources']
        to_save.to_csv('jobs.csv')
        return cls.create_jobs_from_params(cls,params=params)
    
    @staticmethod
    def create_jobs_from_params(cls, **args):
        if 'path' in args:
            params = pd.read_csv(args['path'],index_col=0).values
        elif 'params' in args:
            params = args['params']
        else:
            raise Error("Method called without source of params")
        
        return [cls(i,j) for i,j in params]

