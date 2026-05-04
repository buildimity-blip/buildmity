from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobCreateForm
from .models import Job


@login_required
def create_job(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobCreateForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            return redirect('my_jobs')
    else:
        form = JobCreateForm()

    return render(request, 'create_job.html', {'form': form})


@login_required
def my_jobs(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    jobs = Job.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'my_jobs.html', {'jobs': jobs})


@login_required
def available_jobs(request):
    if request.user.role != 'provider':
        return redirect('dashboard')

    jobs = Job.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'available_jobs.html', {'jobs': jobs})


@login_required
def assign_job(request, job_id):
    if request.user.role != 'provider':
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id, status='pending')
    job.assigned_provider = request.user
    job.status = 'assigned'
    job.save()

    return redirect('available_jobs')


@login_required
def assigned_jobs(request):
    if request.user.role != 'provider':
        return redirect('dashboard')

    jobs = Job.objects.filter(assigned_provider=request.user).order_by('-created_at')
    return render(request, 'assigned_jobs.html', {'jobs': jobs})