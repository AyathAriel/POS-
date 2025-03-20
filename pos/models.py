from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Extended user model with additional fields for POS system"""
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Administrador'),
        ('cashier', 'Cajero'),
        ('inventory', 'Inventario'),
    ], default='cashier')
    
    def __str__(self):
        return self.username


class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Products available for sale"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    barcode = models.CharField(max_length=50, blank=True, null=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return self.name
    
    @property
    def current_stock(self):
        """Get current stock quantity"""
        inventory = self.inventory_set.first()
        return inventory.quantity if inventory else 0
    
    @property
    def profit_margin(self):
        """Calculate profit margin"""
        if self.purchase_price > 0:
            return ((self.sale_price - self.purchase_price) / self.purchase_price) * 100
        return 0


class Inventory(models.Model):
    """Inventory management for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5)
    max_stock_level = models.PositiveIntegerField(default=100)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"
    
    @property
    def is_low_stock(self):
        """Check if product is low in stock"""
        return self.quantity <= self.min_stock_level


class Supplier(models.Model):
    """Suppliers for product inventory"""
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
    
    def __str__(self):
        return self.name


class Purchase(models.Model):
    """Purchase orders from suppliers"""
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
    
    def __str__(self):
        return f"Compra #{self.id} - {self.supplier.name}"
    
    def update_total(self):
        """Update total amount based on purchase items"""
        self.total_amount = sum(item.subtotal for item in self.purchaseitem_set.all())
        self.save()


class PurchaseItem(models.Model):
    """Items in a purchase order"""
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Item de Compra"
        verbose_name_plural = "Items de Compra"
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update inventory
        inventory, created = Inventory.objects.get_or_create(product=self.product)
        inventory.quantity += self.quantity
        inventory.save()
        # Update purchase total
        self.purchase.update_total()


class Customer(models.Model):
    """Customer information for sales"""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def __str__(self):
        return self.name


class Sale(models.Model):
    """Sales transaction"""
    PAYMENT_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    paid = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
    
    def __str__(self):
        return f"Venta #{self.invoice_number}"
    
    def save(self, *args, **kwargs):
        # Generate invoice number if not set
        if not self.invoice_number:
            last_invoice = Sale.objects.order_by('-id').first()
            invoice_num = 1
            if last_invoice:
                invoice_num = last_invoice.id + 1
            self.invoice_number = f"INV-{timezone.now().strftime('%Y%m%d')}-{invoice_num:04d}"
        super().save(*args, **kwargs)
    
    def update_total(self):
        """Update total amount based on sale items"""
        self.total = sum(item.subtotal for item in self.saleitem_set.all())
        self.save()


class SaleItem(models.Model):
    """Items in a sale"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Item de Venta"
        verbose_name_plural = "Items de Venta"
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        # Set price from product if not specified
        if not self.price or self.price == 0:
            self.price = self.product.sale_price
            
        super().save(*args, **kwargs)
        
        # Update inventory
        inventory, created = Inventory.objects.get_or_create(product=self.product)
        inventory.quantity = max(0, inventory.quantity - self.quantity)
        inventory.save()
        
        # Update sale total
        self.sale.update_total()
