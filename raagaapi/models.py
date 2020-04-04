from django.db import models

class Raga(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    format_name = models.CharField(max_length=100, blank=False, null=False, default="")
    melakarta = models.ForeignKey('Raga', null=True, on_delete=models.SET_NULL)
    arohanam = models.CharField(max_length=100, blank=False, null=False)
    avarohanam = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name