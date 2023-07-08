from rest_framework import serializers
from .models import Company

# class CompanySerializers(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Company
#         fields = '__all__'

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        # exclude = ['company_id',]

    def validate(self, data):
        if data['name']:
            for n in data['name']:
                if n.isdigit():
                    raise serializers.ValidationError({"error":"name cannot contain numeric value"})
    
        return data
