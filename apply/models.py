from django.db import models

class Apply(models.Model):
    user           = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting        = models.ForeignKey('posting.Posting', on_delete=models.SET_NULL, null=True)
    process_status = models.ForeignKey('ProcessStatus', on_delete=models.CASCADE, default=1)
    reward_status  = models.ForeignKey('RewardStatus', on_delete=models.CASCADE, default=1)
    update_at      = models.DateTimeField(auto_now=True)
    create_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'applies'

class RewardStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'reward_statuses'

class ProcessStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'process_statuses'