from django.core.management.base import BaseCommand
from pos.models import Category, Product, Inventory, Customer, Supplier

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para el sistema POS'

    def handle(self, *args, **options):
        # Crear categorías
        categories = [
            {'name': 'Electrónicos', 'description': 'Productos electrónicos y gadgets'},
            {'name': 'Alimentos', 'description': 'Comida y bebidas'},
            {'name': 'Ropa', 'description': 'Prendas de vestir y accesorios'},
            {'name': 'Hogar', 'description': 'Artículos para el hogar'},
        ]
        
        created_categories = []
        for cat_data in categories:
            category, created = Category.objects.get_or_create(**cat_data)
            created_categories.append(category)
            status = 'creada' if created else 'ya existía'
            self.stdout.write(f"Categoría '{category.name}' {status}")
        
        # Crear productos
        products = [
            {
                'name': 'Smartphone XYZ', 
                'description': 'Smartphone de última generación', 
                'category': created_categories[0], 
                'purchase_price': 300, 
                'sale_price': 499.99,
                'barcode': '1234567890123'
            },
            {
                'name': 'Tablet Pro', 
                'description': 'Tablet de 10 pulgadas', 
                'category': created_categories[0], 
                'purchase_price': 200, 
                'sale_price': 349.99,
                'barcode': '1234567890124'
            },
            {
                'name': 'Agua Mineral 1L', 
                'description': 'Botella de agua mineral', 
                'category': created_categories[1], 
                'purchase_price': 0.50, 
                'sale_price': 1.20,
                'barcode': '1234567890125'
            },
            {
                'name': 'Chocolate Premium', 
                'description': 'Barra de chocolate premium', 
                'category': created_categories[1], 
                'purchase_price': 1.20, 
                'sale_price': 2.50,
                'barcode': '1234567890126'
            },
            {
                'name': 'Camiseta Algodón', 
                'description': 'Camiseta 100% algodón', 
                'category': created_categories[2], 
                'purchase_price': 5, 
                'sale_price': 15.99,
                'barcode': '1234567890127'
            },
            {
                'name': 'Jeans Classic', 
                'description': 'Pantalones vaqueros clásicos', 
                'category': created_categories[2], 
                'purchase_price': 15, 
                'sale_price': 39.99,
                'barcode': '1234567890128'
            },
            {
                'name': 'Lámpara LED', 
                'description': 'Lámpara de escritorio LED', 
                'category': created_categories[3], 
                'purchase_price': 12, 
                'sale_price': 24.99,
                'barcode': '1234567890129'
            },
            {
                'name': 'Juego de Sábanas', 
                'description': 'Juego de sábanas de algodón', 
                'category': created_categories[3], 
                'purchase_price': 20, 
                'sale_price': 45.99,
                'barcode': '1234567890130'
            },
        ]
        
        for prod_data in products:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults=prod_data
            )
            
            # Crear o actualizar inventario
            inventory, inv_created = Inventory.objects.get_or_create(
                product=product,
                defaults={
                    'quantity': 10,
                    'min_stock_level': 3,
                    'max_stock_level': 20
                }
            )
            
            status = 'creado' if created else 'ya existía'
            self.stdout.write(f"Producto '{product.name}' {status} con {inventory.quantity} unidades")
        
        # Crear clientes
        customers = [
            {
                'name': 'Cliente General',
                'phone': '555-0000',
                'email': 'cliente@example.com',
                'address': 'Dirección genérica 123'
            },
            {
                'name': 'Juan Pérez',
                'phone': '555-1111',
                'email': 'juan@example.com',
                'address': 'Calle Principal 456'
            },
            {
                'name': 'María López',
                'phone': '555-2222',
                'email': 'maria@example.com',
                'address': 'Avenida Central 789'
            },
        ]
        
        for cust_data in customers:
            customer, created = Customer.objects.get_or_create(
                name=cust_data['name'],
                defaults=cust_data
            )
            
            status = 'creado' if created else 'ya existía'
            self.stdout.write(f"Cliente '{customer.name}' {status}")
        
        # Crear proveedores
        suppliers = [
            {
                'name': 'Electrónicos Distribuidor',
                'contact_person': 'Carlos Rodríguez',
                'phone': '555-3333',
                'email': 'distribuidor@example.com',
                'address': 'Calle Industria 101'
            },
            {
                'name': 'Alimentos Mayorista',
                'contact_person': 'Ana Gómez',
                'phone': '555-4444',
                'email': 'mayorista@example.com',
                'address': 'Avenida Comercio 202'
            },
        ]
        
        for supp_data in suppliers:
            supplier, created = Supplier.objects.get_or_create(
                name=supp_data['name'],
                defaults=supp_data
            )
            
            status = 'creado' if created else 'ya existía'
            self.stdout.write(f"Proveedor '{supplier.name}' {status}")
        
        self.stdout.write(self.style.SUCCESS('Datos de ejemplo creados con éxito')) 