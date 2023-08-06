from django.db import models


class AbstractAbout(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='about/')

    class Meta:
        abstract = True
        verbose_name = "About"
        verbose_name_plural = "About"

    def __str__(self):
        return self.title


class About(AbstractAbout):
    pass
