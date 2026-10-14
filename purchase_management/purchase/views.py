from django.shortcuts import render, redirect, get_object_or_404
from purchase.models import Supplier, Purchase
from purchase.forms import SupplierForm, PurchaseForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Sum

def login_view(request):
    form_data = AuthenticationForm()
    if request.method == 'POST':
        form_data = AuthenticationForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request, user)
                messages.success(request, 'User Logged-in Successfully.')
                return redirect('dashboard_view')
        
        messages.warning(request,'Invalid Credentials')
    context = {
        'form_data': form_data
    }
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully')
    return redirect('login_view')

@login_required
def dashboard_view(request):

    return render(request, 'dashboard.html')

@login_required
def supplier_list_view(request):
    suppliers = Supplier.objects.filter(user=request.user)
    context = {
        'suppliers': suppliers
    }
    return render(request, 'supplier_list.html', context)

@login_required
def supplier_create_view(request):
    form_data = SupplierForm()
    if request.method == 'POST':
        form_data = SupplierForm(request.POST)
        if form_data.is_valid():
            supplier = form_data.save(commit=False)
            supplier.user = request.user
            supplier.save()
            messages.success(request, 'Supplier Created Successfully.')
            return redirect('supplier_list_view')
        
    context = {
        'form_data': form_data,
        'form_title': 'Create Supplier',
        'form_btn': 'Create'
    }
    return render(request, 'master/base-form.html', context)

@login_required
def supplier_update_view(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, user=request.user)
    form_data = SupplierForm(instance=supplier)
    if request.method == 'POST':
        form_data = SupplierForm(request.POST, instance=supplier)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Supplier Updated Successfully.')
            return redirect('supplier_list_view')
        
    context = {
        'form_data': form_data,
        'form_title': 'Update Supplier',
        'form_btn': 'Update'
    }
    return render(request, 'master/base-form.html', context)

@login_required
def supplier_delete_view(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, user=request.user)
    supplier.delete()
    messages.success(request, 'Supplier Deleted Successfully.')
    return redirect('supplier_list_view')

@login_required
def purchase_list_view(request):
    purchases = Purchase.objects.select_related('supplier').filter(user=request.user)
    context = {
        'purchases': purchases
    }
    return render(request, 'purchase_list.html', context)

@login_required
def purchase_create_view(request):
    form_data = PurchaseForm(user=request.user)
    if request.method == 'POST':
        form_data = PurchaseForm(request.POST, user=request.user)
        if form_data.is_valid():
            purchase = form_data.save(commit=False)
            purchase.user = request.user
            purchase.save()
            messages.success(request, 'Purchase Created Successfully.')
            return redirect('purchase_list_view')

    context = {
        'form_data': form_data,
        'form_title': 'Create Purchase',
        'form_btn': 'Create'
    }
    return render(request, 'master/base-form.html', context)

@login_required
def purchase_update_view(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk, user=request.user)
    form_data = PurchaseForm(instance=purchase, user=request.user)
    if request.method == 'POST':
        form_data = PurchaseForm(request.POST, instance=purchase, user=request.user)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Purchase Updated Successfully.')
            return redirect('purchase_list_view')

    context = {
        'form_data': form_data,
        'form_title': 'Update Purchase',
        'form_btn': 'Update'
    }
    return render(request, 'master/base-form.html', context)

@login_required
def purchase_delete_view(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk, user=request.user)
    purchase.delete()
    messages.success(request, 'Purchase Deleted Successfully.')
    return redirect('purchase_list_view')





