from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product, Category, Inventory, Customer, Supplier


class UserRegistrationForm(UserCreationForm):
    """Form for registering new users"""
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'role']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class ProductForm(forms.ModelForm):
    """Form for creating and updating products"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'barcode', 'purchase_price', 'sale_price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class InventoryForm(forms.ModelForm):
    """Form for updating inventory levels"""
    
    class Meta:
        model = Inventory
        fields = ['quantity', 'min_stock_level', 'max_stock_level']
        

class CustomerForm(forms.ModelForm):
    """Form for creating and updating customers"""
    
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class SupplierForm(forms.ModelForm):
    """Form for creating and updating suppliers"""
    
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        } 