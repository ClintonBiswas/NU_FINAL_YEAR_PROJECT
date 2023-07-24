from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.
class RefBooks(models.Model):
    book_name = models.CharField(max_length=200)
    bio = models.TextField(max_length=300)
    cover_photo = models.ImageField(upload_to='book_images', blank=True, null=True)
    pdf = models.FileField(upload_to='ref_book')

    def __str__(self) -> str:
        return self.book_name

class NuQuestion(models.Model):
    type = (
        ('Mid Question', 'Mid Question'),
        ('Year Question', 'Year Question'),
    )
    subject_name = models.CharField(max_length=100)
    question_year = models.IntegerField()
    question_type = models.CharField(choices=type, max_length=100)
    question_image = models.ImageField(upload_to='question_image')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.subject_name} question paper"
    

class AddProjects(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='project_image')
    live_demo = models.CharField(max_length=10000, blank=True, null=True)
    github_code = models.CharField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title)
        super(AddProjects, self).save()

class ProgrammingContest(models.Model):
    contest_name = models.CharField(max_length=200)
    organization_name = models.CharField(max_length=200, blank=True, null=True)
    duration = models.TextField()
    join_link = models.CharField(max_length=500, blank=True)

    def __str__(self) -> str:
        return self.contest_name

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name
    
class OurTeam(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField()
    photo = models.ImageField(upload_to='our_team')

    def __str__(self) -> str:
        return self.name