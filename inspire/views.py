from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from datetime import datetime, timedelta
from .helperfunctions import *
from .models import *
from .checker import *
from .token import account_activation_token

import environ
import pytz
import requests
import json

env = environ.Env()
environ.Env.read_env()

def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    elif request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if message is None:
            return render(request, "index.html", 
            {"message": message, "error": "Please write us a message."})
        
        usermessage = UserMessage.objects.create_message(name=name, email=email, message=message)
        usermessage.save()

        return render(request, "index.html")



def signup(request):
    if request.method == "GET":
        data = {"recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY}
        return render(request, "signup.html", data)
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        data = {"username": username, "password": password, 
                "email": email, "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY}

        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
        }
        
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        success = False
        if not result["success"]:
            message = "reCAPTCHA invalid. Please try again."
        elif InspireUser.objects.filter(username=username).exists():
            message = "Username is taken"
        elif not valid_username(username):
            message = """Username cannot have spaces or contain any of the following:
            ", ', /, \\, -, @. Username cannot exceed 30 characters"""
        elif not valid_password(password):
            message = """Password must have at least 1 uppercase letter, 
            at least 1 lowercase letter, 1 number, 
            longer than 8 characters, and have no spaces."""
        elif not valid_email(email):
            message = """Enter valid email"""
        elif InspireUser.objects.filter(email=email).exists():
            message = "Email is taken"
        else:
            success = True

        if success:
            user = InspireUser.objects.create_user(username=username, password=password, email=email)
            user.save()

            domain = get_current_site(request).domain
            subject = "Verify Your Email"
            body = render_to_string(
                "emailverification.html",
                {
                    "domain": domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                    "username": username
                }
            )

            print("Sending email...")
            send_mail(
                subject,
                "",
                env('EMAIL_HOST_USER'),
                [email],
                html_message=body
            )
            print("Email sent.")

            notify(user, "Welcome to the Inspire community!")

            return redirect("/login")
        else:
            data["message"] = message
            return render(request, "signup.html", data)

def loginpage(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/feed")
        else:
            return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        rememberme = request.POST.get("remember-me")

        user = authenticate(request, username=username, password=password)

        if user is None:
            userem = InspireUser.objects.filter(email=username, emailverified=True)
            if userem.exists():
                username = userem.first().username

                user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            if rememberme == "on":
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(7200)
            return redirect("/feed")
            
        return render(request, "login.html", 
        {"message": """Wrong username/email or password. 
         Signing in with email must have email verified."""})

def forgotpassword(request):
    data = {"user": request.user}
    if request.method == "GET":
        return render(request, "forgotpassword.html", data)
    elif request.method == "POST":
        email = request.POST.get("email")
        data["email"] = email
        user = InspireUser.objects.filter(email=email)

        if user.exists():
            if not user[0].emailverified:
                data["message"] =  "Email has not been verified. Check sent email to verify email."
                return render(request, "forgotpassword.html", data)     

            code = random_code()
            print(code)

            print("Sending email...")
            send_mail(
                "New Password Code",
                code,
                env('EMAIL_HOST_USER'),
                [email]
            )
            print("Email sent.")

            user.update(pwcode = code)
            user.update(pwcodecreated = datetime.now())

            return redirect("/forgotpassword/change")
        else:
            data["message"] =  "Enter valid email."
            return render(request, "forgotpassword.html", data)     
        
def changepassword(request):
    if request.method == "GET":
        return render(request, "changepassword.html", {"user": request.user, "authenticated": False})
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        data = {"user": request.user, "username": username, "email": email}

        if "check_code" in request.POST:
            code = request.POST.get("code")

            data["authenticated"] =  False

            user = InspireUser.objects.filter(username=username, email=email, pwcode=code)

            if user.exists():
                user = user[0]

                if datetime.now(pytz.utc) - user.pwcodecreated <= timedelta(minutes = 10):
                    data["authenticated"] = True
                    user.pwcode = None
                    user.save()
                    return render(request, "changepassword.html", data)
                else:
                    data["message"] = "Code expired."
                    return render(request, "changepassword.html", data)
                    
            else:
                data["message"] = "Invalid username, email or code. Check email for code. Code can only be used once."
                return render(request, "changepassword.html", data)
        else:
            data["authenticated"] =  True
            pw = request.POST.get("new-pw")
            verify_pw = request.POST.get("verify-new-pw")

            data["pw"] = pw
            data["verify_pw"] = verify_pw

            user  = InspireUser.objects.get(username=username, email=email)

            if pw != verify_pw:
                data["message"] = "Passwords don't match"
            elif not valid_password(pw):
                data["message"] = """Password must have at least 1 uppercase letter, 
                at least 1 lowercase letter, 1 number, 
                longer than 8 characters, and have no spaces."""
            elif datetime.now(pytz.utc) - user.pwcodecreated > timedelta(minutes = 10):
                data["message"] = "Code expired."
            else:
                user.set_password(pw)
                user.save()
                return redirect("/login")

            return render(request, "changepassword.html", data)
        
def activate(request, uidb64, token):
    def get_user_from_email_verification_token(self, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(self))
            user = InspireUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                InspireUser.objects.get(pk=uid).DoesNotExist):
            return None

        if user is not None \
                and \
                account_activation_token.check_token(user, token):
            return user

        return None
    
    if request.method == "GET":
        user = get_user_from_email_verification_token(uidb64, token)
        user.emailverified = True
        user.save()
        return redirect("/login")


def feed(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            featured = get_featured()
            liked = get_liked(request.user, list(featured.values()))
            print(liked)
            print(featured['quote'].postid)
            return render(request, "feed.html", {"user": request.user, "posts": featured, "liked": liked})
        else:
            return redirect("/login")
    elif request.method == "POST":
        logout(request)
        return redirect("/")
    elif request.method == "PUT":
        body = json.loads(request.body)

        handle_like(request.user, body)

        return HttpResponse(500)
    
def account(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "account.html", {"user": request.user})
        else:
            return redirect("/login")
        
def accountsettings(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "accountsettings.html", {"user": request.user})
        else:
            return redirect("/login")
    elif request.method == "POST":
        data = {"user": request.user}
        formtype = request.POST.get("form-id")
        send_success_email = False

        if formtype == "new-username":
            username = request.POST.get("username")
            confirmusername = request.POST.get("confirm-username")

            if username != confirmusername:
                data["usermessage"] = "Usernames don't match."
            elif InspireUser.objects.filter(username=username).exists():
                data["usermessage"] = "Username is taken"
            elif not valid_username(username):
                data["usermessage"] = """Username cannot have spaces or contain any of the following:
                ", ', /, \\, -, @. Username cannot exceed 30 characters"""
            elif request.user.lastunchange is not None:
                if datetime.now(pytz.utc) - request.user.lastunchange > timedelta(days = 1):
                    request.user.username = username
                    request.user.lastunchange = datetime.now(pytz.utc)
                    request.user.save()

                    data["usermessage"] = "Success!"
                    send_success_email = True
                    emailsubject = "New Username"
                    emailmessage = f"Username has successfully switched to: {username}"
                else:
                    data["usermessage"] = "Can only change username once per day."
            else:
                request.user.username = username
                request.user.lastunchange = datetime.now(pytz.utc)
                request.user.save()

                data["usermessage"] = "Success!"
                send_success_email = True
                emailsubject = "New Username"
                emailmessage = f"Username has successfully switched to: {username}"

        elif formtype == "new-email":
            email = request.POST.get("email")
            confirmemail = request.POST.get("confirm-email")

            if email != confirmemail:
                data["emailmessage"] = "Emails don't match."
            elif InspireUser.objects.filter(email=email).exists():
                data["emailmessage"] = "Email is taken"
            elif not valid_email(email):
                data["emailmessage"] = "Email invalid."
            elif request.user.lastemailchange is not None:
                if datetime.now(pytz.utc) - request.user.lastemailchange > timedelta(days = 1):
                    request.user.email = email
                    request.user.lastemailchange = datetime.now(pytz.utc)
                    request.user.emailverified = False
                    request.user.save()

                    data["emailmessage"] = "Success!"
                else:
                    data["emailmessage"] = "Can only change email once per day."
            else:
                request.user.email = email
                request.user.lastemailchange = datetime.now(pytz.utc)
                request.user.emailverified = False
                request.user.save()

                data["emailmessage"] = "Success! Check email to verify email."

                domain = get_current_site(request).domain
                subject = "Verify Your Email"
                body = render_to_string(
                    "emailverification.html",
                    {
                        "domain": domain,
                        "uid": urlsafe_base64_encode(force_bytes(request.user.pk)),
                        "token": account_activation_token.make_token(request.user),
                        "username": request.user.username
                    }
                )

                print("Sending email...")
                send_mail(
                    subject,
                    "",
                    env('EMAIL_HOST_USER'),
                    [email],
                    html_message=body
                )
                print("Email sent.")


        elif formtype == "new-pw":
            currentpw = request.POST.get("current-pw")
            pw = request.POST.get("pw")
            confirmpw = request.POST.get("confirm-pw")

            user = authenticate(request, username=request.user.username, password=currentpw)

            if pw != confirmpw:
                data["pwmessage"] = "Usernames don't match."
            elif user is None:
                print(request.user.username)
                data["pwmessage"] = "Current password is incorrect."
            elif not valid_password(pw):
                data["pwmessage"] = """Password must have at least 1 uppercase letter, 
                at least 1 lowercase letter, 1 number, 
                longer than 8 characters, and have no spaces."""
            elif request.user.lastpwchange is not None:
                if datetime.now(pytz.utc) - request.user.lastpwchange > timedelta(days = 1):
                    request.user.set_password(pw)
                    request.user.lastpwchange = datetime.now(pytz.utc)
                    request.user.save()

                    data["pwmessage"] = "Success!"
                    send_success_email = True
                    emailsubject = "New Password"
                    emailmessage = f"Password has successfully been changed."
                else:
                    data["pwmessage"] = "Can only change username once per day."
            else:
                request.user.set_password(pw)
                request.user.lastpwchange = datetime.now(pytz.utc)
                request.user.save()
    
                data["pwmessage"] = "Success!"
                send_success_email = True
                emailsubject = "New Password"
                emailmessage = f"Password has successfully been changed."


        if send_success_email:
            if request.user.emailverified:
                print("Sending email...")
                send_mail(
                    emailsubject,
                    emailmessage,
                    env('EMAIL_HOST_USER'),
                    [request.user.email]
                )
                print("Email sent.")
                
            notify(request.user, emailmessage)
        
        return render(request, "accountsettings.html", data)
    
def staff(request):
    if request.method == "GET":
        if request.user.is_authenticated and request.user.is_staff:
            return render(request, "staff.html")
        else:
            return HttpResponseForbidden()
        
def staffpost(request, ptype):
    if request.method == "GET":
        if request.user.is_authenticated and request.user.is_staff:
            return render(request, "staffpost.html", {"ptype": ptype})
        else:
            return HttpResponseForbidden()
    elif request.method == "POST":
        title = request.POST.get("title")
        tags = request.POST.get("tags").split(' ')[0:-1]
        category = request.POST.get("category")
        description = request.POST.get("description")
        if ptype == "text":
            text = request.POST.get("text")
            image = request.POST.get("image")

            text = Text.objects.create_text(title, tags, category, description, text, image)
            text.save()
        elif ptype == "video":
            src = request.POST.get("src")
            platform = request.POST.get("platform")

            video = Video.objects.create_video(title, tags, category, description, src, platform)
            video.save()
        
        return render(request, "staffpost.html", {"ptype": ptype})
    
def jsondata(request, data, minlimit, maxlimit):
    if request.method == "GET":
        if request.user.is_authenticated:
            if data == "notifications":
                notis = request.user.notifications[minlimit:maxlimit]
                jsonnotis = []
                for n in notis:
                    noti = Notification.objects.filter(id=n)[0]
                    jsonnotis.append((noti.noti, noti.sent.date()))

                return JsonResponse(jsonnotis, safe=False)
        else:
            return HttpResponseForbidden()
        
def post(request, postid):
    if request.method == "GET":
        if request.user.is_authenticated:
            post = get_post(postid)
            re = similar_posts(postid)
            related = [get_post(r) for r in re]
            liked = get_liked(request.user, [post] + related)
            print(related)
            print(liked)
            return render(request, "post.html", {"user": request.user, 
                        "post": post, "liked": liked, "related": related})
        else:
            return redirect("/login")
    elif request.method == "PUT":
        body = json.loads(request.body)
        
        handle_like(request.user, body)

        return HttpResponse(500)