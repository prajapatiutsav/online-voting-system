from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count

from .models import Candidate, Vote, ElectionControl


# 🏠 HOME
def home(request):
    return render(request, 'home.html')


# 📝 REGISTER
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already used'})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'register.html')


# 🔐 LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# 🚪 LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# 🗳️ VOTE
@login_required
def vote(request):
    control = ElectionControl.objects.first()

    # ⛔ Voting closed
    if control and control.end_time and timezone.now() > control.end_time:
        return render(request, 'voting_closed.html')

    # 🚫 Prevent double vote
    if Vote.objects.filter(user=request.user).exists():
        return render(request, 'already_voted.html')

    candidates = Candidate.objects.all()

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')

        if not candidate_id:
            return redirect('vote')

        candidate = Candidate.objects.get(id=candidate_id)
        Vote.objects.create(user=request.user, candidate=candidate)

        return redirect('success')

    return render(request, 'vote.html', {
        'candidates': candidates,
        'end_time': control.end_time if control else None
    })


# ✅ SUCCESS
def success(request):
    return render(request, 'success.html')


# 📊 RESULTS
@login_required
def results(request):
    control = ElectionControl.objects.first()

    if not control or (control.end_time and timezone.now() < control.end_time):
        return render(request, 'results_locked.html')

    if not control.show_results:
        return render(request, 'results_locked.html')

    candidates = Candidate.objects.annotate(
        total_votes=Count('vote')
    ).order_by('-total_votes')

    total_votes = sum(c.total_votes for c in candidates)

    for c in candidates:
        if total_votes > 0:
            c.percentage = round((c.total_votes / total_votes) * 100, 2)
        else:
            c.percentage = 0

    winner = candidates.first()

    return render(request, 'results.html', {
        'candidates': candidates,
        'winner': winner,
        'total_votes': total_votes
    })
