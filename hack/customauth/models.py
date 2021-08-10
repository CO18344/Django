from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self,email,fname,lname,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not fname:
            raise ValueError('First Name can"t be empty')

        user = self.model(
            email = self.normalize_email(email),
            # fname = fname,
            # lname=lname,
        )

        user.set_password(password)
        user.first_name = fname
        user.last_name = lname

        user.save(using=self._db)
        return user

    def create_superuser(self,email,first_name,last_name,password=None):
        user = self.create_user(
            email,
            fname = first_name,
            lname=last_name,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user
# class MyUser(models.Model):

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    score = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = MyUserManager()
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
