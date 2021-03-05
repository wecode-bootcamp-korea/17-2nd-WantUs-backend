from django.db import models

class Posting(models.Model):
    title          = models.CharField(max_length=50)
    job_category   = models.ForeignKey('JobCategory', on_delete=models.CASCADE)
    company_detail = models.ForeignKey('CompanyDetail', on_delete=models.CASCADE)
    reward         = models.DecimalField(max_digits=10, decimal_places=2)
    description    = models.TextField()
    posting_mark   = models.ManyToManyField('user.User', through='BookMark', related_name='user_mark_posting')
    posting_like   = models.ManyToManyField('user.User', through='Like', related_name='user_like_posting')
    end_date       = models.DateTimeField()
    update_at      = models.DateTimeField(auto_now=True)
    create_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'postings'

class JobCategory(models.Model):
    name       = models.CharField(max_length=50)
    occupation = models.ForeignKey('Occupation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'job_categories' 

class Occupation(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'occupations'

class Company(models.Model):
    name        = models.CharField(max_length=50)
    icon        = models.URLField(max_length=2000)
    description = models.TextField()
    tag         = models.ManyToManyField('TagDetail', through='CompanyTag')

    class Meta:
        db_table = 'companies'

class CompanyImage(models.Model):
    company   = models.ForeignKey('Company', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'company_images'

class CompanyDetail(models.Model):
    company   = models.ForeignKey('Company', on_delete=models.CASCADE)
    name      = models.CharField(max_length=50)
    address   = models.CharField(max_length=300)
    latitude  = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)
    state     = models.ForeignKey('State', on_delete=models.CASCADE)
    county    = models.ForeignKey('County', on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_details'

class State(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'states'

class County(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'counties'

class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'

class TagDetail(models.Model):
    name = models.CharField(max_length=50)
    tag  = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tag_details'

class CompanyTag(models.Model):
    company    = models.ForeignKey('Company', on_delete=models.CASCADE)
    tag_detail = models.ForeignKey('TagDetail', on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_tags'

class Like(models.Model):
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

class BookMark(models.Model):
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_marks'

