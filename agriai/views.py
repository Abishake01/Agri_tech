from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import FarmerProfileForm, WellDetailsForm, VoiceQueryForm, RegisterForm
from .models import FarmerProfile, QueryHistory, WellDetails
from .ai_services import CropRecommender, WaterAdvisor
from django.http import JsonResponse
import json
from datetime import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
 

# Initialize AI services
crop_advisor = CropRecommender()
water_advisor = WaterAdvisor()

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    try:
        profile = request.user.farmerprofile
    except FarmerProfile.DoesNotExist:
        return redirect('complete_profile')
    
    return render(request, 'dashboard.html', {'profile': profile})

@login_required
def complete_profile(request):
    try:
        # Check if profile already exists
        profile = request.user.farmerprofile
        return redirect('dashboard')
    except FarmerProfile.DoesNotExist:
        if request.method == 'POST':
            form = FarmerProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, 'Profile completed successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = FarmerProfileForm()
        
        return render(request, 'complete_profile.html', {'form': form})
@login_required
def crop_recommendation(request):
    profile = request.user.farmerprofile
    
    # Get current season (simplified)
    today = datetime.now()
    month = today.month
    if 3 <= month <= 5:
        season = 'spring'
    elif 6 <= month <= 8:
        season = 'summer'
    elif 9 <= month <= 11:
        season = 'autumn'
    else:
        season = 'winter'
    
    # Get recommendations
    recommendations = crop_advisor.recommend_crops(
        temperature=25,  # Would normally come from weather API
        rainfall=100,     # Would normally come from weather API
        humidity=60,      # Would normally come from weather API
        soil_type=profile.soil_type,
        water_availability=3  # Scale of 1-5
    )
    
    # Save query to history
    QueryHistory.objects.create(
        user=request.user,
        question=f"Crop recommendation for {season}",
        response=json.dumps(recommendations),
        query_type='crop'
    )
    
    return render(request, 'crop_recommendation.html', {
        'recommendations': recommendations,
        'season': season
    })

@login_required
def water_management(request):
    profile = request.user.farmerprofile
    well_details = WellDetails.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        form = WellDetailsForm(request.POST, instance=well_details)
        if form.is_valid():
            well = form.save(commit=False)
            well.user = request.user
            well.save()
            
            # Calculate drain time (assuming pump rate of 5 liters/sec)
            drain_time = water_advisor.calculate_water_drain_time(
                diameter=well.diameter,
                depth=well.depth,
                current_level=well.water_level,
                pump_rate=5
            )
            
            return render(request, 'water_management.html', {
                'form': form,
                'well_details': well,
                'drain_time': drain_time,
                'calculated': True
            })
    else:
        form = WellDetailsForm(instance=well_details)
    
    return render(request, 'water_management.html', {
        'form': form,
        'well_details': well_details,
        'calculated': False
    })

@login_required
def voice_assistant(request):
    response = None
    
    if request.method == 'POST':
        form = VoiceQueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # Process query through the same logic as the API
            if any(word in query.lower() for word in ['crop', 'plant', 'grow']):
                # Get actual recommendations from your AI service
                profile = request.user.farmerprofile
                recommendations = crop_advisor.recommend_crops(
                    temperature=25,
                    rainfall=100,
                    humidity=60,
                    soil_type=profile.soil_type,
                    water_availability=3
                )
                crop_names = [crop['crop_name'] for crop in recommendations[:3]]
                response = f"Recommended crops: {', '.join(crop_names)}"
                
            elif any(word in query.lower() for word in ['water', 'irrigation', 'well']):
                response = "Visit the Water Management page to analyze your well specifications."
            else:
                response = "I can help with crop and water advice. Please ask specific questions."
            
            # Save to history
            QueryHistory.objects.create(
                user=request.user,
                question=query,
                response=response,
                query_type='general'
            )
    else:
        form = VoiceQueryForm()
    
    return render(request, 'voice_assistant.html', {
        'form': form,
        'response': response
    })
    
    

@csrf_exempt
def voice_assistant_api(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            query = data.get('query', '').lower()
            user = request.user if request.user.is_authenticated else None
            
            # Process query with NLP logic
            if any(word in query for word in ['crop', 'plant', 'grow', 'suggest']):
                # Get default parameters or from user profile
                params = {
                    'temperature': 25,
                    'rainfall': 100,
                    'humidity': 60,
                    'soil_type': 'loamy',
                    'water_availability': 3
                }
                
                if user and hasattr(user, 'farmerprofile'):
                    profile = user.farmerprofile
                    params.update({
                        'soil_type': profile.soil_type,
                        'water_availability': 3  # Could come from user data
                    })
                
                recommendations = crop_advisor.recommend_crops(**params)
                top_crops = [r['crop_name'] for r in recommendations[:3]]
                response = {
                    'text': f"For your farm, I recommend: {', '.join(top_crops)}. " +
                           "Visit the crop recommendations page for details.",
                    'redirect': '/crop-recommendation/'
                }
            
            elif any(word in query for word in ['water', 'irrigation', 'well']):
                response = {
                    'text': "I can help with water management. Please specify your well " +
                           "dimensions on the water management page for precise calculations.",
                    'redirect': '/water-management/'
                }
            
            elif any(word in query for word in ['hello', 'hi', 'hey']):
                response = {'text': "Hello! How can I help with your farming questions today?"}
            
            else:
                response = {
                    'text': "I can help with crop recommendations and water management. " +
                           "Ask me about what to plant or irrigation advice.",
                    'suggestions': [
                        "What crops grow best in my area?",
                        "How much water does my well have?",
                        "What's the most water-efficient crop?"
                    ]
                }
            
            # Save to query history if user is authenticated
            if user:
                QueryHistory.objects.create(
                    user=user,
                    question=query,
                    response=response['text'],
                    query_type='voice'
                )
            
            return JsonResponse(response)
            
        except Exception as e:
            return JsonResponse(
                {'error': f"Sorry, I encountered an error: {str(e)}"},
                status=500
            )
    
    return JsonResponse(
        {'error': 'Only POST requests are supported'},
        status=405
    )

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
 

@csrf_exempt
def voice_query_api(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data
            data = json.loads(request.body)
            query = data.get('query', '').lower()
            
            # Process the query with more sophisticated logic
            if any(word in query for word in ['crop', 'plant', 'grow']):
                # Get recommendations (simplified example)
                recommendations = crop_advisor.recommend_crops(
                    temperature=25,
                    rainfall=100,
                    humidity=60,
                    soil_type='loamy',  # Default, you can get from user profile
                    water_availability=3
                )
                crop_names = [crop['crop_name'] for crop in recommendations[:3]]
                response = f"Based on your conditions, I recommend: {', '.join(crop_names)}"
                
            elif any(word in query for word in ['water', 'irrigation', 'well']):
                # Get water advice (simplified example)
                response = "For water management, please specify your well dimensions on the water management page."
                
            else:
                response = "I can help with crop recommendations and water management. Please ask about specific crops or irrigation needs."
            
            return JsonResponse({
                'response': response,
                'status': 'success'
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)