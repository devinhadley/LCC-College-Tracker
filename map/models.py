from django.db import models


class College(models.Model):
    name = models.CharField(max_length=50)
    long = models.DecimalField(max_digits=8, decimal_places=3)
    lat = models.DecimalField(max_digits=8, decimal_places=3)
    image = models.URLField(max_length=200,default="N/A")

    def get_students(self):
        return Entry.objects.filter(college=self)


class Entry(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=62)
    college = models.ForeignKey(College, on_delete=models.CASCADE, default=1, related_name="entry")
