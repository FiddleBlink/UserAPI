from rest_framework import serializers
from .models import *

# class CompanySerializers(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Company
#         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create(email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

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

class EmployeeSerializers(serializers.ModelSerializer):
    company = CompanySerializers()
    class Meta:
        model = Employee
        fields = '__all__'