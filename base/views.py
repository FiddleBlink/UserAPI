from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout 
from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from datetime import timezone, timedelta, datetime

# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken

##################################################################################################
############################################# APIS ###############################################
##################################################################################################

# class CompanyViewSet(viewsets.ModelViewSet):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializers

# @api_view(['GET'])
# def get_employee(request):
#     employee_objs = Employee.objects.all()
#     serializer = EmployeeSerializers(employee_objs, many = True)
#     return Response({"Status":200, "payload": serializer.data})

# @api_view(['POST'])
# def post_employee(request):
#     data = request.data
#     serializer = EmployeeSerializers(data = data)

#     if not serializer.is_valid():
#         print(serializer.errors)
#         return Response({"Status":403, "errors":serializer.errors, "message":"Invalid Data"})
    
#     serializer.save()

#     return Response({"status":200 , "payload":serializer.data, "message": "You sent"})

# class UserAPI(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data = request.data)
#         if not serializer.is_valid():
#             return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
        
#         serializer.save()

#         user = User.objects.get(email = serializer.data['email'])
#         token_obj, _ = Token.objects.get_or_create(user=user)
#         return redirect('home')

#         # return Response({"status":200, "payload": serializer.data,"token":str(token_obj), "message": "You sent"})

class CompanyAPI(APIView):
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        # Token_val = request.GET.get('token', None)
        # token_obj = Token.objects.get(key=Token_val)
        # user = token_obj.user
        Token_val = request.GET.get('Bearer', None)
        authentication = JWTAuthentication()
        validate_tok = authentication.get_validated_token(Token_val)
        user = authentication.get_user(validate_tok)

        if user.is_authenticated:
            request.META['HTTP_AUTHORIZATION']=f'Bearer {validate_tok}'
        return super().dispatch(request, *args, **kwargs)

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


# # @api_view(['GET'])
# # def get_company(request):
# #     company_objs = Company.objects.all()
# #     serializer = CompanySerializers(company_objs, many = True)
# #     return Response({"status": 200, "payload": serializer.data})

# # @api_view(['POST'])
# # def post_company(request):
# #     data = request.data
# #     serializer = CompanySerializers(data = data)

# #     if not serializer.is_valid():
# #         print(serializer.errors)
# #         return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
    
# #     serializer.save()

# #     return Response({"status":200, "payload": serializer.data, "message": "You sent"})

# # @api_view(['PATCH'])
# # def update_company(request, pk):
# #     try:
# #         data = request.data
# #         company_obj = Company.objects.get(company_id = pk)
# #         serializer = CompanySerializers(company_obj, data = data, partial = True)

# #         if not serializer.is_valid():
# #             print(serializer.errors)
# #             return Response({"status":403, "errors":serializer.errors, "message":"something went wrong"})
        
# #         serializer.save()

# #         return Response({"status":200, "payload": serializer.data, "message": "You sent"})
# #     except Exception as e:
# #         return Response({"status":403, "errors":"invalid id"})
    

# # @api_view(['DELETE'])
# # def delete_company(request, pk):
# #     try:
# #         company_obj = Company.objects.get(company_id = pk)
# #         company_obj.delete()
# #         return Response({"status":200, "message":"Comapany was successfully deleted"})
# #     except Exception as e:
# #         print(e)
# #         return Response({"status":403, "errors":"Invalid ID"})

# ##################################################################################################
# ########################################## USER PATHS ############################################
# ##################################################################################################

def home(request):
    return render(request, 'base/home.html')

def loginuser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email = email, password = password)
        login(request,user)
        # token_obj, _ = Token.objects.get_or_create(user=ins)
        # return redirect('/company/'+f'?token={token_obj.key}')

        refresh = RefreshToken.for_user(user)
        refresh.access_token.set_exp(datetime.now() + timedelta(minutes=5))
        return redirect('/company/'+f'?Bearer={str(refresh.access_token)}')

    return render(request, 'base/login.html')

def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():   
            user = form.save()     
            login(request,user)
            return redirect('home')   
        else:
            return HttpResponse('error occured')
        

    return render(request, 'base/register.html', {'form':form})

def logoutuser(request):
    logout(request)
    return redirect('login')

