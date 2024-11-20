from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta
from .models import Donation

class DeleteExpiredDonations(CronJobBase):
    run_at_times = ['21:35']  # Run at 12 AM every day

    schedule = Schedule(run_at_times=run_at_times)
    code = 'app1.delete_expired_donations'

    def do(self):
        two_days_ago = datetime.now() - timedelta(days=2)
        expired_donations = Donation.objects.filter(created_on__lt=two_days_ago)
        expired_donations.delete()
