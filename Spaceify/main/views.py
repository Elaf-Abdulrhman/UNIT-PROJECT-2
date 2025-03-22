from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomLoginForm, CustomSignUpForm
import requests
from PIL import Image
from urllib.parse import unquote

def home(request):
    return render(request, 'main/home.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/home.html', {'login_form': form, 'signup_form': UserCreationForm()})

# Sign Up view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/home.html', {'signup_form': form, 'login_form': AuthenticationForm()})

# View for rendering the room upload page
def add_room(request):
    return render(request, 'main/add_room.html')

# Function to analyze image using DeepAI API
def analyze_image(image_path):
    url = "https://api.deepai.org/api/detection"
    headers = {'api-key': settings.DEEPAI_API_KEY}  # Use environment variable or settings for the API key

    # Open the image file to send in the request
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        # Extract the labels from the API response
        labels = [item['name'] for item in data.get('output', {}).get('detections', [])]
        return labels
    else:
        # In case of failure, return an empty list or handle the error
        return []

# Function to generate recommendations based on detected labels
def generate_recommendations(labels):
    room_labels = [label.lower() for label in labels]
    recommendations = []

    # Customize recommendations based on room type and furniture
    if "bedroom" in room_labels:
        recommendations.append("Consider adding calming colors like blue or green.")
    if "living room" in room_labels:
        recommendations.append("Try placing a rug for warmth and comfort.")
    if "sofa" in room_labels:
        recommendations.append("Consider rearranging the furniture for better flow.")
    if "tv" in room_labels:
        recommendations.append("Try placing the TV on the opposite wall for better viewing angles.")
    if "coffee table" in room_labels:
        recommendations.append("Consider a smaller coffee table to create more space.")

    # Default suggestion if no relevant items are found
    if not recommendations:
        recommendations.append("Try adding some artwork or plants to enhance the space.")

    return recommendations

# View for uploading and analyzing room image
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('room_image'):
        image_file = request.FILES['room_image']
        
        # Save the image to the server
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        file_url = fs.url(filename)
        
        # Get the full path of the uploaded image
        image_path = fs.path(filename)

        # Process the image using the DeepAI API
        labels = analyze_image(image_path)
        
        # Generate recommendations based on the labels
        recommendations = generate_recommendations(labels)

        # Return recommendations and image URL as a JSON response
        return JsonResponse({'recommendations': recommendations, 'image_url': file_url})

    return render(request, 'main/upload_image.html')

def logout_view(request):
    logout(request)
    return redirect('home')
