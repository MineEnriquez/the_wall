from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.utils.dateparse import parse_date
# from .models import User
from .models import User, Messages, Comments
from django.contrib import messages # line added during the implementation of validation .
import bcrypt 


def index(request):
    request.session.flush()
    if request.method == "GET":
        return render(request, "login_and_reg_app/login.html")

    if request.method == "POST":
        return render(request, "login_and_reg_app/login.html")

# On POST: Processing view- no rendering of html
# On GET: Render the html page
def register(request):
    if request.method == "GET":
        return render(request, "login_and_reg_app/login.html")

    elif request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
        else:
            #if passwords match:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # create the hash
            print(pw_hash)
            us = User.objects.create(last_name=request.POST['last_name'], first_name=request.POST['first_name'], email=request.POST['email'], password_hash=pw_hash)
            #----- MODIFY NEXT LINE TO REUSE -----
            request.session['current_user']= us.email
            request.session['current_user_id'] = us.id
            request.session['user']=us.first_name
            request.session['latest_message_id'] = ""
            return redirect("/success")  # never render on a post, always redirect!
        return redirect('/register')

def success(request):
    try:
        if request.session['current_user'] == "":
            print( "no user")
            return redirect('/')
        else:
            return redirect(request, "/success_proceed_to_process_wall")   ####### ------MODIFY HERE IF YOU WANT TO REUSE THIS-------
    except:
        return redirect('/')


def validate_login(request):
    request.session.flush()
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), user.password_hash.encode()):
                print("password match------")
                request.session['current_user']=user.email
                request.session['current_user_id']=user.id
                request.session['user']=user.first_name
                request.session['latest_message_id'] = ""
                return redirect("/wall") 
            else:
                print("failed password")
                messages.error(request, "Wrong password was provided")
                return redirect('/register')
        except:
            print ("user not found")
            messages.error(request, "Username not found")
            return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')


def wall(request):
    print("--------------")
    return redirect("/wall_render")

def post_message(request):
    try:
        person = User.objects.get(id=request.session['current_user_id'])
        msg = request.POST['message']
        newmsg = Messages.objects.create(message=msg, user_id=person)
        request.session['latest_message_id'] = newmsg.id
        return redirect("/wall_render")
    except:
        messages.error("it seems like your sessions has terminated. Please login and try again")
        return redirect('/register')

    pass

def wall_render(request):
    print("Render all messages:----")
    comm = Comments.objects.all()
    msg = Messages.objects.all().order_by("-created_at")
    for c in comm:
        print(c.comment)
    context = {
        "all_messages" : Messages.objects.all().order_by("-created_at"),
        "all_comments" : Comments.objects.all()
    }

    return render(request, "login_and_reg_app/index.html", context)

def post_comment(request):
    try:
        _user = User.objects.get(id= request.session['current_user_id'])
        _message = Messages.objects.get(id=request.POST['message_id'])
        _comment = str(request.POST['comment'])
        newcomment = Comments.objects.create(comment = _comment, user_id = _user, message_id = _message)
        print(newcomment.comment)
        return redirect("/wall_render")
    except:
        messages.error("it seems like your sessions has terminated. Please login and try again")
        return redirect('/register')