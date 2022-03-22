from django.db import models
from django.contrib.auth.models import User

# if i wanted images i would need to pip3 install Pillow
# the profile uses the user main info plus adds a first and last name here i am using this becasue in
# the future i may want to add more things to a profile like images


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=25, default="")
    lastName = models.CharField(max_length=25, default="")

    def __str__(self):
        return self.user.username
