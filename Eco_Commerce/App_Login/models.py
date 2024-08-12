from django.db import models
# Create your models here.
# To create a custom user model and admin  model
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUserManager(BaseUserManager):
    # user access will have only email and pass, email is custom identifier
    def create_user(self, email, password, **extra_fields):
        """ creates and saves a user with a given emaila & pass """
        if not email:  
            raise ValueError("The Email Must Be Set!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)    
        extra_fields.setdefault('is_superuser', True)    
        extra_fields.setdefault('is_active', True)    

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super User must have is_staff = True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super User must have is_superuser = True")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(gettext_lazy('staff status'), default=False, help_text= gettext_lazy('Designate whether the user can login into the site'))
    is_active = models.BooleanField(gettext_lazy('active'), default=True, help_text=gettext_lazy('This user is now active. Unselect it instead of delete it')) 
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def  __str__(self):
        return self.email

    def get_full_name(self):    # default full name of user, now redirecting them to 
        return self.email    
    
    def get_short_name(self):    # default full name of user, now redirecting them to 
        return self.email  
            


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile' )
    username = models.CharField(max_length=100, blank=True)
    address1 = models.TextField(max_length=400, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    joined_date = models.DateField(auto_now_add=True)


    # alternate to views.py
    def __str__(self):
        return self.username + "'s Profile"

    # check all model is filled in the profile
    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]    

        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


# when user is create, profile will be create and they will be linked
# to automatically create Profile/one to one object

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() #same as related name = profile













