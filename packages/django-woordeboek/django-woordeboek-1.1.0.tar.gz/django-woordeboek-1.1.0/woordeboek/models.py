from django.db import models


class Credentials(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Credentials'
        verbose_name_plural = 'Credentials'


class Query(models.Model):
    query = models.CharField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)
    response_time = models.FloatField(blank=True, null=True)
    num_results = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=10, blank=True)
    cached = models.BooleanField(default=False)

    def __str__(self):
        return self.query

    class Meta:
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'


class QueryResult(models.Model):
    query = models.CharField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)
    data = models.TextField()  # holds JSON dump of results
