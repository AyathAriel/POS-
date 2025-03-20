# Sistema POS (Point of Sale)

Sistema de Punto de Venta desarrollado con Django, diseñado para gestionar ventas, inventario, compras y reportes de manera eficiente.

## Características Principales

### Gestión de Inventario
- Panel de control con estadísticas en tiempo real:
  - Total de productos
  - Valor total del inventario
  - Alertas de stock bajo
  - Número de categorías
- Gestión completa de productos:
  - Registro y edición de productos
  - Control de stock con alertas
  - Imágenes de productos
  - Códigos de producto
  - Precios de compra y venta
- Funciones avanzadas:
  - Importación/Exportación de productos (CSV/Excel)
  - Ajustes de inventario con registro de motivos
  - Historial de movimientos
  - Filtros y búsqueda avanzada
  - Categorización de productos

### Gestión de Ventas
- Proceso de venta intuitivo
- Carrito de compras dinámico
- Múltiples formas de pago
- Descuentos y promociones
- Impresión de recibos
- Cancelación de ventas con registro de motivos
- Historial de ventas por cliente

### Gestión de Compras
- Registro de compras a proveedores
- Control de facturas y pagos
- Actualización automática de inventario
- Historial de compras por proveedor
- Registro de devoluciones

### Gestión de Proveedores
- Registro completo de proveedores
- Historial de transacciones
- Información de contacto
- Estado de cuenta
- Registro de productos por proveedor

### Gestión de Clientes
- Base de datos de clientes
- Historial de compras
- Información de contacto
- Límites de crédito
- Saldos pendientes

### Reportes y Estadísticas
- Reportes de ventas:
  - Diarios
  - Semanales
  - Mensuales
  - Por período personalizado
- Reportes de inventario:
  - Productos más vendidos
  - Stock bajo
  - Valorización de inventario
- Reportes financieros:
  - Balance de ventas
  - Ganancias y pérdidas
  - Flujo de caja
- Exportación de reportes en múltiples formatos

### Gestión de Usuarios
- Roles y permisos:
  - Administrador
  - Vendedor
  - Almacenista
- Registro de actividades
- Perfiles personalizables
- Control de acceso por módulo

### Configuración del Sistema
- Personalización de la empresa:
  - Datos fiscales
  - Logo
  - Información de contacto
- Configuración de impresión
- Parámetros del sistema:
  - Moneda
  - Impuestos
  - Alertas de stock
- Copias de seguridad

### Características Técnicas
- Interfaz responsive
- Diseño moderno con Bootstrap 5
- Validaciones en tiempo real
- Búsqueda y filtros dinámicos
- Paginación de resultados
- Modales para acciones importantes
- Notificaciones y alertas
- Protección CSRF
- Manejo de sesiones
- Optimización de consultas

## Requisitos Técnicos
- Python 3.8+
- Django 4.0+
- PostgreSQL/MySQL
- Bootstrap 5
- Font Awesome 5
- Dependencias adicionales en requirements.txt

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Iniciar el servidor:
```bash
python manage.py runserver
```

## Contribución
Las contribuciones son bienvenidas. Por favor, asegúrese de actualizar las pruebas según corresponda.

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)

## Soporte
Para soporte, envíe un correo electrónico a [correo_de_soporte] o abra un issue en el repositorio.

## Estado del Proyecto
En desarrollo activo - Versión 1.0.0 #
