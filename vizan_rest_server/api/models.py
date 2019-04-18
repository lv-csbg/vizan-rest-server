from django.db import models

# Create your models here.
ANALYSIS_TYPES = (('FBA', 'FLUX BALANCE ANALYSIS'), ('FVA', 'FLUX VARIABILITY ANALYSIS'))


class Analysis(models.Model):
    model = models.TextField()
    svg = models.TextField()
    analysis_type = models.CharField(choices=ANALYSIS_TYPES, max_length=3, blank=False, default='FBA')

    class Meta:
        ordering = ('model',)
