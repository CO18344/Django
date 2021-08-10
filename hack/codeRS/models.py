from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import AutoField
from django.db.models.fields.related import ForeignKey
from customauth.models import MyUser
import datetime
# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=200)
    LANGUAGE_CHOICES = [
        ('cpp','C++'),
        ('python','Python'),
    ]
    DIFFICULTY_IN_CHALLENGES_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default='cpp',
    )

    level = models.CharField(
        max_length=8,
        choices=DIFFICULTY_IN_CHALLENGES_CHOICES,
        default='easy',
    )
    description = models.TextField(max_length=1000)
    impKey = models.CharField(max_length=1000,default='imp')
    contraints = models.TextField(max_length=200,null=True,blank=True)
    example = models.TextField(max_length=500,null=True,blank=True)
    inputf = models.TextField(verbose_name='Input format',max_length=1000)
    outputf = models.TextField(verbose_name='Output format',max_length=1000)
    explanation = models.TextField(max_length=3000,blank=True,null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Constraint(models.Model):
    lower_limit = models.BigIntegerField()
    variable = models.CharField(max_length=200)
    upper_limit = models.BigIntegerField()
    pid = models.ForeignKey(verbose_name='Problem ID',to=Problem, on_delete=models.CASCADE)

    def __str__(self):
        return 'Constraint ' +  str(self.id)

class Solved(models.Model):
    pid = models.ForeignKey(verbose_name='Problem ID',to=Problem, on_delete=models.CASCADE)
    uid = models.ForeignKey(verbose_name='User',to=MyUser, on_delete=models.CASCADE)
    time = models.DateField(default=datetime.date.today)

    def __str__(self):
        return 'Solved ' + str(self.id)
