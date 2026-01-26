from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import CustomUser
from .forms import SignUpForm, LoginForm


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)#creates form object with submitted data
        if form.is_valid():#every fields are checked against validation rules
            user = form.save()      #  password hashed automatically
            login(request, user)    #  auto login after signup
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

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
