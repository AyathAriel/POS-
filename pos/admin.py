from django.contrib import admin
from .models import (
    User, Category, Product, Inventory, Supplier, 
    Purchase, PurchaseItem, Customer, Sale, SaleItem
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'barcode', 'purchase_price', 'sale_price', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'barcode', 'description')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'min_stock_level', 'max_stock_level', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('product__name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'created_at')
    search_fields = ('name', 'contact_person', 'email')


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'user', 'date', 'total_amount', 'paid')
    list_filter = ('date', 'paid')
    search_fields = ('supplier__name', 'reference')
    inlines = [PurchaseItemInline]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'email', 'phone')


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'user', 'customer', 'date', 'total', 'payment_method', 'paid')
    list_filter = ('date', 'payment_method', 'paid')
    search_fields = ('invoice_number', 'customer__name')
    inlines = [SaleItemInline]
