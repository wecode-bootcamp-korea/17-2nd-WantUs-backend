from django.db import models
from django.db.models.fields import CharField, DateField

from datetime import datetime

class Resume(models.Model):
    user            = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title           = models.CharField(max_length=50)
    introduce       = models.CharField(max_length=300, null=True)
    is_default      = models.BooleanField(default=False)
    complete_status = models.ForeignKey('ResumeStatus', on_delete=models.CASCADE, default=1)
    create_at       = models.DateField(auto_now_add=True)
    update_at       = models.DateField(auto_now=True)

    class Meta:
        db_table = 'resumes'

class ResumeFile(models.Model):
    user            = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title           = models.CharField(max_length=50)
    file_url        = models.URLField(max_length=2000)
    is_default      = models.BooleanField(default=False)
    create_at       = models.DateField(auto_now_add=True)
    update_at       = models.DateField(auto_now=True)
    uuidcode        = models.CharField(max_length=40)
    complete_status = models.ForeignKey('ResumeStatus', on_delete=models.CASCADE, default=3)

    class Meta:
        db_table = 'resume_files'

class ResumeStatus(models.Model):
    status_code = models.CharField(max_length=50)

    class Meta:
        db_table = 'resume_statuses'

class Education(models.Model):
    resume     = models.ForeignKey('Resume', on_delete=models.CASCADE)
    name       = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date   = models.DateField(null=True)

    class Meta:
        db_table = 'educations'

class Language(models.Model):
    resume     = models.ForeignKey('Resume', on_delete=models.CASCADE)
    name       = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date   = models.DateField(null=True)

    class Meta:
        db_table = 'languages'

class Career(models.Model):
    resume     = models.ForeignKey('Resume', on_delete=models.CASCADE)
    name       = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date   = models.DateField(null=True)

    class Meta:
        db_table = 'careers'
