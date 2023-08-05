from django.db import models
from django.db.models import Q

# Create your models here.
class Configuration(models.Model):
    end_point = models.URLField(blank=False, null=False)
    token = models.CharField(max_length=50, blank=False, null=False)
    trigger = models.BooleanField(default=False, null=False)
    default = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.end_point

    def save(self, *args, **kwargs):
        if(self.default == True):
            self.__class__.objects.filter(~Q(id=self.id)).update(default=False)
        super(Configuration, self).save(*args, **kwargs)