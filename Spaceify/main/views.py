from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomLoginForm, CustomSignUpForm
import requests

def home(request):
    return render(request, 'main/home.html')

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

def add_room(request):
    return render(request, 'main/add_room.html')

# Define the free image recognition API (DeepAI in this case)
def analyze_image(image_path):
    url = "https://api.deepai.org/api/detection"
    headers = {'api-key': 'your_deepai_api_key'}  # Replace with your DeepAI API key
    files = {'image': open(image_path, 'rb')}
    
    response = requests.post(url, headers=headers, files=files)
    data = response.json()
    
    # Process the result
    labels = [item['name'] for item in data.get('output', {}).get('detections', [])]
    return labels

def generate_recommendations(labels):
    room_labels = [label.lower() for label in labels]
    recommendations = []

    if "bedroom" in room_labels:
        recommendations.append("Consider adding calming colors like blue or green.")
    if "living room" in room_labels:
        recommendations.append("Try placing a rug for warmth and comfort.")
    if "sofa" in room_labels:
        recommendations.append("Consider rearranging the furniture for better flow.")
    if "tv" in room_labels:
        recommendations.append("Try placing the TV on the opposite wall for better viewing angles.")

    if not recommendations:
        recommendations.append("Try adding some artwork or plants to enhance the space.")
    
    return recommendations

def upload_image(request):
    if request.method == 'POST' and request.FILES['room_image']:
        image_file = request.FILES['room_image']
        
        # Save the image to the server (you can also use free CDNs like ImgBB or Cloudflare for hosting)
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        file_url = fs.url(filename)
        
        # Process the image using the DeepAI API
        image_path = os.path.join(os.getcwd(), file_url[1:])
        labels = analyze_image(image_path)
        
        # Generate room recommendations based on the labels
        recommendations = generate_recommendations(labels)

        return JsonResponse({'recommendations': recommendations, 'image_url': file_url})

    return render(request, 'main/upload_image.html')

def logout_view(request):
    logout(request)
    return redirect('home')
