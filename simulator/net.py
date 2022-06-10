import os
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

from datetime import datetime
from datetime import timedelta

class network:
    def __init__(self,data_path,interval_hours = 1, sim_duration_days=2):
        self.graph = nx.Graph()
        self.internal_time = None
        self.interval = timedelta(hours = interval_hours)
        self.sim_end = timedelta(days=sim_duration_days)
        for i in [i for i in os.listdir(data_path) if '.csv'in i]:
            name = i[:-4]
            data = pd.read_csv(data_path+'/'+i)

            # znormalizować - przerobić datetime na utc
            data['datetime']=data.datetime.apply(
                lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S%z")
            )
            if not self.internal_time or self.internal_time>data.datetime.min():
                self.internal_time = data.datetime.min()
                
            self.graph.add_node(name)
            self.graph.nodes[name]['index'] = 0
            self.graph.nodes[name]['data'] = data
            self.graph.nodes[name]['previous_emission'] = np.inf
            self.graph.nodes[name]['current_emission'] = np.inf
            self.graph.nodes[name]['jobs'] = set()
            self.graph.nodes[name]['accumulated_co2'] = 0
            self.graph.nodes[name]['resources'] = 16#np.random.rand()*10
            self.graph.nodes[name]['cords'] = (np.random.randn(),np.random.randn())
        
        self.sim_end = self.sim_end + self.internal_time
        self.countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
            
    def step(self):
        if self.internal_time>self.sim_end:
            return False
            
        for i in self.graph.nodes():
            self.set_emission(i)
            self.acc_co2_compute(i)
            self.filter_jobs(i)
        #w tej funkcji iterowć po dataframe'ach i ustawić current emission
        
        self.internal_time += self.interval
        return True
        
    def predict(self):
        pass
        
    def get_acc_co2(self):
        acc = []
        for i in self.graph.nodes():
            node = self.get_node(i)
            acc.append(node['accumulated_co2'])
        return acc
    def get_node(self,name):
        return self.graph.nodes[name]
        
    def acc_co2_compute(self,name):
        node = self.get_node(name)
        if node['current_emission']==np.inf or node['previous_emission']==np.inf:
            return
        for i in node['jobs']:
            node['accumulated_co2'] += i.resources*(node['current_emission'] + node['previous_emission'])/2
            
    def filter_jobs(self,name):
        node = self.get_node(name)
        node['jobs'] = {*filter(lambda x: x.is_running(), node['jobs'])}
       
    def set_emission(self,name):
        node = self.get_node(name)
        node['previous_emission'] = node['current_emission']
        while node['data'].loc[node['index']].datetime < self.internal_time and node['index'] < node['data'].shape[0]:
            node['index'] += 1
        node['index'] -= 1 
        node['index'] = np.maximum(node['index'],0)
        row = node['data'].loc[node['index']]
        node['current_emission'] = row.carbon_per_MWh
        
    def vis(self):
        if hasattr(self,'put_fun'):
            self.put_fun.__next__()
        else:
            self.countries.plot()
            self.put_fun = self.put_graph_on_plot()

    def put_graph_on_plot(self):
        while True:
            nx.draw(
                self.graph,
                with_labels=True,
                pos = dict([[i,self.get_node(i)['cords']] for i in self.graph.nodes()]),
                node_size = 800,
                node_color = [self.graph.nodes[i]['accumulated_co2'] for i in self.graph.nodes()],
                cmap = 'cool',
                #arrowsize = [self.g[i][j]['avg_traffic']*10+1 for i,j in self.g.edges()]
            )
            plt.pause(0.5) 
            yield None

    def get_available_resources(self,node_name):
        node = self.get_node(node_name)
        return node['resources'] - np.sum([i.resources for i in node['jobs']])

    def add_job(self,node_name,job):
        if node_name in self.graph:
            node = self.get_node(node_name)
            if self.get_available_resources(node_name)> job.resources:
                node['jobs'] |= {job}
                return True
            return False
            
        else:
            raise Exception(f"There is no {node_name} in graph")

    def get_all_available_resources(self):
        acc = 0
        for i in self.graph.nodes():
            acc += self.get_available_resources(i)

        return acc
