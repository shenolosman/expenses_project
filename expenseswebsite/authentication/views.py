from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse(
                {
                    "username_error": "username should only contain alphanumeric characters"
                },
                status=400,
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"username_error": "username already exists"}, status=400
            )

        return JsonResponse({"username_valid": True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        try:
            validate_email(email)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"email_error": "email already exists"}, status=400)
            return JsonResponse({"email_valid": True})

        except ValidationError as e:
            return JsonResponse(
                {"email_error": "Invalid email address"},
                status=400,
            )
