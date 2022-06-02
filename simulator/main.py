from net import network
from job import job
from data_wrapper import data_wrapper
from datetime import datetime

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
while net.step():
    if(i%12==0):
        
        net.add_job("California",jobs[0])
    net.vis()
