from net import network
from job import job
from data_wrapper import data_wrapper
from datetime import datetime
from optimizer import optimizer
from scheduler import scheduler
import matplotlib.pyplot as plt
import pytz

net = network('../data/USA')
wrapper = data_wrapper('../data/USA')
jobs = job.create_jobs_from_params(job,path='jobs.csv')
b = datetime(2021, 11, 28, 22, 0, 0)
c = datetime(2021, 11, 29, 22, 0, 0)
timezone = pytz.timezone('UTC')

scheduler = scheduler(wrapper,net,timezone.localize(b),"opt",5)
scheduler.step()

scheduler.schedule(jobs)
i = 0
print('--------------------------------')
cumulated = []
while scheduler.step():
    curr = net.get_acc_co2()
    print(curr)
    cumulated.append(sum(curr))
    #scheduler.vis()
plt.plot(cumulated)
plt.show()
