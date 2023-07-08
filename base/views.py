from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response


# class CompanyViewSet(viewsets.ModelViewSet):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializers

@api_view(['GET'])
def get_company(request):
    company_objs = Company.objects.all()
    serializer = CompanySerializers(company_objs, many = True)
    return Response({"status": 200, "payload": serializer.data})

@api_view(['POST'])
def post_company(request):
    data = request.data
    serializer = CompanySerializers(data = data)

    if not serializer.is_valid():
        print(serializer.errors)
        return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
    
    serializer.save()

    return Response({"status":200, "payload": serializer.data, "message": "You sent"})

@api_view(['PATCH'])
def update_company(request, pk):
    try:
        data = request.data
        company_obj = Company.objects.get(company_id = pk)
        serializer = CompanySerializers(company_obj, data = data, partial = True)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
        
        serializer.save()

        return Response({"status":200, "payload": serializer.data, "message": "You sent"})
    except Exception as e:
        return Response({"status":403, "errors":"invalid id"})
    

@api_view(['DELETE'])
def delete_company(request, pk):
    try:
        company_obj = Company.objects.get(company_id = pk)
        company_obj.delete()
        return Response({"status":200, "message":"Comapany was successfully deleted"})
    except Exception as e:
        print(e)
        return Response({"status":403, "errors":"Invalid ID"})
