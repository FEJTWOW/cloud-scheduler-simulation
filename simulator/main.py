from net import network
from job import job
from data_wrapper import data_wrapper
from datetime import datetime
from optimizer import optimizer

import matplotlib.pyplot as plt

net = network('../data/USA')
wrapper = data_wrapper('../data/USA')
jobs = job.create_jobs_from_params(job,path='jobs.csv')
b = datetime(2021, 11, 28, 22, 0, 0)
c = datetime(2021, 11, 29, 22, 0, 0)
print(wrapper.get_prediction_span('Texas',b,c))

net.add_job('New-York',jobs[0])
net.add_job('New-York',jobs[1])
net.add_job('Central',jobs[2])
net.add_job('Texas',jobs[3])
net.add_job('Texas',jobs[4])
i = 0
print('--------------------------------')
cumulated = []
while net.step():
    opt = optimizer(jobs,net.graph)
    print(opt.get_results())
    if(i%12==0):
        net.add_job("California",jobs[0])
    curr = net.get_acc_co2()
    print(curr)
    cumulated.append(sum(curr))
    #net.vis()
plt.plot(cumulated)
plt.show()
