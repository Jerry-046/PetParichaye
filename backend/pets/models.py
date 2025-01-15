from django.db import models
from accounts.models import CustomUser

class Pet(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to="profile_pics/pets/", blank=True, null=True)

    def __str__(self):
        return self.name
