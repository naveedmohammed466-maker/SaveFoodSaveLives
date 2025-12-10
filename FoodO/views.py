# from django.shortcuts import render
# #LOGIN VIEW
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Invalid credentials")

#     return render(request, 'login.html')
# #LOGOUT VIEW
# def logout_view(request):
#     logout(request)
#     return redirect('login')

# #DASHBOARD VIEW

# from django.contrib.auth.decorators import login_required
# from .models import Profile

# @login_required
# def dashboard(request):
#     profile = Profile.objects.get(user=request.user)

#     if profile.role == 'restaurant':
#         return render(request, 'restaurant_dashboard.html')
#     else:
#         return render(request, 'ngo_dashboard.html')

# # Create your views here.

# from django.shortcuts import render
# from .models import FoodDonation

# def login_view(request):
#     return render(request, 'login.html')

# def ngo_dashboard(request):
#     donations = FoodDonation.objects.all().order_by('-created_at')
#     return render(request, 'ngo_dashboard.html', {'donations': donations})

# def restaurant_dashboard(request):
#     if request.method == 'POST':
    
#         FoodDonation.objects.create(
#         restaurant=request.POST.get("restaurant"),
#         food_name=request.POST.get("food_name"),
#         food_type=request.POST.get("food_type"),
#         quantity=request.POST.get("quantity"),
#         location=request.POST.get("location"),
#         phone=request.POST.get("phone"),
#         available_till=request.POST.get("available_till"),
#         notes=request.POST.get("notes"),
#         ) 
#         return render(request, 'restaurant_dashboard.html')

#     def ngo_login(request):
#         return render(request, 'ngo_login.html')

#     def restaurant_login(request):
#         return render(request, 'restaurant_login.html')

from django.shortcuts import render, redirect
# from .models import messages
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import FoodDonation, PickupRequest, DashboardStats, RestaurantUser, NGOUser

def login_view(request):
    return render(request, 'login.html')

def ngo_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        NGOUser.objects.create(username=username, password=password)
        request.session['ngo'] = username
        return redirect('ngo_dashboard')
    return render(request, 'ngo_login.html')

def ngo_dashboard(request):
   donations = FoodDonation.objects.filter(is_picked=False)
   stats, created = DashboardStats.objects.get_or_create(id=1)
   
   message = ""

   if request.method == "POST":
        donation_id = request.POST.get("donation_id")

        if donation_id:
            donation = FoodDonation.objects.get(id=donation_id)

            # Create pickup request
            PickupRequest.objects.create(donation=donation)

            message = "✅ Request sent successfully!"

   return render(request, 'ngo_dashboard.html', {
       'donations': donations,
       'stats': stats,
       'message': message
   })

def restaurant_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        RestaurantUser.objects.create(
            username=uname,
            password=pwd
        )
        RestaurantUser.objects.create(username=uname, password=pwd)
        request.session['restaurant'] = uname
        return redirect('restaurant_dashboard')
    return render(request, 'restaurant_login.html') 

def restaurant_dashboard(request):
    # Get logged-in restaurant name safely
    restaurant_name = request.session.get('restaurant')

    # If user directly opens dashboard without login
    if not restaurant_name:
        return redirect('restaurant_login')

    # Save donation when form is submitted
    if request.method == "POST":
        FoodDonation.objects.create(
            restaurant=restaurant_name,   # ✅ Automatically use logged in restaurant
             # restaurant=request.POST['restaurant'],
            food_name=request.POST['food_name'],
            food_type=request.POST['food_type'],
            quantity=request.POST['quantity'],
            location=request.POST['location'],
            phone=request.POST['phone'],
            available_till=request.POST['available_till'],
            notes=request.POST.get('notes', '')
        )

    # Show only requests for this restaurant
    requests = PickupRequest.objects.filter(
        donation__restaurant=restaurant_name
    )

    return render(request, 'restaurant_dashboard.html', {
        'requests': requests,
        'restaurant_name': restaurant_name
    })

    
    # Auto delete food after pickup accepted
    for r in pickup_requests:
        if r.status == "Picked":
            r.donation.delete()
            r.delete()

    return render(request, 'restaurant_dashboard.html', {
        'requests': pickup_requests
    })

# ------------------ PICKUP REQUEST ------------------

def request_pickup(request, id):
    donation = FoodDonation.objects.get(id=id)

    # Save request to DB
    PickupRequest.objects.create(
        donation=donation,
        ngo_name=request.session.get('ngo', 'NGO')
    )

    # Increase pickup counter
    stats = DashboardStats.objects.get(id=1)
    stats.pickup_requests += 1
    stats.save()

    messages.success(request, "Request sent successfully!")

    return redirect('ngo_dashboard')

# ---------- Accept / Reject ----------
@require_POST
def handle_request(request, request_id):
    restaurant_name = request.session.get('restaurant')
    if not restaurant_name:
        return redirect('restaurant_login')

    pickup = PickupRequest.objects.get(id=request_id)

    # Security check – only allow correct restaurant
    if pickup.donation.restaurant != restaurant_name:
        return redirect('restaurant_dashboard')

    action = request.POST.get('action')

    if action == 'accept':
        pickup.status = 'Accepted'
        pickup.save()

        # Block this NGO request from showing elsewhere
        pickup.donation.is_assigned = True
        pickup.donation.save()

    elif action == 'reject':
        pickup.status = 'Rejected'
        pickup.save()

    return redirect('restaurant_dashboard')