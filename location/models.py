from django.db import models

class Location(models.Model): 
	name = models.CharField(max_length=100)
	lock_id = models.CharField(max_length=100)

	def __str__(self):
		return self.name