from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Product, Inventory, Customer, Sale

User = get_user_model()

class ModelTestCase(TestCase):
    """Pruebas para los modelos de la aplicación"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123',
            email='test@example.com',
            role='admin'
        )
        
        # Crear categoría
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        
        # Crear producto
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product description',
            category=self.category,
            purchase_price=10.00,
            sale_price=20.00,
            barcode='1234567890'
        )
        
        # Crear inventario
        self.inventory = Inventory.objects.create(
            product=self.product,
            quantity=10,
            min_stock_level=3,
            max_stock_level=20
        )
        
        # Crear cliente
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone='1234567890',
            email='customer@example.com',
            address='Test address'
        )
    
    def test_category_str(self):
        """Probar la representación de cadena de Category"""
        self.assertEqual(str(self.category), 'Test Category')
    
    def test_product_str(self):
        """Probar la representación de cadena de Product"""
        self.assertEqual(str(self.product), 'Test Product')
    
    def test_product_profit_margin(self):
        """Probar el cálculo del margen de beneficio del producto"""
        # El margen debe ser (20 - 10) / 10 * 100 = 100%
        self.assertEqual(self.product.profit_margin, 100.0)
    
    def test_inventory_str(self):
        """Probar la representación de cadena de Inventory"""
        self.assertEqual(str(self.inventory), 'Test Product - 10 unidades')
    
    def test_inventory_is_low_stock(self):
        """Probar la detección de bajo stock"""
        # Inicialmente no está en bajo stock (10 > 3)
        self.assertFalse(self.inventory.is_low_stock)
        
        # Actualizar a bajo stock
        self.inventory.quantity = 2
        self.inventory.save()
        self.assertTrue(self.inventory.is_low_stock)
    
    def test_customer_str(self):
        """Probar la representación de cadena de Customer"""
        self.assertEqual(str(self.customer), 'Test Customer')


class ViewTestCase(TestCase):
    """Pruebas para las vistas de la aplicación"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear cliente HTTP
        self.client = Client()
        
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123',
            email='test@example.com',
            role='admin'
        )
    
    def test_login_view_get(self):
        """Probar la vista de inicio de sesión (GET)"""
        response = self.client.get(reverse('pos:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pos/login.html')
    
    def test_login_view_post_valid(self):
        """Probar inicio de sesión válido"""
        response = self.client.post(
            reverse('pos:login'),
            {'username': 'testuser', 'password': 'password123'},
            follow=True
        )
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('pos:dashboard'))
    
    def test_login_view_post_invalid(self):
        """Probar inicio de sesión inválido"""
        response = self.client.post(
            reverse('pos:login'),
            {'username': 'testuser', 'password': 'wrongpassword'},
            follow=True
        )
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_dashboard_view_authenticated(self):
        """Probar acceso a dashboard cuando está autenticado"""
        # Iniciar sesión
        self.client.login(username='testuser', password='password123')
        
        # Acceder al dashboard
        response = self.client.get(reverse('pos:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pos/dashboard.html')
    
    def test_dashboard_view_unauthenticated(self):
        """Probar redirección cuando no está autenticado"""
        response = self.client.get(reverse('pos:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertIn('login', response.url)  # Verificar que redirige a login


class POSTestCase(TestCase):
    """Pruebas específicas para el sistema de punto de venta"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear cliente HTTP
        self.client = Client()
        
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123',
            email='test@example.com',
            role='admin'
        )
        
        # Iniciar sesión
        self.client.login(username='testuser', password='password123')
        
        # Crear categoría
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        
        # Crear producto
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product description',
            category=self.category,
            purchase_price=10.00,
            sale_price=20.00,
            barcode='1234567890'
        )
        
        # Crear inventario
        self.inventory = Inventory.objects.create(
            product=self.product,
            quantity=10,
            min_stock_level=3,
            max_stock_level=20
        )
        
        # Crear cliente
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone='1234567890',
            email='customer@example.com',
            address='Test address'
        )
    
    def test_point_of_sale_view(self):
        """Probar la vista del punto de venta"""
        response = self.client.get(reverse('pos:point_of_sale'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pos/point_of_sale.html')
        self.assertContains(response, self.product.name)
    
    def test_process_sale(self):
        """Probar el procesamiento de ventas"""
        # Datos de la venta para la prueba
        sale_data = {
            'items': [
                {
                    'product_id': self.product.id,
                    'quantity': 2,
                    'price': float(self.product.sale_price)
                }
            ],
            'customer': '',
            'payment_method': 'cash',
            'notes': 'Test sale'
        }
        
        # Realizar la solicitud POST para procesar la venta
        response = self.client.post(
            reverse('pos:process_sale'),
            data=sale_data,
            content_type='application/json'
        )
        
        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se creó la venta en la base de datos
        self.assertEqual(Sale.objects.count(), 1)
        sale = Sale.objects.first()
        self.assertEqual(sale.user, self.user)
        self.assertEqual(sale.payment_method, 'cash')
        self.assertEqual(sale.notes, 'Test sale')
        
        # Verificar que se crearon los items de venta
        self.assertEqual(sale.saleitem_set.count(), 1)
        sale_item = sale.saleitem_set.first()
        self.assertEqual(sale_item.product, self.product)
        self.assertEqual(sale_item.quantity, 2)
        self.assertEqual(sale_item.price, self.product.sale_price)
        
        # Verificar que se actualizó el inventario
        inventory = Inventory.objects.get(product=self.product)
        self.assertEqual(inventory.quantity, 8)  # 10 inicial - 2 vendidos
