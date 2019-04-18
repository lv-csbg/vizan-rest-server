from rest_framework import serializers
from .models import Analysis, Analysis2


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ('model', 'svg', 'analysis_type',)


class Analysis2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis2
        fields = ('model', 'svg', 'analysis_type',)
