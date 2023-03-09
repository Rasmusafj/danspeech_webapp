from django.db import models


class Recording(models.Model):
    recorded_file = models.FileField()
    transcription = models.CharField(max_length=1000)
    age = models.IntegerField()
    dialect = models.CharField(max_length=1000)
    gender = models.CharField(max_length=1000)
    accent = models.CharField(max_length=1000)
    zipcode_residence = models.CharField(max_length=1000)
    zipcode_birth = models.CharField(max_length=1000)
    education = models.CharField(max_length=1000)
    ethnicity = models.CharField(max_length=1000)
    occupation = models.CharField(max_length=1000)

    def __str__(self):
        return self.transcription
