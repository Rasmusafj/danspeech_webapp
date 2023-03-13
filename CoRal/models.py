from django.db import models


class Recording(models.Model):
    recorded_file = models.FileField()
    transcription = models.CharField(max_length=1000)
    room_dimensions = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    background_noise = models.CharField(max_length=1000)
    noise = models.CharField(max_length=1000)
    age = models.IntegerField()
    dialect = models.CharField(max_length=1000)
    gender = models.CharField(max_length=1000)
    accent = models.CharField(max_length=1000)
    zipcode_residence = models.CharField(max_length=1000)
    zipcode_birth = models.CharField(max_length=1000)
    education = models.CharField(max_length=1000)
    occupation = models.CharField(max_length=1000)
    birth_place = models.CharField(max_length=1000)
    experiment_start_time = models.CharField(max_length=1000)
    submitted_time = models.CharField(max_length=1000)

    def __str__(self):
        return self.transcription
