# 🏪 Sistema POS - Point of Sale System

[![Django](https://img.shields.io/badge/Django-5.1.6-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Un **Sistema de Punto de Venta (POS)** moderno y completo desarrollado con **Django 5.1.6**, diseñado para gestionar eficientemente las operaciones comerciales de pequeñas y medianas empresas.

## 📋 Tabla de Contenidos

- [✨ Características](#-características)
- [🛠 Tecnologías](#-tecnologías)
- [🚀 Instalación](#-instalación)
- [⚙️ Configuración](#%EF%B8%8F-configuración)
- [📱 Uso](#-uso)
- [🏗 Estructura del Proyecto](#-estructura-del-proyecto)
- [🤝 Contribuir](#-contribuir)
- [📝 Licencia](#-licencia)
- [🆘 Soporte](#-soporte)

## ✨ Características

### 🛒 Punto de Venta (POS)
- Interfaz intuitiva para procesamiento rápido de ventas
- Carrito de compras dinámico con actualización en tiempo real
- Búsqueda rápida de productos por nombre o código de barras
- Múltiples métodos de pago (efectivo, tarjeta, transferencia)
- Impresión automática de recibos
- Aplicación de descuentos y promociones

### 📦 Gestión de Inventario
- Control completo de stock con alertas automáticas
- Gestión de productos con imágenes y códigos de barras
- Categorización avanzada de productos
- Seguimiento de niveles mínimos y máximos de stock
- Historial completo de movimientos de inventario
- Valorización del inventario en tiempo real

### 📊 Dashboard y Reportes
- Dashboard ejecutivo con métricas clave
- Reportes de ventas diarios, semanales y mensuales
- Gráficos interactivos de tendencias de ventas
- Análisis de productos más vendidos
- Reportes de inventario y stock bajo
- Exportación de reportes en PDF y Excel

### 👥 Gestión de Clientes
- Base de datos completa de clientes
- Historial de compras por cliente
- Información de contacto y preferencias
- Programa de fidelización (próximamente)

### 🏢 Gestión de Proveedores
- Registro detallado de proveedores
- Historial de compras y pagos
- Gestión de órdenes de compra
- Control de facturas y pagos pendientes

### 👤 Sistema de Usuarios
- Autenticación segura con roles y permisos
- Diferentes niveles de acceso (Administrador, Vendedor, Almacenista)
- Registro de actividades por usuario
- Perfiles personalizables

### 🔧 Características Técnicas
- Diseño responsive compatible con móviles y tablets
- Interfaz moderna con Bootstrap 5
- Base de datos PostgreSQL para alta performance
- Sistema de caché para optimización
- Validaciones en tiempo real
- Protección CSRF y seguridad avanzada

## 🛠 Tecnologías

- **Backend:** Django 5.1.6, Python 3.8+
- **Base de Datos:** PostgreSQL, SQLite (desarrollo)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Iconos:** Font Awesome
- **Formularios:** Django Crispy Forms
- **Autenticación:** Django Authentication System
- **Deployment:** Compatible con Heroku, AWS, DigitalOcean

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 13+ (para producción)
- Git

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/pos-system.git
cd pos-system
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Configurar base de datos**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Cargar datos de ejemplo (opcional)**
```bash
python manage.py loaddata fixtures/sample_data.json
```

8. **Iniciar servidor de desarrollo**
```bash
python manage.py runserver
```

Visita `http://127.0.0.1:8000` para acceder al sistema.

## ⚙️ Configuración

### Variables de Entorno

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DB_NAME=nombre_base_datos
DB_USER=usuario_db
DB_PASSWORD=password_db
DB_HOST=localhost
DB_PORT=5432
```

### Configuración de Producción

Para despliegue en producción, asegúrate de:

1. Establecer `DEBUG=False`
2. Configurar `ALLOWED_HOSTS`
3. Usar PostgreSQL como base de datos
4. Configurar archivos estáticos y media
5. Implementar HTTPS
6. Configurar logs y monitoreo

## 📱 Uso

### Acceso al Sistema

1. **Página de Login:** `/pos/login/`
2. **Dashboard Principal:** `/`
3. **Punto de Venta:** `/pos/pos/`
4. **Gestión de Productos:** `/pos/products/`
5. **Inventario:** `/pos/inventory/`
6. **Reportes:** `/pos/reports/`

### Flujo de Trabajo Típico

1. **Configuración inicial:** Crear categorías y productos
2. **Gestión de inventario:** Agregar stock inicial
3. **Procesamiento de ventas:** Usar la interfaz POS
4. **Seguimiento:** Revisar reportes y dashboard

## 🏗 Estructura del Proyecto

```
POS-/
├── FinalProject/           # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pos/                    # Aplicación principal POS
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Lógica de vistas
│   ├── urls.py            # URLs de la aplicación
│   ├── forms.py           # Formularios
│   └── admin.py           # Configuración admin
├── templates/             # Templates HTML
│   └── pos/
├── static/               # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── media/                # Archivos subidos
├── requirements.txt      # Dependencias Python
├── manage.py            # Comando Django
└── README.md           # Este archivo
```

## 📄 Modelos de Datos

### Principales Entidades

- **User:** Sistema de usuarios personalizado
- **Product:** Productos del inventario
- **Category:** Categorías de productos
- **Inventory:** Control de stock
- **Sale:** Registros de ventas
- **SaleItem:** Items de cada venta
- **Customer:** Base de datos de clientes
- **Supplier:** Proveedores

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Sigue las convenciones de código de Django
- Incluye tests para nuevas funcionalidades
- Actualiza la documentación según corresponda
- Asegúrate de que todos los tests pasen

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

### Documentación

- [Documentación de Django](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

### Contacto

- **Email:** ayath1006@gmail.com
- **Issues:** [GitHub Issues](https://github.com/tu-usuario/pos-system/issues)

### FAQ

**¿Cómo resetear la base de datos?**
```bash
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

**¿Cómo hacer backup de la base de datos?**
```bash
python manage.py dumpdata > backup.json
```

**¿Cómo restaurar un backup?**
```bash
python manage.py loaddata backup.json
```

## 🚦 Estado del Proyecto

- ✅ **Core POS Functionality** - Completo
- ✅ **Inventory Management** - Completo  
- ✅ **User Authentication** - Completo
- ✅ **Reports & Dashboard** - Completo
- 🔄 **Advanced Reporting** - En desarrollo
- 📋 **Mobile App** - Planificado
- 📋 **Multi-tienda** - Planificado

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025

---

<p align="center">
  <strong>¿Te gusta este proyecto? ¡Dale una ⭐!</strong>
</p>

---
Prueba de commit.
