from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout


def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
  else:
    # 初期化されたフォームがレンダリングされる
    form = UserCreationForm()
  return render(request, 'signup.html', {'form':form})
    
def logoutfunc(request):
  logout(request)
  return redirect('home')