from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from .models import CustomUser, Rack, Target
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

@never_cache
@csrf_exempt
def login_view(request):
    context = {}
    
    if request.method == 'POST':
        email = request.POST.get('login-email')
        password = request.POST.get('login-password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)

            # Fetch target numbers and other necessary data
            racks = Rack.objects.prefetch_related('target_set').all()
            rack_data = []
            for rack in racks:
                targets = Target.objects.filter(rack=rack)
                target_data = [
                    {
                        'number': target.number,
                        'telnet_port': target.telnet_port,
                        'telnet_id': target.telnet_id,
                        'is_booked': target.is_booked,
                        'booked_by': target.booked_by.email if target.booked_by else None
                        
                    } 
                    for target in targets
                ]
                rack_data.append({
                    'rack_number': rack.rack_number,
                    'targets': target_data
                })

            # Render home page with target numbers upon successful login
            return render(request, 'home.html', {'racks': rack_data})

        else:
            # Invalid credentials
            context['error'] = 'Invalid login credentials'

    # If GET request or invalid credentials, render login page with context
    return render(request, 'login.html', context)

def register(request):
    context = {}

    if request.method == 'POST':
        email = request.POST.get('register-email')
        password = request.POST.get('register-password')

        if not email.endswith('@alstomgroup.com'):
            context['error'] = 'Email must end with @alstomgroup.com'
        elif CustomUser.objects.filter(email=email).exists():
            context['error'] = 'This email already exists. Try logging in.'
        else:
            user = CustomUser.objects.create_user(email=email, password=password)
            context['success'] = 'Email registered successfully'
        
    return render(request, 'registration.html', context)

def logout_user(request):
    logout(request)  # This logs the user out
    return redirect('login_view')

@login_required
def book_target(request):
    if request.method == 'POST':
        rack_number = request.POST.get('rack_number')  # Assuming you get this from the POST data
        target_number = request.POST.get('target_number')

        try:
            rack = Rack.objects.get(rack_number=rack_number)
            target = Target.objects.get(rack=rack, number=target_number)

            if target.is_booked:
                return JsonResponse({'error': 'Target already booked'}, status=400)

            target.is_booked = True
            target.booked_by = request.user  # Assuming you have user in request
            target.save()

            return JsonResponse({'success': 'Target booked successfully'})
        except Rack.DoesNotExist:
            return JsonResponse({'error': 'Rack not found'}, status=404)
        except Target.DoesNotExist:
            return JsonResponse({'error': 'Target not found'}, status=404)

@login_required
def release_target(request):
    if request.method == 'POST':
        rack_number = request.POST.get('rack_number')
        target_number = request.POST.get('target_number')

        try:
            rack = Rack.objects.get(rack_number=rack_number)
            target = Target.objects.get(rack=rack, number=target_number)

            if target.booked_by != request.user:
                return JsonResponse({'error': 'You cannot release a target you did not book'}, status=400)

            target.is_booked = False
            target.booked_by = None
            target.save()

            return JsonResponse({'success': 'Target released successfully'})
        except Rack.DoesNotExist:
            return JsonResponse({'error': 'Rack not found'}, status=404)
        except Target.DoesNotExist:
            return JsonResponse({'error': 'Target not found'}, status=404)