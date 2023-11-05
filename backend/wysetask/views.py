from django.shortcuts import render
from django.http import JsonResponse          
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers import serialize
import firebase_admin
from wysetask.models import User
from firebase_admin import credentials
from firebase_admin import auth
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.http import JsonResponse
# Create your views here.
firebase_creds = credentials.Certificate(settings.FIREBASE_CONFIG)
firebase_app = firebase_admin.initialize_app(firebase_creds)

def getUsers(request,pk):
    # get token
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    token = authorization_header.replace("Bearer ","")
    # verify the token
    print("request",token)
    
    try:
        decoded_token = auth.verify_id_token(token)
        print("yaha aaya kya")
        firebase_user_id = decoded_token['user_id']
        user = User.objects.filter(email=pk).values('username', 'email', 'first_name', 'last_name')
        custom_response = []
        for usr in user:
            custom_obj = {
                'username': usr['username'],
                'email': usr['email'],
                'fullname': f"{usr['first_name']} {usr['last_name']}"
            }
            custom_response.append(custom_obj)

        response_object = {"data": custom_response}
    except:
        return JsonResponse({"data":"user token is invalid"})
    return JsonResponse(response_object)


def generate_unique_username(email, base_username):
    username = base_username
    suffix = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{suffix}"
        suffix += 1
    return username


@csrf_exempt
def registerUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        lastname=data.get('lastName')
        firstname=data.get('firstName')
        
        # generate unique username and check wether it exsists in our database if it exists check again        
        base_username = email.split('@')[0]  # Use a portion of the email as the base username
        username = generate_unique_username(email, base_username)
        # Check if the username already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        elif len(password) < 8:
            return JsonResponse({'error': 'The password is too short .It must contain at least 8 characters'}, status=401)
        elif len(password) > 100 or len(email) > 100 or len(firstname) >100 or len(lastname) >100 or len(username) >100: 
            return JsonResponse({'error': 'Only 100 characters are allowed per field'}, status=401)
        elif email == '' or password=='': 
            return JsonResponse({'error': 'Email and Password required'}, status=401)
        # Create a new user
        new_user = User.objects.create_user(username=username,email=email, password=password,lastname=lastname,firstname=firstname)

        if new_user:
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        else:
            # would never reach here as conditions are checked
            return JsonResponse({'error': 'Failed to register user'}, status=500)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

        


@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            # User is authenticated
            uid = email
            custom_token_bytes = auth.create_custom_token(uid)
            custom_token = str(custom_token_bytes, 'utf-8')
            return JsonResponse({'user_id': user.id, 'message': 'Login successful','custom_token':custom_token}, status=200)
        else:
            # Invalid credentials
            return JsonResponse({'error': 'username or password invalid'}, status=401)

    else:
        # Method not allowed
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def updateUser(request):
    if request.method == 'POST':
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        token = authorization_header.replace("Bearer ","")
        try:
            decoded_token = auth.verify_id_token(token)
            user_id = decoded_token.get('uid')

            if user_id is not None:
                data = json.loads(request.body)
                username = data.get('userName')
                first_name = data.get('firstName')
                last_name = data.get('lastName')

            if username and User.objects.exclude(email=user_id).filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            # Fetch the user from the database based on user_id
            user = User.objects.get(email=user_id)
            if username:
                user.username = username
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name

            user.save()  # Save the updated user details
            print(user.first_name)
            response_data = {
                'message': 'User details updated successfully',
                'username': user.username,
                'email': user.email,
                'fullname': f"{user.first_name} {user.last_name}"
            }
        except :
            return JsonResponse({'error':"User Details could not be updated"}, status=403)
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

        
         
        
        

    