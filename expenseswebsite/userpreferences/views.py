from django.shortcuts import render
import os
import json
from django.contrib import messages
from django.conf import settings
from .models import UserPreferences

# Create your views here.


def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, "currencies.json")
    # import pdb
    # pdb.set_trace()
    with open(file_path) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            currency_data.append({"name": key, "value": value})
    exists = UserPreferences.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreferences.objects.get(user=request.user)

    if request.method == "GET":
        # import pdb
        # pdb.set_trace()
        return render(request, "preferences/index.html", {"currencies": currency_data, "user_preferences": user_preferences})
    else:
        currency = request.POST["currency"]
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
            
        else:
            UserPreferences.objects.create(user=request.user, currency=currency)
        messages.success(request, "Changes saved successfully")
        return render(request, "preferences/index.html", {"currencies": currency_data, "user_preferences": user_preferences})
