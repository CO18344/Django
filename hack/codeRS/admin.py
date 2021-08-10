from django.contrib import admin
from .models import Problem, Constraint, Solved
from customauth.models import MyUser 
# Register your models here.

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id','title','language','level')

@admin.register(Constraint)
class ConstraintAdmin(admin.ModelAdmin):
    list_display = ('pid','lower_limit','variable','upper_limit')

@admin.register(Solved)
class SolvedAdmin(admin.ModelAdmin):
    list_display = ('pid','uid')

