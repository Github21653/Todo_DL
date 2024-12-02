from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(blank = True)
    date_created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=1, choices=[(i,i) for i in range(1,4)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
