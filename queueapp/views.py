from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Business, Queue, Ticket
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .forms import BusinessForm
from .forms import QueueForm
from .forms import QueueParticipantForm  # ✅ Add this import
from .models import QueueParticipant  # Add this line
from django.contrib.auth import get_backends
from django.contrib.auth.forms import AuthenticationForm



def custom_logout(request):
    logout(request)
    return redirect('home')  
def home(request):
    return render(request, 'queueapp/home.html')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # ✅ Explicitly set authentication backend
            backend = get_backends()[0]  # Get the first authentication backend
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'queueapp/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # ✅ Correct way to get the user
            login(request, user)  # ✅ Pass both request & user
            return redirect('dashboard')  # Change to your actual dashboard URL
    else:
        form = AuthenticationForm()
    
    return render(request, 'queueapp/login.html', {'form': form})
@login_required
def dashboard(request):
    businesses =  Business.objects.filter(owner=request.user)
    print(businesses)
    return render(request, 'queueapp/dashboard.html', {'businesses': businesses})
@login_required  
def business_detail(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    queues = business.queues.all()
    print(queues)
    return render(request, 'queueapp/business_detail.html', {'business': business, 'queues': queues})

def join_queue(request, queue_id):
    queue = get_object_or_404(Queue, id=queue_id)

    if request.method == "POST":
        form = QueueParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.queue = queue

            # Assign position dynamically
            last_position = QueueParticipant.objects.filter(queue=queue, served=False).count()
            participant.position = last_position + 1  
            participant.save()

            # **Send email if position < 5**
            if participant.position < 5:
                send_mail(
                    "Your Turn is Near!",
                    f"Hello {participant.name}, your queue position is now {participant.position}. Please be ready!",
                    "noreply@queueapp.com",
                    [participant.email],
                    fail_silently=False,
                )

            return redirect('queue_detail', queue_id=queue.id)

    else:
        form = QueueParticipantForm()

    return render(request, 'queueapp/join_queue.html', {'form': form, 'queue': queue})
@login_required 
def queue_detail(request, queue_id):
    queue = get_object_or_404(Queue, id=queue_id)
    participants = queue.participants.all().order_by('position')
    return render(request, 'queueapp/queue_detail.html', {'queue': queue, 'participants': participants})
@login_required    
def create_queue(request, business_id):
    business = get_object_or_404(Business, id=business_id)

    if request.method == "POST":
        form = QueueForm(request.POST)
        if form.is_valid():
            queue = form.save(commit=False)
            queue.business = business
            queue.save()  # This triggers QR code generation
            
            return redirect('view_qr', queue.id)  # Redirect to QR view page

    else:
        form = QueueForm()
    
    return render(request, 'queueapp/create_queue.html', {'form': form, 'business': business})

def view_qr(request, queue_id):
    queue = get_object_or_404(Queue, id=queue_id)
    return render(request, 'queueapp/view_qr.html', {'queue': queue})

def queue_success(request, queue_id, participant_id):
    participant = get_object_or_404(QueueParticipant, id=participant_id)
    return render(request, "queueapp/queue_success.html", {"participant": participant})


def join_queue(request, queue_id):
    queue = get_object_or_404(Queue, id=queue_id)

    if request.method == "POST":
        form = QueueParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.queue = queue
            participant.position = QueueParticipant.objects.filter(queue=queue).count() + 1
            participant.save()
            return redirect("queue_success", queue_id=queue.id, participant_id=participant.id)

    else:
        form = QueueParticipantForm()

    return render(request, "queueapp/join_queue.html", {"queue": queue, "form": form})
@login_required
def create_queue(request):
    business = Business.objects.filter(owner=request.user).first()
    
    if not business:
        return redirect('register_business')  # Ensure only registered businesses can create queues
    
    if request.method == 'POST':
        form = QueueForm(request.POST)
        if form.is_valid():
            queue = form.save(commit=False)
            queue.business = business  # Associate queue with logged-in user's business
            queue.save()
            return redirect('dashboard')  # Redirect to dashboard after creation
    else:
        form = QueueForm()
    
    return render(request, 'queueapp/create_queue.html', {'form': form})
@login_required
def register_business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            return redirect('dashboard')
    else:
        form = BusinessForm()
    return render(request, 'queueapp/register_business.html', {'form': form})

def complete_participant(request, participant_id):
    participant = get_object_or_404(QueueParticipant, id=participant_id)

    # Mark as served
    participant.served = True
    participant.save()

    # Update positions of remaining participants
    remaining_participants = QueueParticipant.objects.filter(queue=participant.queue, served=False).order_by('position')

    # Reassign positions
    for index, p in enumerate(remaining_participants):
        p.position = index + 1
        p.save()

    return redirect('business_detail', business_id=participant.queue.business.id)