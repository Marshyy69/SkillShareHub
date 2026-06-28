from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import FreelanceGig, Order, Profile
from .forms import GigForm, UserRegisterForm, OrderSubmissionForm


def get_user_role(user):
    """Safely get user role, returns 'buyer' if no profile exists."""
    try:
        return user.profile.role
    except Profile.DoesNotExist:
        return 'buyer'


def seller_required(view_func):
    """Decorator that restricts a view to seller accounts only."""
    def wrapper(request, *args, **kwargs):
        if get_user_role(request.user) != 'seller':
            messages.error(request, 'Access denied. This feature is for sellers only.')
            return redirect('marketplace:home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    wrapper.__doc__ = view_func.__doc__
    return wrapper


# ============================================
# PUBLIC VIEWS
# ============================================

def home(request):
    gigs = FreelanceGig.objects.all().order_by('-created_at')
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    if query:
        gigs = gigs.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if category:
        gigs = gigs.filter(category=category)

    categories = FreelanceGig.CATEGORY_CHOICES
    context = {
        'gigs': gigs,
        'query': query,
        'selected_category': category,
        'categories': categories,
    }
    return render(request, 'marketplace/home.html', context)


def gig_detail(request, gig_id):
    gig = get_object_or_404(FreelanceGig, id=gig_id)
    return render(request, 'marketplace/gig_detail.html', {'gig': gig})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role', 'buyer')
            Profile.objects.create(user=user, role=role)
            login(request, user)
            messages.success(request, f'Welcome to SkillShare Hub, {user.username}!')
            return redirect('marketplace:home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# ============================================
# SELLER-ONLY VIEWS
# ============================================

@login_required
@seller_required
def seller_dashboard(request):
    gigs = FreelanceGig.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'marketplace/seller_dashboard.html', {'gigs': gigs})


@login_required
@seller_required
def create_gig(request):
    if request.method == 'POST':
        form = GigForm(request.POST, request.FILES)
        if form.is_valid():
            gig = form.save(commit=False)
            gig.seller = request.user
            gig.save()
            messages.success(request, 'Your gig has been created!')
            return redirect('marketplace:seller_dashboard')
    else:
        form = GigForm()
    return render(request, 'marketplace/gig_form.html', {'form': form, 'action': 'Create'})


@login_required
@seller_required
def update_gig(request, gig_id):
    gig = get_object_or_404(FreelanceGig, id=gig_id, seller=request.user)
    if request.method == 'POST':
        form = GigForm(request.POST, request.FILES, instance=gig)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your gig has been updated!')
            return redirect('marketplace:seller_dashboard')
    else:
        form = GigForm(instance=gig)
    return render(request, 'marketplace/gig_form.html', {'form': form, 'action': 'Update'})


@login_required
@seller_required
def delete_gig(request, gig_id):
    gig = get_object_or_404(FreelanceGig, id=gig_id, seller=request.user)
    if request.method == 'POST':
        gig.delete()
        messages.success(request, 'Your gig has been deleted.')
        return redirect('marketplace:seller_dashboard')
    return render(request, 'marketplace/gig_confirm_delete.html', {'gig': gig})


@login_required
@seller_required
def seller_orders(request):
    orders = Order.objects.filter(gig__seller=request.user).order_by('-date_ordered')
    return render(request, 'marketplace/seller_orders.html', {'orders': orders})


@login_required
@seller_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, gig__seller=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}.')
    return redirect('marketplace:seller_orders')


@login_required
@seller_required
def submit_work(request, order_id):
    order = get_object_or_404(Order, id=order_id, gig__seller=request.user)
    if order.status not in ['progress', 'delivered']:
        messages.error(request, 'You can only submit work for orders that are In Progress.')
        return redirect('marketplace:seller_orders')

    if request.method == 'POST':
        form = OrderSubmissionForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.status = 'delivered'
            submission.date_submitted = timezone.now()
            submission.save()
            messages.success(request, f'Work for Order #{order.id} has been delivered to the buyer!')
            return redirect('marketplace:seller_orders')
    else:
        form = OrderSubmissionForm(instance=order)
    
    return render(request, 'marketplace/submit_work_form.html', {'form': form, 'order': order})


# ============================================
# BUYER VIEWS
# ============================================

@login_required
def order_gig(request, gig_id):
    gig = get_object_or_404(FreelanceGig, id=gig_id)

    # Sellers cannot buy gigs
    if get_user_role(request.user) == 'seller':
        messages.error(request, 'Sellers cannot place orders. Register as a buyer to purchase services.')
        return redirect('marketplace:gig_detail', gig_id=gig.id)

    if gig.seller == request.user:
        messages.error(request, 'You cannot order your own gig.')
        return redirect('marketplace:gig_detail', gig_id=gig.id)

    if request.method == 'POST':
        requirements = request.POST.get('requirements', '').strip()
        Order.objects.create(gig=gig, buyer=request.user, requirements=requirements)
        messages.success(request, f'Order placed for "{gig.title}"! The seller will review your requirements.')
        return redirect('marketplace:my_orders')

    # GET — show the order confirmation / requirements form
    return render(request, 'marketplace/order_form.html', {'gig': gig})


@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-date_ordered')
    return render(request, 'marketplace/my_orders.html', {'orders': orders})


@login_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    if order.status != 'delivered':
        messages.error(request, 'This order cannot be marked as completed yet.')
        return redirect('marketplace:my_orders')

    if request.method == 'POST':
        order.status = 'completed'
        order.save()
        messages.success(request, f'Order #{order.id} marked as completed! Thank you.')
    return redirect('marketplace:my_orders')

