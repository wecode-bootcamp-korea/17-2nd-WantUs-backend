from django.db import models

class Resume(models.Model):
    user      = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title     = models.CharField(max_length=50)
    introduce = models.CharField(max_length=300)

    class Meta:
        db_table = 'resumes'

class ResumeFile(models.Model):
    user     = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title    = models.CharField(max_length=50)
    file_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'resume_files'

class Education(models.Model):
    resume     = models.ForeignKey('Resume', on_delete=models.CASCADE)
    name       = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date   = models.DateTimeField(null=True)

    class Meta:
        db_table = 'educations'

class Language(models.Model):
    resume     = models.ForeignKey('Resume', on_delete=models.CASCADE)
    name       = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date   = models.DateTimeField(null=True)

    class Meta:
        db_table = 'languages'

class Career(models.Model):
    resume     = models.ForeignKey('Resume', on_delete=models.CASCADE)
    name       = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date   = models.DateTimeField(null=True)

    class Meta:
        db_table = 'careers'