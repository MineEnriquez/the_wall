from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import User, Messages
# Create your views here.
def wall(request):
    print("--------------")
    if request.method=="POST":
        pass
    if request.method=="GET":
        pass
    return redirect("/wall_render")

def wall_render(request):
    msgs = Messages.objects.all()
    for msg in msgs:
        print("--------------")
        print(msg.message)


    context = {
        "all_messages" : Messages.objects.all()
    }

    return render(request, "the_wall_app/index.html", context)
