# used2b
# import datetime
from django.db import models
# Used2B
# from django.contrib.auth.models import User
# is
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils import timezone
from datetime import datetime
# pip install django-ckeditor
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save


# is
class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=225, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    # required fields? for superuser?
    REQUIRED_FIELDS = ['phone_number', 'email', 'first_name', 'last_name']


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=12)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created.time()} - {timezone.localtime(self.created).date()}'

    def calculate_time(self):
        create_time = timezone.localtime(self.created).time()
        return create_time

    def calculate_date(self):
        create_date = timezone.localtime(self.created).date()
        return create_date


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    # Used2B
    # phone = models.CharField(max_length=15, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    # phase2) country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)


class Collection(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=False)
    image = models.ImageField(blank=True, default="fallback.png")
    pub_date = models.DateTimeField("creation date")

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    description = models.TextField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=10)
    is_available = models.BooleanField(default=False)
    image = models.ImageField(blank=True, default="fallback.png")
    has_discount = models.BooleanField(default=False)
    discount = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=2)
    pub_date = models.DateTimeField("creation date")

    def price_with_discount(self):
        amount = self.price - self.price * self.discount / 100
        return amount

    def __str__(self):
        return f"{self.name} از {self.collection.name}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=200, default="", blank=True)
    phone = models.CharField(max_length=13, default="", blank=True)
    date = models.DateField(datetime.today())
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} by {self.customer}"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    blog_image = models.ImageField()
    body = RichTextField()
    # body = models.TextField(max_length=150000)
    pub_date = models.DateTimeField("creation date")
    body_summary = models.TextField(max_length=115, null=True)

    # def body_summary(self):
    #     return self.body[:102]

    def __str__(self):
        return self.title

