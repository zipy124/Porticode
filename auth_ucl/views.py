from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.urls import reverse
from uuid import uuid4
from requests import get
from urllib.parse import urlencode

def error_page(request):
    message = request.session.get('error_message') # Pass custom messages to this page
    if(message == None):
        message = 'Sorry, there has been an error! Please try again.'
    request.session['error_message'] = None
    context = {
        'error_message': message
    }
    return render(request, 'auth/error.html', context)

def ucl_login(request):
    return redirect(get_authorisation_url(request))

def get_authorisation_url(request): # Returns the URL for UCL API login
    state = str(uuid4())
    request.session['state'] = state # Store to mitigate CSRF attacks
    params = {
        'client_id': 'id here',
        'state': state
    }
    authorisation_url = 'https://uclapi.com/oauth/authorise?' + urlencode(params)
    return authorisation_url

def ucl_callback_url(request):
    state = request.GET.get('state')
    code = request.GET.get('code')
    result = request.GET.get('result')

    if(result == 'denied'): # User did not verify the app on UCL API
        request.session['error_message'] = "Please allow access through UCL API to use this application!"
        return redirect('auth_ucl:error_page')
    if(state != request.session.get('state')): # Check for CSFR attacks
        raise Exception('Invalid OAuth state')
    if(code):
        student_code = get_student_code(request, code)
    user = authenticate(request, username=student_code, password='')
    if(user):
        login(request, user) # Attach user to current session
    else:
        user = User.objects.create_user(student_code, password='') # Create a non accessible user account
        user.save()
        login(request, user)

    request.session['state'] = None
    return redirect('music:index')

def get_student_code(request, code):
    token_params = { # These are the parameters required for UCL API
        'client_id': 'id here',
        'code': code,
        'client_secret': 'secret here'
    }
    token_url = 'https://uclapi.com/oauth/token'
    r_token = get(token_url, params=token_params).json()
    state = r_token['state']

    if(state != request.session.get('state')): # Check for CSFR attacks
        raise Exception('Invalid OAuth state')

    user_params = {
        'token': r_token['token'],
        'client_secret': 'secret here'

    }
    user_data_url = 'https://uclapi.com/oauth/user/studentnumber'
    r_user_data = get(user_data_url, params = user_params).json()

    student_code = r_user_data['student_number']

    return student_code[1:] # Student code should be 8 digits not 9

def ucl_logout(request):
    logout(request) # Detatch user from session
    return redirect('matchingsystem:index')
