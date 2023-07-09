from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# class CompanyViewSet(viewsets.ModelViewSet):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializers

@api_view(['GET'])
def get_employee(request):
    employee_objs = Employee.objects.all()
    serializer = EmployeeSerializers(employee_objs, many = True)
    return Response({"Status":200, "payload": serializer.data})

@api_view(['POST'])
def post_employee(request):
    data = request.data
    serializer = EmployeeSerializers(data = data)

    if not serializer.is_valid():
        print(serializer.errors)
        return Response({"Status":403, "errors":serializer.errors, "message":"Invalid Data"})
    
    serializer.save()

    return Response({"status":200 , "payload":serializer.data, "message": "You sent"})

class UserAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
        
        serializer.save()

        user = User.objects.get(email = serializer.data['email'])
        token_obj, _ = Token.objects.get_or_create(user=user)

        return Response({"status":200, "payload": serializer.data,"token":str(token_obj), "message": "You sent"})

class CompanyAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        company_objs = Company.objects.all()
        serializer = CompanySerializers(company_objs, many = True)
        return Response({"status": 200, "payload": serializer.data})

    def post(self, request):
        data = request.data
        serializer = CompanySerializers(data = data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
        
        serializer.save()

        return Response({"status":200, "payload": serializer.data, "message": "You sent"})

    def put(self, request):
        pass

    def patch(self, request):
        try:
            data = request.data
            company_obj = Company.objects.get(company_id = request.data['company_id'])
            serializer = CompanySerializers(company_obj, data = data, partial = True)

            if not serializer.is_valid():
                print(serializer.errors)
                return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
            
            serializer.save()

            return Response({"status":200, "payload": serializer.data, "message": "You sent"})
        except Exception as e:
            return Response({"status":403, "errors":"invalid id"})

    def delete(self, request):
        try:
            company_obj = Company.objects.get(company_id = request.data['company_id'])
            company_obj.delete()
            return Response({"status":200, "message":"Comapany was successfully deleted"})
        except Exception as e:
            print(e)
            return Response({"status":403, "errors":"Invalid ID"})





# @api_view(['GET'])
# def get_company(request):
#     company_objs = Company.objects.all()
#     serializer = CompanySerializers(company_objs, many = True)
#     return Response({"status": 200, "payload": serializer.data})

# @api_view(['POST'])
# def post_company(request):
#     data = request.data
#     serializer = CompanySerializers(data = data)

#     if not serializer.is_valid():
#         print(serializer.errors)
#         return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
    
#     serializer.save()

#     return Response({"status":200, "payload": serializer.data, "message": "You sent"})

# @api_view(['PATCH'])
# def update_company(request, pk):
#     try:
#         data = request.data
#         company_obj = Company.objects.get(company_id = pk)
#         serializer = CompanySerializers(company_obj, data = data, partial = True)

#         if not serializer.is_valid():
#             print(serializer.errors)
#             return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
        
#         serializer.save()

#         return Response({"status":200, "payload": serializer.data, "message": "You sent"})
#     except Exception as e:
#         return Response({"status":403, "errors":"invalid id"})
    

# @api_view(['DELETE'])
# def delete_company(request, pk):
#     try:
#         company_obj = Company.objects.get(company_id = pk)
#         company_obj.delete()
#         return Response({"status":200, "message":"Comapany was successfully deleted"})
#     except Exception as e:
#         print(e)
#         return Response({"status":403, "errors":"Invalid ID"})
