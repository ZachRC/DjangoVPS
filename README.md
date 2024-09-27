# DjangoVPS Boilerplate

![Django Logo](https://static.djangoproject.com/img/logos/django-logo-positive.svg)

## Overview

**DjangoVPS** is a comprehensive boilerplate/template designed to streamline the process of local development and VPS deployment for Django applications. Leveraging Docker, Nginx, and Certbot, this setup provides an efficient and secure environment for your Django projects.

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Usage](#usage)
5. [User Guides](#user-guides) <!-- Add this section -->

## Features

- **Dockerized Environment**: Simplify development and deployment with Docker and Docker Compose.
- **Nginx as a Reverse Proxy**: Efficiently handle HTTP/HTTPS requests and serve static/media files.
- **Automated SSL with Let's Encrypt**: Secure your application with free SSL certificates using Certbot.
- **Environment Management**: Easily manage different configurations for development and production using `.env.local` and `.env` files.
- **Gunicorn Application Server**: Serve your Django application with Gunicorn for better performance.
- **Custom User Authentication**:
  - Register with both **username** and **email**.
  - Login using either **username** or **email**.
  - Ensures security and flexibility across both local and production environments.
- **Superuser Panel**:
  - Custom admin login page for superusers.
  - Dedicated panel displaying all registered users and their information.
  - Accessible only to superusers.
- **Responsive Frontend**: Utilizes Tailwind CSS for a clean and responsive design.

## Project Structure

```
.
├── .dockerignore
├── .env
├── .env.local
├── .gitignore
├── Dockerfile
├── README.md
├── db.sqlite3
├── docker-compose.yml
├── init-letsencrypt.sh
├── main
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── backends.py
│   ├── forms.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── ... (migration files)
│   ├── models.py
│   ├── templates
│   │   └── main
│   │       ├── dashboard.html
│   │       ├── index.html
│   │       ├── login.html
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── media
├── myproject
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── nginx.conf
├── requirements.txt
├── static
└── superuserapp
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── templates
    │   └── superuserapp
    │       ├── login.html
    │       └── panel.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your local machine or VPS.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.
- A domain name (e.g., `scriptflows.com`) with DNS configured.
- Access to your domain registrar (e.g., GoDaddy) to manage DNS records.
- Valid email address for Let's Encrypt SSL certificates.

## Usage

### 1. Clone the Repository

```bash
git clone https://github.com/ZachRC/DjangoVPS.git
cd DjangoVPS
```

### 2. Configure Environment Variables

Create two environment files: `.env.local` for local development and `.env` for production.

#### `.env.local`

This file contains settings specific to your local development environment.

```dotenv
# Common Settings
SECRET_KEY=your-local-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Debug Mode
DEBUG=1

# Database Configuration for Local Development (SQLite)
# No need for DATABASE_ variables when using SQLite
```

#### `.env`

This file contains production settings and should **never** be committed to version control.

```dotenv
# Common Settings
SECRET_KEY=your-production-secret-key
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-VPS-ip

# Debug Mode
DEBUG=0

# Database Configuration for Production (Supabase PostgreSQL)
DATABASE_NAME=postgres
DATABASE_USER=your-db-username
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=your-db-host
DATABASE_PORT=your-db-port

# SSL Configuration
USE_SSL=1
```

**Important**: Replace placeholders like `your-production-secret-key` and database credentials with your actual values.

### 3. Configure DNS Records

On your domain registrar (e.g., GoDaddy), set up the following DNS records:

1. **A Record for Root Domain**
   - **Type**: A
   - **Name**: @
   - **Value**: `your-VPS-ip-address`
   - **TTL**: 1/2 Hour

2. **A Record for www Subdomain**
   - **Type**: A
   - **Name**: www
   - **Value**: `your-VPS-ip-address`
   - **TTL**: 1/2 Hour

### 4. Build and Run Docker Containers

Ensure that Docker and Docker Compose are installed and running on your machine.

```bash
docker compose up --build -d
```

This command will:

- Build the Docker images based on the `Dockerfile`.
- Start the Django application using Gunicorn.
- Start Nginx as a reverse proxy.
- Start Certbot for SSL certificate management.

### 5. Initialize Let's Encrypt SSL Certificates

Run the `init-letsencrypt.sh` script to obtain and install SSL certificates.

```bash
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh
```

**Script Breakdown:**

- **Domains & Email**: The script is configured to request certificates for `yourdomain.com` and `www.yourdomain.com` using the provided email (e.g., `youremail@example.com`). Modify these values in the script as needed.
- **Staging Mode**: By default, `staging=0` is set to obtain real certificates. Use `staging=1` for testing to avoid hitting Let's Encrypt rate limits.
- **SSL Parameters**: The script downloads recommended TLS parameters if not already present.
- **Dummy Certificate**: A temporary certificate is created to allow Nginx to start.
- **Certificate Request**: Certbot requests a real SSL certificate for the specified domains.
- **Nginx Reload**: Nginx is reloaded to apply the new SSL certificates.

**Note**: Ensure that your DNS records have propagated before running the script. This can take up to 48 hours but typically completes within a few hours.

### 6. Apply Database Migrations

After setting up the environment and running the containers, apply the database migrations.

```bash
docker compose run web python manage.py makemigrations
docker compose run web python manage.py migrate
```

**Note**: Migrations are essential for synchronizing your Django models with the database schema. They should **not** be added to `.gitignore` to ensure consistency across different environments.

### 7. Create a Superuser (Optional)

To access the Django admin interface and the Superuser Panel, create a superuser.

```bash
docker compose run web python manage.py createsuperuser
```

**Ensure:**

- The superuser has `is_superuser=True` and `is_staff=True`.
- Use the superuser credentials to log in via `superuserapp/login/`.

### 8. Collect Static Files

Ensure that static files are properly collected, especially since Tailwind CSS is being used from a CDN.

```bash
docker compose run web python manage.py collectstatic --noinput
```

### 9. Access Your Application

After successful setup:

- **Local Development**: Access via `http://localhost:8000`
- **Production**: Access via `https://yourdomain.com` and `https://www.yourdomain.com`

### 10. Managing Static and Media Files

- **Static Files**: Served from `/static/`.
- **Media Files**: Served from `/media/`.

Ensure that you collect static files during the Docker build process as shown above.

### 11. Environment Management

- **Local Development**: Use `.env.local` to override settings for local development.
- **Production**: Use `.env` to set production configurations.

### 12. Custom User Authentication

DjangoVPS now supports robust user authentication with the following capabilities:

- **Registration**:
  - Users can register using both a **username** and **email**.
  - Email addresses are unique and required for registration.
  
- **Login**:
  - Users can log in using either their **username** or **email** along with their password.
  
- **Backend Configuration**:
  - Custom authentication backend (`UsernameEmailBackend`) ensures flexibility in user login methods.
  
**Testing Authentication:**

1. **Register a New User**:
   - Navigate to `/register/`.
   - Fill out the registration form with a unique username and email.
   - Submit the form and ensure you're redirected to the dashboard without errors.

2. **Login with Username**:
   - Log out if already logged in.
   - Navigate to `/login/`.
   - Enter your username and password to log in.

3. **Login with Email**:
   - Log out again.
   - Navigate to `/login/`.
   - Enter your email and password to log in.

### 13. Superuser Panel

Superusers can access a dedicated panel to view all registered users.

**Accessing the Panel:**

1. **Login as Superuser**:
   - Navigate to `/superuser/login/`.
   - Enter your superuser credentials.

2. **View Users**:
   - Upon successful login, you'll be redirected to `/superuser/panel/`.
   - Here, you'll see a table listing all registered users along with their information.

**Dashboard Enhancements:**

- If a superuser is authenticated and is on `dashboard.html`, a button is available to redirect them to the `superuserapp` panel.

```html
{% if user.is_superuser %}
<a href="{% url 'superuserapp:panel' %}" class="block w-full bg-green-600 text-white py-3 rounded-lg font-semibold text-center hover:bg-green-700 transition duration-300">Superuser Panel</a>
{% endif %}
```

### 14. Security Considerations

- **Secret Keys**: Always keep your `SECRET_KEY` secure and do not expose it publicly.
- **Debug Mode**: Ensure `DEBUG=0` in production to avoid exposing sensitive information.
- **Allowed Hosts**: Configure `DJANGO_ALLOWED_HOSTS` in `.env` to include your domain names and IP address.
- **SSL Certificates**: Use automated SSL renewals to maintain secure HTTPS connections.

### 15. Renewing SSL Certificates

Certbot is set up to automatically renew SSL certificates. The `certbot` service in `docker-compose.yml` runs the renewal process every 12 hours. To manually trigger a renewal:

```bash
docker compose run --rm certbot renew
```

### 16. Managing Migration Files

**Should Migration Files Be Added to `.gitignore`?**

**Recommendation:** **Do _not_ add migration files to `.gitignore`**. Migration files are essential for maintaining the consistency of your database schema across different environments (development, testing, production). Tracking them in version control ensures that all changes to the models are accurately reflected in the database structure wherever your project is deployed.

**Benefits of Tracking Migrations:**

- **Consistency:** Ensures that all developers and deployment environments apply the same schema changes.
- **Collaboration:** Facilitates collaboration by sharing migration history among team members.
- **Deployment:** Streamlines the deployment process by allowing automated migration application.

**Action Steps:**

1. **Ensure Migrations Are Not Ignored:**
   - **Review Your `.gitignore`:** Verify that your `.gitignore` doesn't exclude migration files. Migration files are typically located in each app's `migrations` directory (e.g., `main/migrations/` and `superuserapp/migrations/`).

   - **Sample `.gitignore` for Migrations:**
     ```gitignore
     # Migrations
     # Don't ignore migration files
     # Example:
     # main/migrations/
     # !main/migrations/__init__.py
     # superuserapp/migrations/
     # !superuserapp/migrations/__init__.py
     ```

2. **Add Existing Migrations to Git:**
   If you've previously ignored migrations or haven't added them yet, you can add them to your repository:

   ```bash
   git add main/migrations/
   git add superuserapp/migrations/
   git commit -m "Add initial migration files for main and superuserapp"
   ```

3. **Handle Future Migrations Appropriately:**
   - **Creating Migrations:**
     Whenever you make changes to your models, create new migrations:

     ```bash
     docker compose run web python manage.py makemigrations
     ```

   - **Applying Migrations:**
     Apply migrations to your development and production databases:

     ```bash
     docker compose run web python manage.py migrate
     ```

**Important Considerations:**

- **Sequential Migrations:** Ensure that migration files are applied in the correct order to prevent conflicts and maintain database integrity.
- **Avoiding Conflicts:** When working in a team, communicate schema changes to avoid migration conflicts. You might need to merge migration files if multiple developers are making concurrent changes.

### 17. Contributing

This boilerplate is intended for ease of setup and deployment. Contributions are welcome to enhance its features or improve its documentation. Fork the repository on GitHub and submit pull requests for any improvements.

### 18. Troubleshooting

- **Template Loading Issues**: If you encounter `TemplateDoesNotExist` errors, ensure that your templates are correctly placed within the `templates` directory of each app and that `APP_DIRS` is set to `True` in your `settings.py`.
- **DNS Propagation**: Ensure your DNS records are correctly set and have fully propagated.
- **Port Conflicts**: Ensure ports `80` and `443` are free on your VPS.
- **Permissions**: Verify that `init-letsencrypt.sh` has execute permissions.
- **Logs**: Check Docker logs for any issues.

```bash
docker compose logs
```

- **Superuser Redirection Issues**: If superusers are being redirected incorrectly, ensure that the `get_success_url` method in `views.py` of `superuserapp` is correctly set to redirect to the panel.

### 19. License

This project is open-source and available under the [MIT License](LICENSE).

## References

- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Certbot Documentation](https://certbot.eff.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## Acknowledgements

- **Django**: The web framework used.
- **Docker**: For containerization.
- **Nginx**: For efficient web serving.
- **Let's Encrypt**: For free SSL certificates.
- **Tailwind CSS**: For frontend styling.

## User Guides

- [Simplified User Guide](Simplified_User_Guide.md) <!-- Link to the guide -->

---