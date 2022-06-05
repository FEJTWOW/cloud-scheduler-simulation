from datetime import datetime, timedelta
from datetime import timezone
from optimizer import optimizer

class scheduler:
    def __init__(self, data_wrapper,net,start_datetime,scheduling_type="naive",naive_limit=5):
        self.data_wrapper = data_wrapper
        self.net = net
        self.naive_limit = naive_limit
        self.scheduling_type = scheduling_type
        zones = data_wrapper.get_zones()
        self.zones_jobs = {}
        self.datetime = start_datetime
        for z in zones:
            self.zones_jobs[z] = []



    def get_avg_hour_emission(self,zone, start,end):
        predictions = self.data_wrapper.get_prediction_span(zone,start,end)
        return sum(predictions)/len(predictions)


    def get_job_zone(self, job,avaliable_zones):
        start = self.datetime
        duration = job.duration
        end = start + timedelta(hours=duration)
        current = (avaliable_zones[0],self.get_avg_hour_emission(avaliable_zones[0],start,end))
        for z in avaliable_zones:
            avg = self.get_avg_hour_emission(z,start,end)
            if avg < current[1]:
                current = (z,avg)

        return current[0]

    def schedule(self,jobs):
        if self.scheduling_type == "naive":
            self.schedule_naive(jobs)
        else:
            self.schedule_optimized(jobs)

    def schedule_optimized(self,jobs):
        opt = optimizer(jobs,self.net.graph)
        result = opt.get_results()
        for key, value in result.items():
            for i in value:
                self.net.add_job(key,jobs[i])

        
    def schedule_naive(self,jobs):
        result = {}
        for j in jobs:
            availabe_zones = []
            for key, value in self.zones_jobs.items():
                if len(value) <self.naive_limit:
                    availabe_zones.append(key)
            zone = self.get_job_zone(j,availabe_zones)
            self.zones_jobs[zone].append(j.duration)
            self.net.add_job(zone,j)

    def step(self):
        self.datetime = self.datetime + timedelta(hours=1)
        if self.scheduling_type == "naive":
            for key, value in self.zones_jobs.items():
                self.zones_jobs[key] = [x-1 for x in value]
        return self.net.step()

    def vis(self):
        self.net.vis()

            



