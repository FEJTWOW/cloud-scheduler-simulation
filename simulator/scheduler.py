from datetime import datetime, timedelta
from datetime import timezone

class data_wrapper:
    def __init__(self, data_wrapper):
        self.data_wrapper = data_wrapper


    def get_avg_hour_emission(self,zone, start,end):
        predictions = self.data_wrapper.get_prediction_span(zone,start,end)
        return sum(predictions)/len(predictions)


    def get_job_zone(self, job):
        start = datetime.now(timezone.utc)
        avaliable_zones = self.data_wrapper.get_zones()
        duration = job.duration
        end = start + timedelta(hours=duration)
        current = (avaliable_zones[0],self.get_avg_hour_emission(avaliable_zones[0],start,end))
        for z in avaliable_zones:
            avg = self.get_avg_hour_emission(z,start,end)
            if avg < current[1]:
                current = (z,avg)

        return current[0]
