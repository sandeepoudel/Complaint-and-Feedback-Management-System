from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import CustomUser, Complaint, StatusHistory
from .forms import SignUpForm, LoginForm, ComplaintForm, StatusUpdateForm


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)#creates form object with submitted data
        if form.is_valid():#every fields are checked against validation rules
            user = form.save()      #  password hashed automatically
            login(request, user)    #  auto login after signup
            return redirect("user_dashboard")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("user_dashboard")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

<<<<<<< HEAD

# Helper function to check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_admin


# User Complaint Views
@login_required
def complaint_list_view(request):
    """Display user's complaints with filtering and pagination"""
    complaints = Complaint.objects.filter(user=request.user)
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter and status_filter in dict(Complaint.STATUS_CHOICES):
        complaints = complaints.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        complaints = complaints.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(complaints, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': Complaint.STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search_query,
    }
    return render(request, 'complaints/complaint_list.html', context)


@login_required
def complaint_detail_view(request, complaint_id):
    """Display individual complaint details"""
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    status_history = complaint.status_history.all()
    
    context = {
        'complaint': complaint,
        'status_history': status_history,
        'can_edit': complaint.can_be_edited(),
    }
    return render(request, 'complaints/complaint_detail.html', context)


@login_required
def complaint_create_view(request):
    """Handle complaint creation"""
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            
            # Create initial status history
            StatusHistory.objects.create(
                complaint=complaint,
                old_status='',
                new_status='open',
                changed_by=request.user,
                notes='Complaint created'
            )
            
            messages.success(request, 'Your complaint has been submitted successfully!')
            return redirect('complaint_detail', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/complaint_form.html', {'form': form, 'action': 'Create'})


@login_required
def complaint_update_view(request, complaint_id):
    """Handle complaint editing with restrictions"""
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    
    if not complaint.can_be_edited():
        messages.error(request, 'This complaint cannot be edited as it has been resolved.')
        return redirect('complaint_detail', complaint_id=complaint.id)
    
=======
def home_view(request):
    return render(request, "home.html")


from django.shortcuts import render, get_object_or_404, redirect
from .models import Complaint
from .forms import ComplaintForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# READ – list of complaints
def complaint_list(request):
    complaint_list = Complaint.objects.all()
    paginator = Paginator(complaint_list, 5)  # 5 complaints per page

    page_number = request.GET.get('page')
    complaints = paginator.get_page(page_number)

    return render(request, 'complaint_list.html', {
        'complaints': complaints
    })

# READ – detail of a single complaint
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, "complaint_detail.html", {"complaint": complaint})

# CREATE – complaint submission (requires login)
@login_required
def submit_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            # Associate the complaint with the logged-in user
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()

            return redirect('complaint_list')  # Redirect to the complaint list after successful submission
    else:
        form = ComplaintForm()

    return render(request, 'submit_complaint.html', {'form': form})

# UPDATE – update complaint status by admin (requires login)
@login_required
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    if request.method == "POST":
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('complaint_detail', pk=complaint.pk)
    else:
        form = ComplaintForm(instance=complaint)

    return render(request, 'update_complaint.html', {'form': form, 'complaint': complaint})

from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'message', 'email']
    
    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        # Add form-control class to fields
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

@login_required
def edit_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    # Check if the complaint is resolved, if yes, prevent editing
    if complaint.is_resolved:
        return redirect('complaint_detail', pk=complaint.pk)

>>>>>>> origin/main
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            messages.success(request, 'Your complaint has been updated successfully!')
            return redirect('complaint_detail', complaint_id=complaint.id)
    else:
        form = ComplaintForm(instance=complaint)
    
    return render(request, 'complaints/complaint_form.html', {
        'form': form, 
        'complaint': complaint,
        'action': 'Update'
    })


@login_required
def user_dashboard_view(request):
    """User's main complaint dashboard"""
    user_complaints = Complaint.objects.filter(user=request.user)
    
    # Statistics
    total_complaints = user_complaints.count()
    open_complaints = user_complaints.filter(status='open').count()
    in_progress_complaints = user_complaints.filter(status='in_progress').count()
    resolved_complaints = user_complaints.filter(status='resolved').count()
    
    # Recent complaints
    recent_complaints = user_complaints[:5]
    
    context = {
        'total_complaints': total_complaints,
        'open_complaints': open_complaints,
        'in_progress_complaints': in_progress_complaints,
        'resolved_complaints': resolved_complaints,
        'recent_complaints': recent_complaints,
    }
    return render(request, 'complaints/user_dashboard.html', context)


# Admin Views
@user_passes_test(is_admin)
def admin_complaint_list_view(request):
    """Display all complaints for admin with filtering"""
    complaints = Complaint.objects.all()
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter and status_filter in dict(Complaint.STATUS_CHOICES):
        complaints = complaints.filter(status=status_filter)
    
    # Filter by user
    user_filter = request.GET.get('user')
    if user_filter:
        complaints = complaints.filter(user__username__icontains=user_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        complaints = complaints.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(complaints, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': Complaint.STATUS_CHOICES,
        'current_status': status_filter,
        'current_user': user_filter,
        'search_query': search_query,
    }
    return render(request, 'complaints/admin_complaint_list.html', context)


@user_passes_test(is_admin)
def admin_complaint_detail_view(request, complaint_id):
    """Admin view for complaint details with status management"""
    complaint = get_object_or_404(Complaint, id=complaint_id)
    status_history = complaint.status_history.all()
    
    context = {
        'complaint': complaint,
        'status_history': status_history,
    }
    return render(request, 'complaints/admin_complaint_detail.html', context)


@user_passes_test(is_admin)
def complaint_status_update_view(request, complaint_id):
    """Handle status updates by admin"""
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            old_status = complaint.status
            new_status = form.cleaned_data['status']
            notes = form.cleaned_data['notes']
            
            # Update complaint status
            complaint.status = new_status
            if new_status == 'resolved':
                complaint.resolved_by = request.user
                complaint.resolved_at = timezone.now()
            complaint.save()
            
            # Create status history record
            StatusHistory.objects.create(
                complaint=complaint,
                old_status=old_status,
                new_status=new_status,
                changed_by=request.user,
                notes=notes
            )
            
            messages.success(request, f'Complaint status updated to {complaint.get_status_display()}')
            return redirect('admin_complaint_detail', complaint_id=complaint.id)
    else:
        form = StatusUpdateForm(initial={'status': complaint.status})
    
    return render(request, 'complaints/status_update.html', {
        'form': form,
        'complaint': complaint
    })


@user_passes_test(is_admin)
def complaint_delete_view(request, complaint_id):
    """Handle complaint deletion with confirmation"""
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        complaint_title = complaint.title
        complaint.delete()
        messages.success(request, f'Complaint "{complaint_title}" has been deleted successfully.')
        return redirect('admin_complaint_list')
    
    return render(request, 'complaints/complaint_delete_confirm.html', {'complaint': complaint})


@user_passes_test(is_admin)
def admin_dashboard_view(request):
    """Administrative dashboard with system statistics"""
    all_complaints = Complaint.objects.all()
    
    # Statistics
    total_complaints = all_complaints.count()
    open_complaints = all_complaints.filter(status='open').count()
    in_progress_complaints = all_complaints.filter(status='in_progress').count()
    resolved_complaints = all_complaints.filter(status='resolved').count()
    
    # Recent complaints
    recent_complaints = all_complaints[:10]
    
    # Recent status changes
    recent_status_changes = StatusHistory.objects.all()[:10]
    
    context = {
        'total_complaints': total_complaints,
        'open_complaints': open_complaints,
        'in_progress_complaints': in_progress_complaints,
        'resolved_complaints': resolved_complaints,
        'recent_complaints': recent_complaints,
        'recent_status_changes': recent_status_changes,
    }
    return render(request, 'complaints/admin_dashboard.html', context)

@login_required
def user_detail_view(request, pk):
    """Simple user detail view"""
    user = get_object_or_404(CustomUser, pk=pk)
    if request.user != user and not request.user.is_admin:
        messages.error(request, 'You can only view your own profile.')
        return redirect('user_dashboard')
    
    context = {'profile_user': user}
    return render(request, 'user_detail.html', context)
=======
            return redirect('complaint_detail', pk=complaint.pk)
    else:
        form = ComplaintForm(instance=complaint)

    return render(request, 'edit_complaint.html', {'form': form, 'complaint': complaint})
>>>>>>> origin/main
