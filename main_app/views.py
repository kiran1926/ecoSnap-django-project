from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Sighting 
import json 
from django.urls import reverse 
from .forms import SightingForm 
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

def index(request):
    if request.user.is_authenticated:
        return redirect('main_app:map_view') 
    return render(request, 'main_app/index.html')

@login_required
def sighting_map_view(request):
    sightings = Sighting.objects.all()
    sightings_data = []
    for sighting in sightings:
        try:
            detail_url = reverse('main_app:sighting_detail', args=[sighting.id])
        except Exception as e: 
            print(f"Error reversing URL for sighting {sighting.id}: {e}") 
            detail_url = f'/sighting/{sighting.id}/' 

        image_urls = []
        if sighting.image_urls:
            image_urls = sighting.image_urls.split('\n') if isinstance(sighting.image_urls, str) else sighting.image_urls

        sightings_data.append({
            'id': sighting.id,
            'species_name': sighting.species_name,
            'description': (sighting.description[:75] + '...') if len(sighting.description) > 75 else sighting.description,
            'latitude': sighting.latitude,
            'longitude': sighting.longitude,
            'detail_url': detail_url,
            'is_native': sighting.is_native,
            'image_urls': image_urls
        })

    context = {
        'mapbox_access_token': 'pk.eyJ1IjoibWlndWVsY29yaWE5NCIsImEiOiJjbWFkY2V6ZmYwY3l6MmxwcDh4anExMmdyIn0.hEMag3lCKS-843Ll_R6jzw',
        'sightings_json': json.dumps(sightings_data)
    }
    return render(request, 'main_app/map_view.html', context)

@login_required
def sighting_detail_view(request, sighting_id):
    sighting = get_object_or_404(Sighting, id=sighting_id)
    context = {
        'sighting': sighting
    }
    return render(request, 'main_app/sighting_detail.html', context)

@login_required
def sighting_create_view(request):
    if request.method == 'POST':
        form = SightingForm(request.POST)
        if form.is_valid():
            new_sighting = form.save(commit=False)
            new_sighting.user = request.user 
            new_sighting.save()
            return redirect('main_app:sighting_detail', sighting_id=new_sighting.id)
    else:
        form = SightingForm()
    
    context = {
        'form': form,
        'mapbox_access_token': 'pk.eyJ1IjoibWlndWVsY29yaWE5NCIsImEiOiJjbWFkY2V6ZmYwY3l6MmxwcDh4anExMmdyIn0.hEMag3lCKS-843Ll_R6jzw' 
    }
    return render(request, 'main_app/sighting_form.html', context)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_app:index') 
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@require_POST
@csrf_exempt
def analyze_image(request):
    """API endpoint to analyze plant images using OpenAI's Vision API"""
    try:
        data = json.loads(request.body)
        image_url = data.get('image_url')
        
        if not image_url:
            return JsonResponse({'error': 'No image URL provided'}, status=400)
        
        openai_api_key = "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"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this plant image and provide the following information in JSON format: 1) species_name: the scientific name of the plant, 2) description: a brief description of the plant, 3) is_native: boolean indicating if this is likely native to North America (true/false), 4) fun_facts: some interesting facts about the plant. If this is not a plant, return an error message."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", 
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            return JsonResponse({'error': f"OpenAI API error: {response.text}"}, status=500)
        
      
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        
        try:
            if content.strip().startswith('{'):
                analysis_data = json.loads(content)
            else:
                import re
                json_match = re.search(r'```json\s*([\s\S]*?)\s*```|{[\s\S]*}', content)
                if json_match:
                    json_str = json_match.group(1) if json_match.group(1) else json_match.group(0)
                    analysis_data = json.loads(json_str)
                else:
                    return JsonResponse({'error': 'Could not parse JSON from API response'}, status=500)
            
            if 'error' in analysis_data:
                return JsonResponse({'error': analysis_data['error']}, status=400)
                
            return JsonResponse(analysis_data)
            
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Failed to parse API response as JSON: {str(e)}'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def sighting_update_view(request, sighting_id):
    """View for editing an existing sighting"""
    sighting = get_object_or_404(Sighting, id=sighting_id)
    if request.user != sighting.user:
        return redirect('main_app:sighting_detail', sighting_id=sighting.id)
    
    if request.method == 'POST':
        form = SightingForm(request.POST, instance=sighting)
        if form.is_valid():
            form.save()
            return redirect('main_app:sighting_detail', sighting_id=sighting.id)
    else:
        form = SightingForm(instance=sighting)
    
    context = {
        'form': form,
        'sighting': sighting,
        'edit_mode': True,
        'mapbox_access_token': 'pk.eyJ1IjoibWlndWVsY29yaWE5NCIsImEiOiJjbWFkY2V6ZmYwY3l6MmxwcDh4anExMmdyIn0.hEMag3lCKS-843Ll_R6jzw'
    }
    return render(request, 'main_app/sighting_form.html', context)

@login_required
def sighting_delete_view(request, sighting_id):
    """View for deleting a sighting"""
    sighting = get_object_or_404(Sighting, id=sighting_id)
    
    if request.user != sighting.user:
        return redirect('main_app:sighting_detail', sighting_id=sighting.id)
    
    if request.method == 'POST':
        sighting.delete()
        return redirect('main_app:map_view')
    
    context = {
        'sighting': sighting
    }
    return render(request, 'main_app/sighting_confirm_delete.html', context)
