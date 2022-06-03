from ortools.sat.python import cp_model
import numpy as np
class optimizer:
    def __init__(self,jobs,graph):
        self.index_node_map = dict()
        self.to_optimize  = self.create_optimizer_input(jobs,graph)
        self.num_workers = self.to_optimize.shape[0]
        self.num_tasks = self.to_optimize.shape[1]
        self.model = cp_model.CpModel()
        
        self.x = {}
        for worker in range(self.num_workers):
            for task in range(self.num_tasks):
                self.x[worker, task] = self.model.NewBoolVar(f'x[{worker},{task}]')
        
        # Each worker is assigned to at most one task.
        for worker in range(self.num_workers):
            self.model.AddAtMostOne(self.x[worker, task] for task in range(self.num_tasks))

        # Each task is assigned to exactly one worker.
        for task in range(self.num_tasks):
            self.model.AddExactlyOne(self.x[worker, task] for worker in range(self.num_workers))
            
        self.objective_terms = []
        for worker in range(self.num_workers):
            for task in range(self.num_tasks):
                self.objective_terms.append(self.to_optimize[worker][task] * self.x[worker, task])
        self.model.Minimize(sum(self.objective_terms))
        self.solver = cp_model.CpSolver()
        self.status = self.solver.Solve(self.model)
        
    def get_results(self):
        res = dict()
        #if self.status == cp_model.OPTIMAL or self.status == cp_model.FEASIBLE:
        #    raise Warning("Not optimal")
        for worker in range(self.num_workers):
            for task in range(self.num_tasks):
                if self.solver.BooleanValue(self.x[worker, task]):
                    worker_name = self.index_node_map[worker]
                    if  worker_name in res:
                        res[worker_name].append(task)
                    else:
                        res[worker_name] = [task,]
        return res
        
    def create_optimizer_input(self,jobs,graph):
        job_costs = []
        for i in jobs:
            job_costs.append(i.duration*i.resources)
            
        job_costs = np.array(job_costs).reshape([1,-1])
        
        ind = 0
        workers = []
        for i in graph.nodes():
            node = graph.nodes[i]
            for _ in range(node['resources']):
                self.index_node_map[ind] = i
                workers.append(node['current_emission'])
                ind += 1
        workers = np.array(workers).reshape([-1,1])
        return workers@job_costs
