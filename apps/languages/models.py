from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=30)
    #users liked
    #count of likes

    def __str__(self):
        return self.name