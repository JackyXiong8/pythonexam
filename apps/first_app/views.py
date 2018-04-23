from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Q
import bcrypt
from .models import *
  # the index function is called when root is visited
def index(request):
  return render(request, 'first_app/index.html')
  request.session.clear()
  print (request.session['id'])

def register(request):
  errors = User.objects.nameValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
      request.session['first_name'] = request.POST['first_name']
      request.session['last_name'] = request.POST['last_name']
      request.session['email'] = request.POST['email']
      return redirect('/')
  else:
    pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pwhash)
    request.session['first_name'] = request.POST['first_name']
    request.session['last_name'] = request.POST['last_name']
    return redirect('/dashboard')

def login(request):
  errors = User.objects.loginValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/')
  else:
    request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
    request.session['last_name'] = User.objects.get(email=request.POST['email']).last_name
    request.session['id'] = User.objects.get(email=request.POST['email']).id
    print (request.session['id'])
    return redirect('/dashboard')
  

def success(request):
  currentUser = User.objects.get(id = request.session['id'])

  context = {
    'wishlist' : Wishlist.objects.all(),
    'notliked' : Wishlist.objects.filter(~Q(liked_users=currentUser) & ~Q(added_by=currentUser)),
    'liked' : Wishlist.objects.filter(liked_users = currentUser)
  }
  liked = {}


  return render(request, 'first_app/success.html', context)


def create(request):
  return render(request, 'first_app/create.html')

def createrender(request):
  errors = Wishlist.objects.wish_list_manager(request.POST)
  if (errors):
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/wish_items/create')
  else:
    Wishlist.objects.create(
      name = request.POST['name'],
      added_by = User.objects.get(id=request.session['id'])
    )
    return redirect('/dashboard')
def show(request, itemid):
  x = {
    'item' : Wishlist.objects.get(id=itemid),
    'likedusers' : Wishlist.objects.get(id=itemid).liked_users.all().values('first_name'),
    'uploadedusers' : Wishlist.objects.get(id=itemid).added_by.first_name
  }
  return render(request, 'first_app/info.html', x)

def delete(request, itemid):
  Wishlist.objects.get(id=itemid).delete()
  return redirect('/dashboard')

def remove(request, itemid):
  f = User.objects.get(id=request.session['id'])
  o = f.liked_items.get(id=itemid)
  o.delete()
  o.save()
  print (f)
  return redirect('/dashboard')

def add(request, itemid):
   User.objects.get(id=request.session['id']).liked_items.add(Wishlist.objects.get(id=itemid))
   return redirect('/dashboard')
