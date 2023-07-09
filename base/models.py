from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):       
    def create_user(self, email, password = None, **extra_fields):      
        if not email:   
            raise ValueError('The email should be set')
        email = self.normalize_email(email)      
        user = self.model(email = email, **extra_fields)   
        user.set_password(password)  
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    public_visibility = models.BooleanField(default=False)
    birth_year = models.CharField(max_length=4)
    address = models.TextField(null=True, blank= True)
    profilepic = models.ImageField(upload_to='uploads/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    about = models.TextField
    Type = models.CharField(max_length=100, choices=(('IT','IT'),('Non IT', 'Non IT'),('mobiles', 'mobiles')))
    created = models.DateTimeField(auto_now=True)

    def __str__(self):      #you convert a Company object to a string, it will return the value of its name attribute.
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)