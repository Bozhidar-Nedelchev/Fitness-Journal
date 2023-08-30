from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from Fitness_Journal.app_auth.models import AppUser
from django.db.models.signals import post_save
from django.dispatch import receiver
UserModel = get_user_model()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    age = models.IntegerField(
        blank=True,
        null=True,
    )
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def clean(self):
        if self.age is not None and (self.age < 1 or self.age > 150):
            raise ValidationError("Age must be between 1 and 150.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=UserModel)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Meal(models.Model):
    user = models.ForeignKey('app_auth.AppUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s Meal Plan - {self.date}"


class MealEntry(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE,primary_key=False)
    meal_name = models.CharField(max_length=100)

    def __str__(self):
        return self.meal_name


class UserProfile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    meal_data = models.CharField(max_length=200, blank=True, null=True)


class ProgressPhoto(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='static/')
    caption = models.CharField(max_length=30)
    upload_date = models.DateTimeField(auto_now_add=True)


class Workout(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date = models.DateField()
    workout_type = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.workout_type} on {self.date}"

