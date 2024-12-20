from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import tokenGenerator
from django.contrib import auth


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        # Get user data
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        context = {
            "fieldValues": request.POST,
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short")
                    return render(request, "authentication/register.html", context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                domain = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                link = reverse(
                    "activate",
                    kwargs={"uidb64": uidb64, "token": tokenGenerator.make_token(user)},
                )
                activate_url = f"http://{domain}{link}"
                email_subject = "Activate your account"
                email_body = f"Hi {user.username}, please activate your account using this link:  {activate_url}"
                email_send = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@semycolon.com",
                    [email],
                )
                email_send.send(fail_silently=False)
                messages.success(request, "Account created successfully")
                return render(request, "authentication/register.html")
            else:
                messages.error(request, "Email is already registered")
                return render(request, "authentication/register.html", context)
        else:
            messages.error(request, "Username is already taken")
        return render(request, "authentication/register.html")


class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not tokenGenerator.check_token(user, token):  # check_token
                return redirect("login" + "?message=" + "User already activated")
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully")
                return redirect("login")
            else:
                return redirect("login")
        except Exception as e:
            pass
        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(
                        request, "Welcome, " + user.username + " you are now logged in"
                    )
                    return redirect("/")
                else:
                    messages.error(
                        request, "Account is not activated, please check your email"
                    )
                return render(request, "authentication/login.html")
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, "Please fill all fields")
        return render(request, "authentication/login.html")


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


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "Logout successful")
        return redirect("login")


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
