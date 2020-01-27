from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phone_field import PhoneField



# Create your models here.

# class MyUser(User):
#     class Meta:
#         proxy = True

#     def __str__(self):
#         return str(self.id)


class Profile(models.Model):
    user_id = models.ForeignKey(User, related_name='profiles', on_delete=models.CASCADE)
    gender = models.CharField(max_length=12, blank=False)
    mobile_no = PhoneField(max_length=20, blank=True)
    #email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    about = models.CharField(max_length=150, blank = True)
    photo = models.ImageField(upload_to='', blank=False)
    #TODO chanage location field here #Have to think of it... Experimental
    location = models.CharField("Office location", blank=False, null=False, max_length = 50)
    # created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.user.username

    class Meta:
        unique_together  = ["user_id", "gender", "mobile_no", "location"]
        ordering = ['user_id']


class List_group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, null=False, max_length=150)
    admin = models.ForeignKey(User, related_name='lists_groups', on_delete=models.CASCADE)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['name', 'admin', 'is_group'], name='group_and_list_unique_key')
        ]

    def __str__(self):
        return self.name


class User_list_group(models.Model):
	id = models.BigAutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	groups_id = models.ForeignKey(List_group, on_delete=models.CASCADE)
	is_working_group = models.BooleanField(default=False)
	email_access = models.BooleanField(default=False)
	mobile_access = models.BooleanField(default=False)
	is_group = models.BooleanField(default=False)

	class Meta:
		constraints = [
		models.UniqueConstraint(fields=['user_id', 'groups_id', 'is_working_group', 'is_group'], name='groups_and_lists_diferentiation_key')
		]
