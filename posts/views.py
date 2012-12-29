from datetime import *

from google.appengine.api import memcache
from google.appengine.api import users
from django.shortcuts import render, render_to_response, redirect
from models import *

from posts.models import *

PAGESIZE = 20

def default_context():
  return {
      'user': users.get_current_user(),
      'login_url': users.create_login_url('/'),
      'logout_url': users.create_logout_url('/'),
      'error': False,
      }

def index(request):
  q = Post.all().order('-created_at')
  if 'more_created_at' in request.GET:
    q.filter('created_at <=', datetime.fromtimestamp(float(request.GET['more_created_at']) + 1))
  posts = q.fetch(PAGESIZE + 1)
  context = default_context()
  context.update({
    'posts': posts[:PAGESIZE],
    'more_created_at': posts[-1].created_at.strftime('%s') if len(posts) == PAGESIZE + 1 else None
    })
  return render_to_response('posts/index.html', context)

def create(request):
  context = default_context()
  if request.method == 'POST': 
    if request.POST['content'] == '':
      context['error'] = True
    else:
      post = Post(
        content=request.POST['content'],
        user=users.get_current_user()
        )
      post.put()
      return redirect('/')
  return render(request, 'posts/form.html', context)

def show(request):
  return

def update(request):
  return

def delete(request):
  return
