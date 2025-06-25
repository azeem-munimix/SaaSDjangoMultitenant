from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="tasks")
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return self.name
