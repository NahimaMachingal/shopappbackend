shopappbackend

A simple eCommerce backend built with **Django REST Framework (DRF)**, featuring **JWT authentication** for secure access.

## Features
- User authentication and authorization using **JWT**
- Product listing, filtering, and searching
- Shopping cart and order management
- Secure payment integration (future enhancement)
- Cloud-based media storage with **Cloudinary**

## Tech Stack
- **Django** (Backend framework)
- **Django REST Framework (DRF)** (API development)
- **JWT Authentication** (User authentication)
- **PostgreSQL** (Database)
- **Cloudinary** (Media file storage)
- **CORS Headers** (Cross-origin resource sharing support)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NahimaMachingal/shopappbackend.git
   cd shopappbackend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate  # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints
- `api/auth/login/` - User login with JWT authentication
- `api/auth/register/` - User registration
- `api/products/` - List all products
- `api/products/{id}/` - Retrieve a single product
- `api/cart/` - Manage shopping cart
- `api/orders/` - View and manage orders

## Deployment
To deploy the application, use **Gunicorn** and configure a production server.

## Contributing
Feel free to fork and submit pull requests. Any contributions are welcome!

## License
This project is licensed under the MIT License.

---
**GitHub Repository:** [Shopappbackend](https://github.com/NahimaMachingal/shopappbackend.git)
