from net import network
from job import job


net = network('../data/USA')
jobs = job.create_jobs_from_params(job,path='jobs.csv')
net.add_job('New-York',jobs[0])
net.add_job('New-York',jobs[1])
net.add_job('Central',jobs[2])
net.add_job('Texas',jobs[3])
net.add_job('Texas',jobs[4])
while net.step():
    net.vis()
