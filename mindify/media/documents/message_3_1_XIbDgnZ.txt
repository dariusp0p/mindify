from django.db import models
from django.dispatch import receiver
import os

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30, default="user1234")
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, null=True, blank=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to="images/users/")

    @receiver(models.signals.post_delete, sender='coreApp.User')
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        """Șterge poza de profil când un user e șters."""
        if instance.profile_picture and instance.profile_picture.path and os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)

    @receiver(models.signals.pre_save, sender='coreApp.User')
    def auto_delete_old_file_on_change(sender, instance, **kwargs):
        """Șterge poza veche din media dacă este schimbată."""
        if not instance.pk:
            return  # user nou, deci nu are poza veche
        old_instance = User.objects.get(pk=instance.pk)

        old_file = old_instance.profile_picture
        new_file = instance.profile_picture

        if old_file and old_file != new_file:
            if old_file.path and os.path.isfile(old_file.path):
                os.remove(old_file.path)

    def get_profile_photo_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        
        # Alege poza default în funcție de gen
        if not self.gender:
            return '/static/userApp/images/default_image_neutral.png'
        elif self.gender.lower() == "male":
            return '/static/userApp/images/default_image_man.png'
        else:
            return '/static/userApp/images/default_image_woman.png'
        
    def __str__(self):
        return f"{self.id}. {self.username}"


class Payment(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subscription_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id}: {self.subscription_date}"


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.id}. {self.tag_name}"


class Event(models.Model):
    title = models.CharField(max_length=50)
    id_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(blank=True, null=True)
    is_listed = models.BooleanField(default=True)
    price = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    event_picture = models.ImageField(blank=True, null=True, upload_to="images/events/")
    tags = models.ManyToManyField(Tag, blank=True)

    # Semnal pentru a șterge poza de event când un event este șters
    @receiver(models.signals.post_delete, sender='coreApp.Event')
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        if instance.event_picture and os.path.isfile(instance.event_picture.path):
            os.remove(instance.event_picture.path)

    @receiver(models.signals.pre_save, sender='coreApp.Event')
    def auto_delete_old_file_on_change(sender, instance, **kwargs):
        """Șterge poza veche din media dacă este schimbată."""
        if not instance.pk:
            return  # event nou, deci nu are poza veche
        old_instance = Event.objects.get(pk=instance.pk)

        old_file = old_instance.event_picture
        new_file = instance.event_picture

        if old_file and old_file != new_file:
            if old_file.path and os.path.isfile(old_file.path):
                os.remove(old_file.path)

    def get_event_picture_url(self):
        if self.event_picture:
            return self.event_picture.url
        
        # Alege poza default în caz ca nu este specificat
        return '/static/userApp/images/default_event_photo.png'

    def __str__(self):
        return f"{self.id}. {self.title}"


class Subscription(models.Model):
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)
    left_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.id_user.username} - {self.id_event.title}"

    class Meta:
        unique_together = (('id_event', 'id_user'),)


class Message(models.Model):
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    username_sender = models.CharField(max_length=30)
    date_posted = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        if len(self.body) > 50:
            return f"{self.id}. {self.body[:50]}" + "..."
        return f"{self.id}. {self.body}"
    

    class Meta:
        ordering = ['-date_posted']
    

class Content(models.Model):
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    file_saved = models.FileField(upload_to="documents/")
    audio_extracted = models.FileField(upload_to="audios/", null=True)

    def get_file_path(self):
        return self.file_saved.name  # Returns the full file path relative to MEDIA_ROOT

    def get_file_extension(self):
        return os.path.splitext(self.file_saved.name)[1]

    def __str__(self):
        return self.get_file_path()
    
