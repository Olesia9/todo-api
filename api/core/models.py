from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Каждая задача принадлежит одному пользователю
    description = models.CharField(max_length=150) #В каждой задаче есть описание того, что необходимо сделать.
    due = models.DateField() #У каждой задачи есть срок выполнения, который представляет собой дату и время datetime.date
