from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Friend(models.Model):
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=200)
    gender = models.BooleanField()
    age = models.IntegerField(validators=[ \
          MinValueValidator(0), \
          MaxValueValidator(150)])
    birthday = models.DateField()
     
    def __str__(self):
        return '<Friend:id=' + str(self.id) + ', ' + \
            self.name + '(' + str(self.age) + ')>'
