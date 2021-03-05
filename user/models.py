from django.db import models

class User(models.Model):
    name            = models.CharField(max_length=50)
    email           = models.EmailField(max_length=50, unique=True)
    phone_number    = models.CharField(max_length=50, unique=True, null=True)
    is_spam         = models.BooleanField(default=True)
    image_url       = models.URLField(max_length=2000, null=True)
    work_experience = models.ForeignKey('WorkExperience', on_delete=models.SET_NULL, null=True)
    social_status   = models.ForeignKey('SocialStatus', on_delete=models.SET_NULL, null=True)
    salary          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    skill           = models.ManyToManyField('Skill', through='UserSkill')
    job_category    = models.ManyToManyField('posting.JobCategory', through='UserJobCategory')
    update_at       = models.DateTimeField(auto_now=True)
    create_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

class UserSkill(models.Model):
    user  = models.ForeignKey('User', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_skills'

class Recommand(models.Model):
    to_user   = models.ForeignKey('User', on_delete=models.CASCADE, related_name='recommanded_person')
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='recommander')

    class Meta:
        db_table = 'recommands'

class Skill(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'skills'

class WorkExperience(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'work_experiences'

class SocialStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'social_statuses'

class UserJobCategory(models.Model):
    user         = models.ForeignKey('User', on_delete=models.CASCADE)
    job_category = models.ForeignKey('posting.JobCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_job_categories'
