from django.db import models
from .my_user import MyUser


# Blueprint for creating a single task
class Task(models.Model):

    user = models.ForeignKey("MyUser", on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now=False, auto_now_add=True)
    is_complete = models.BooleanField()
