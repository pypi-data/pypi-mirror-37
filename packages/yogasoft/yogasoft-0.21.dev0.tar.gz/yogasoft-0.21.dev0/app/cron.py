from datetime import datetime
from django_cron import CronJobBase, Schedule
import sys

class JustWriteTimeJob(CronJobBase):

    RUN_EVERY_MINS = 120
    code = 'app.JustWriteTimeJob'
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def do(self):

        with open(sys.argv[0][:sys.argv[0].rfind('/')+1]+'time.txt', 'a') as file:
            file.write(str(datetime.now())+'\n')

