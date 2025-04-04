from django.db import models
from django.contrib.auth.models import User

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    farm_size = models.FloatField(help_text="Farm size in acres")
    soil_type = models.CharField(max_length=50, choices=[
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('silty', 'Silty'),
    ])
    water_source = models.CharField(max_length=50, choices=[
        ('well', 'Well'),
        ('canal', 'Canal'),
        ('rain', 'Rain-fed'),
        ('other', 'Other'),
    ])
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class QueryHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    query_type = models.CharField(max_length=50, choices=[
        ('crop', 'Crop Recommendation'),
        ('water', 'Water Management'),
        ('general', 'General Advice'),
    ])
    
    def __str__(self):
        return f"{self.user.username}'s query at {self.timestamp}"

class WellDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diameter = models.FloatField(help_text="Diameter in meters")
    depth = models.FloatField(help_text="Depth in meters")
    water_level = models.FloatField(help_text="Current water level in meters")
    last_measured = models.DateField()
    
    def __str__(self):
        return f"Well for {self.user.username}"