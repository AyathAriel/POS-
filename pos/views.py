from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum, Count, F, DecimalField
from django.db.models.functions import TruncDate
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from .models import (
    Product, Category, Inventory, Sale, SaleItem, 
    Customer, Supplier, Purchase, PurchaseItem, User
)


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('pos:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pos:dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'pos/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect('pos:login')


@login_required
def dashboard(request):
    """Dashboard view with sales statistics"""
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    
    # Today's sales
    today_sales_data = Sale.objects.filter(date__date=today).aggregate(
        total=Sum('total'),
        count=Count('id')
    )
    
    # Month's sales
    month_sales_data = Sale.objects.filter(date__date__gte=first_day_of_month).aggregate(
        total=Sum('total'),
        count=Count('id')
    )
    
    # Low stock products
    low_stock_products = Inventory.objects.filter(
        quantity__lte=F('min_stock_level')
    ).select_related('product', 'product__category')[:5]
    
    # Recent sales
    recent_sales = Sale.objects.select_related('customer').order_by('-date')[:10]
    
    # Total products
    total_products = Product.objects.count()
    
    # Sales chart data (last 7 days)
    end_date = today
    start_date = end_date - datetime.timedelta(days=6)
    
    daily_sales = Sale.objects.filter(
        date__date__gte=start_date,
        date__date__lte=end_date
    ).annotate(
        day=TruncDate('date')
    ).values('day').annotate(
        daily_total=Sum('total', output_field=DecimalField())
    ).order_by('day')
    
    # Prepare data for chart
    days_labels = []
    sales_data = []
    
    current_date = start_date
    while current_date <= end_date:
        days_labels.append(current_date.strftime('%d/%m'))
        
        # Find sales for this day
        day_sale = next((item for item in daily_sales if item['day'] == current_date), None)
        sales_data.append(float(day_sale['daily_total']) if day_sale else 0)
        
        current_date += datetime.timedelta(days=1)
    
    context = {
        'today_sales': today_sales_data['total'] or 0,
        'today_sales_count': today_sales_data['count'] or 0,
        'month_sales': month_sales_data['total'] or 0,
        'month_sales_count': month_sales_data['count'] or 0,
        'low_stock_count': Inventory.objects.filter(quantity__lte=F('min_stock_level')).count(),
        'low_stock_products': low_stock_products,
        'recent_sales': recent_sales,
        'total_products': total_products,
        'days_labels': json.dumps(days_labels),
        'sales_data': json.dumps(sales_data),
    }
    
    return render(request, 'pos/dashboard.html', context)


@login_required
def product_list(request):
    """List all products"""
    products = Product.objects.select_related('category').all()
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
    }
    
    return render(request, 'pos/product_list.html', context)


@login_required
def product_create(request):
    """Create a new product"""
    if request.method == 'POST':
        # Process form data and create product
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        purchase_price = request.POST.get('purchase_price')
        sale_price = request.POST.get('sale_price')
        barcode = request.POST.get('barcode')
        
        category = None
        if category_id:
            category = get_object_or_404(Category, id=category_id)
        
        product = Product.objects.create(
            name=name,
            description=description,
            category=category,
            purchase_price=purchase_price,
            sale_price=sale_price,
            barcode=barcode
        )
        
        # Handle product image if uploaded
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save()
        
        # Create initial inventory
        Inventory.objects.create(product=product, quantity=0)
        
        messages.success(request, f'Producto "{product.name}" creado con éxito!')
        return redirect('pos:product_list')
    
    context = {
        'categories': Category.objects.all(),
    }
    
    return render(request, 'pos/product_form.html', context)


@login_required
def product_edit(request, pk):
    """Edit an existing product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # Process form data and update product
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        
        category_id = request.POST.get('category')
        if category_id:
            product.category = get_object_or_404(Category, id=category_id)
        else:
            product.category = None
        
        product.purchase_price = request.POST.get('purchase_price')
        product.sale_price = request.POST.get('sale_price')
        product.barcode = request.POST.get('barcode')
        
        # Handle product image if uploaded
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        
        messages.success(request, f'Producto "{product.name}" actualizado con éxito!')
        return redirect('pos:product_list')
    
    context = {
        'product': product,
        'categories': Category.objects.all(),
    }
    
    return render(request, 'pos/product_form.html', context)


@login_required
def product_delete(request, pk):
    """Delete a product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Producto "{product_name}" eliminado con éxito!')
        return redirect('pos:product_list')
    
    context = {
        'product': product,
    }
    
    return render(request, 'pos/product_confirm_delete.html', context)


@login_required
def inventory_list(request):
    """List inventory items"""
    low_stock = request.GET.get('low_stock')
    
    inventory = Inventory.objects.select_related('product', 'product__category')
    
    if low_stock:
        inventory = inventory.filter(quantity__lte=F('min_stock_level'))
    
    context = {
        'inventory': inventory,
        'low_stock_filter': low_stock,
    }
    
    return render(request, 'pos/inventory_list.html', context)


@login_required
def inventory_edit(request, pk):
    """Edit inventory levels"""
    inventory = get_object_or_404(Inventory, pk=pk)
    
    if request.method == 'POST':
        inventory.quantity = request.POST.get('quantity')
        inventory.min_stock_level = request.POST.get('min_stock_level')
        inventory.max_stock_level = request.POST.get('max_stock_level')
        inventory.save()
        
        messages.success(request, f'Inventario de "{inventory.product.name}" actualizado con éxito!')
        return redirect('pos:inventory_list')
    
    context = {
        'inventory': inventory,
    }
    
    return render(request, 'pos/inventory_form.html', context)


@login_required
def point_of_sale(request):
    """Point of sale interface"""
    products = Product.objects.select_related('category').all()
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'customers': Customer.objects.all(),
    }
    
    return render(request, 'pos/point_of_sale.html', context)


@login_required
@require_POST
@csrf_exempt
def process_sale(request):
    """Process a sale transaction"""
    try:
        # Intenta analizar los datos como JSON
        data = json.loads(request.body)
    except json.JSONDecodeError:
        # Si no es JSON, usa POST directamente
        data = request.POST.dict()
    
    # Create the sale
    sale = Sale.objects.create(
        user=request.user,
        payment_method=data.get('payment_method', 'cash'),
        notes=data.get('notes', ''),
        total=0  # Will be updated by the signal
    )
    
    # Add customer if provided
    customer_id = data.get('customer')
    if customer_id:
        sale.customer = get_object_or_404(Customer, id=customer_id)
        sale.save()
    
    # Process sale items
    items = data.get('items', [])
    if isinstance(items, str):
        items = json.loads(items)
        
    for item in items:
        product = get_object_or_404(Product, id=item['product_id'])
        
        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=item['quantity'],
            price=item['price']
        )
    
    # Return sale data
    return JsonResponse({
        'status': 'success',
        'sale_id': sale.id,
        'invoice_number': sale.invoice_number,
    })


@login_required
def sale_list(request):
    """List all sales"""
    sales = Sale.objects.select_related('customer', 'user').order_by('-date')
    
    context = {
        'sales': sales,
    }
    
    return render(request, 'pos/sale_list.html', context)


@login_required
def sale_detail(request, pk):
    """View details of a sale"""
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.saleitem_set.select_related('product')
    
    context = {
        'sale': sale,
        'items': items,
    }
    
    return render(request, 'pos/sale_detail.html', context)


@login_required
def customer_list(request):
    """List all customers"""
    customers = Customer.objects.all()
    
    context = {
        'customers': customers,
    }
    
    return render(request, 'pos/customer_list.html', context)


@login_required
def customer_create(request):
    """Create a new customer"""
    if request.method == 'POST':
        customer = Customer.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address')
        )
        
        messages.success(request, f'Cliente "{customer.name}" creado con éxito!')
        return redirect('pos:customer_list')
    
    return render(request, 'pos/customer_form.html')


@login_required
def customer_edit(request, pk):
    """Edit an existing customer"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.address = request.POST.get('address')
        customer.save()
        
        messages.success(request, f'Cliente "{customer.name}" actualizado con éxito!')
        return redirect('pos:customer_list')
    
    context = {
        'customer': customer,
    }
    
    return render(request, 'pos/customer_form.html', context)


@login_required
def supplier_list(request):
    """List all suppliers"""
    suppliers = Supplier.objects.all()
    
    context = {
        'suppliers': suppliers,
    }
    
    return render(request, 'pos/supplier_list.html', context)


@login_required
def purchase_list(request):
    """List all purchases"""
    purchases = Purchase.objects.select_related('supplier', 'user').order_by('-date')
    
    context = {
        'purchases': purchases,
    }
    
    return render(request, 'pos/purchase_list.html', context)


@login_required
def user_list(request):
    """List all users (admin only)"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('pos:dashboard')
    
    users = User.objects.all()
    
    context = {
        'users': users,
    }
    
    return render(request, 'pos/user_list.html', context)


@login_required
def reports(request):
    """Sales and inventory reports view"""
    # To be implemented
    return render(request, 'pos/reports.html')
