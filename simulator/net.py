import os
import networkx as nx
import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta

class network:
    def __init__(self,data_path,interval_hours = 1, sim_duration_days=25):
        self.graph = nx.Graph()
        self.internal_time = None
        self.interval = timedelta(hours = interval_hours)
        self.sim_end = timedelta(days=sim_duration_days)
        for i in os.listdir(data_path):
            name = i[:-4]
            data = pd.read_csv(data_path+'/'+i)
            data['datetime']=data.datetime.apply(
                lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S%z")
            )
            if not self.internal_time or self.internal_time>data.datetime.min():
                self.internal_time = data.datetime.min()
                
            self.graph.add_node(name)
            self.graph.nodes[name]['data'] = data
            self.graph.nodes[name]['jobs'] = set()
            self.graph.nodes[name]['accumulated_co2'] = 0
            self.self.graph.nodes[name]['resources'] = np.random.rand()*10
            self.graph.nodes[name]['cords'] = (np.random.randn(),np.random.randn())
        
        self.sim_end = self.sim_end + self.internal_time
            
        def step(self):
            while self.internal_time<self.sim_end:
                
                self.internal_time += self.interval
            
        def predict(self):
            pass
            
