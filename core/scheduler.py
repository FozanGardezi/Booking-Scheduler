import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

def start():
    scheduler.start()