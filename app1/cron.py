from django_cron import CronJobBase, Schedule
from datetime import date
from .models import Donation

class DeleteExpiredDonations(CronJobBase):
    RUN_AT_TIMES = ['21:45']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'app1.delete_expired_donations'

    def do(self):
        expired_donations = Donation.objects.filter(expiration_date__lt=date.today())
        expired_donations.delete()
