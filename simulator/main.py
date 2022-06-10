from net import network
from job import job
from data_wrapper import data_wrapper
from datetime import datetime
from optimizer import optimizer
from scheduler import scheduler
import matplotlib.pyplot as plt
import pytz

def split_jobs(x,net):
    jobs = []
    to_add = []
    acc = 0
    for i in x:
        if acc+i.resources<net.get_all_available_resources():
            acc += i.resources
            jobs.append(i)
        else:
            to_add.append(i)
    return jobs, to_add

net = network('../data/USA')
wrapper = data_wrapper('../data/USA/predictions')
#jobs = job.create_n_jobs(job,250)
jobs = job.create_jobs_from_params(job,path='jobs.csv')
b = datetime(2022, 1, 1, 6, 0, 0)
c = datetime(2021, 12, 3, 22, 0, 0)
timezone = pytz.timezone('UTC')

jobs, to_add = split_jobs(jobs, net)
scheduler = scheduler(wrapper,net,timezone.localize(b),"naive",5)
scheduler.step()

jobs = scheduler.schedule(jobs)
i = 0
print('--------------------------------')
cumulated = []
while scheduler.step():
    print(len(jobs))
    curr = net.get_acc_co2()
    #print(curr)
    cumulated.append(sum(curr))
    #scheduler.vis()
    if jobs or to_add:
        jobs, to_add = split_jobs(jobs+to_add, net)
        jobs = scheduler.schedule(jobs)
plt.plot(cumulated)
plt.show()
