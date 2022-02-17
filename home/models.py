from django.db import models

# Create your models here.
# Database ----> Excel Workbook
# Models In Django -----> Table

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=113)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return 'Issue from ' + self.name + ' - ' + self.email