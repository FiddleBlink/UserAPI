from rest_framework import serializers
from .models import Company

# class CompanySerializers(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Company
#         fields = '__all__'

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        # fields = '__all__'
        exclude = ['company_id',]
