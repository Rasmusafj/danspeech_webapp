from django.db import models


class Recording(models.Model):
    recorded_file = models.FileField()
    transcription = models.CharField(max_length=1000)

    def __str__(self):
        return self.transcription
