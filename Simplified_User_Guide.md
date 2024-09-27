# DjangoVPS Simplified User Guide

![Django Logo](https://static.djangoproject.com/img/logos/django-logo-positive.svg)

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Local Development Setup](#local-development-setup)
4. [Running the Application Locally](#running-the-application-locally)
5. [Preparing for Deployment](#preparing-for-deployment)
6. [Deploying to Your VPS](#deploying-to-your-vps)
7. [Managing Static and Media Files](#managing-static-and-media-files)
8. [Additional Tips](#additional-tips)
9. [Troubleshooting](#troubleshooting)
10. [License](#license)
11. [Acknowledgements](#acknowledgements)

## Introduction

Welcome to the **DjangoVPS Simplified User Guide**! This guide will help you set up and deploy your Django application efficiently. Follow these steps to develop your project locally and then deploy it seamlessly to your Virtual Private Server (VPS).

## Prerequisites

Before you begin, ensure you have the following:

- **Local Machine:**
  - [Python 3.9+](https://www.python.org/downloads/) installed
  - [Git](https://git-scm.com/downloads) installed
  - [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (optional but recommended)

- **VPS:**
  - A Linux-based VPS (e.g., Ubuntu 20.04)
  - A domain name (e.g., `yourdomain.com`) with DNS records pointing to your VPS IP
  - SSH access to your VPS

## Local Development Setup

These steps will guide you to set up your Django project on your local machine without using Docker.

### 1. Clone the Repository

Start by cloning the DjangoVPS repository to your local machine.

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

### 2. Set Up Environment Variables

Create two environment files: `.env` for production and `.env.local` for local development and testing.

- **Create `.env.local`:**

  ```bash
  cp .env.local.example .env.local
  ```

- **Edit `.env.local` and add the following:**

  ```dotenv
  # .env.local

  # Common Settings
  SECRET_KEY=your-local-secret-key
  DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

  # Debug Mode
  DEBUG=1

  # Database Configuration for Local Development (SQLite)
  # No need for DATABASE_* variables when using SQLite
  ```

  **Notes:**
  - Replace `your-local-secret-key` with a strong, unique key. You can generate one using Django's [secret key generator](https://djecrety.ir/).
  - Ensure `DEBUG` is set to `1` for development.

### 3. Install Dependencies

It's best practice to use a virtual environment to manage your project's dependencies.

- **Create a Virtual Environment:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

- **Install Required Packages:**

  ```bash
  pip install -r requirements.txt
  ```

### 4. Apply Migrations

Set up your database by applying migrations.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

Create an admin account to access the Django admin interface and Superuser Panel.

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your superuser credentials.

## Running the Application Locally

Start Django's development server to run your application locally.

```bash
python manage.py runserver
```

**Access the Application:**

- Open your browser and navigate to `http://localhost:8000` to view the homepage.
- Access the dashboard at `http://localhost:8000/dashboard/`.
- Login via `http://localhost:8000/login/`.
- Register a new user at `http://localhost:8000/register/`.
- Superusers can access the Superuser Panel at `http://localhost:8000/superuser/login/`.

**Note:** Only superusers can access the Superuser Panel. Regular users will be redirected to the dashboard upon login.

## Preparing for Deployment

Before deploying to your VPS, ensure that your project is ready.

### 1. Update Environment Variables

Ensure your `.env` and `.env.local` files have the correct configurations.

- **Production `.env`:**

  Create or update the `.env` file in the root directory.

  ```dotenv
  # .env

  # Common Settings
  SECRET_KEY=your-production-secret-key
  DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-VPS-ip

  # Debug Mode
  DEBUG=0

  # Database Configuration for Production (Supabase PostgreSQL)
  DATABASE_NAME=your-database-name
  DATABASE_USER=your-database-user
  DATABASE_PASSWORD=your-database-password
  DATABASE_HOST=your-database-host
  DATABASE_PORT=your-database-port

  # Authentication Backends
  AUTHENTICATION_BACKENDS=main.backends.UsernameEmailBackend,django.contrib.auth.backends.ModelBackend

  # SSL Settings
  USE_SSL=1
  ```

  **Important:**
  - Replace `your-production-secret-key` with a strong, unique key.
  - Update `DJANGO_ALLOWED_HOSTS` with your actual domain names and VPS IP address.
  - Provide your Supabase PostgreSQL database credentials.

- **Ensure `.env` is Included in `.gitignore`:**

  The `.env` file should be listed in your `.gitignore` to prevent sensitive information from being committed.

  ```bash
  echo ".env" >> .gitignore
  ```

### 2. Push Changes to GitHub

Commit your changes and push your project to a new GitHub repository.

```bash
git add .
git commit -m "Prepare for deployment"
git remote add origin https://github.com/yourusername/yourrepository.git
git push -u origin main
```

## Deploying to Your VPS

Follow these steps to deploy your Django application to your VPS using Docker.

### 1. Prepare Your VPS

Ensure your VPS is updated and has the necessary tools installed.

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version
```

### 2. Clone the Repository on VPS

Clone your repository on the VPS.

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

### 3. Install Docker and Docker Compose

If you followed Step 1 on your VPS, Docker and Docker Compose should already be installed. Otherwise, refer to the [Docker installation guide](https://docs.docker.com/engine/install/ubuntu/) for your specific OS.

### 4. Configure Environment Variables on VPS

Create a `.env` file on your VPS for production settings.

```bash
nano .env
```

Add the production environment variables as shown in [Update Environment Variables](#1-update-environment-variables).

### 5. Delete `.env.local` on VPS

**Important:** On your VPS, you must delete the `.env.local` file to prevent it from overriding your production settings.

```bash
rm .env.local
```

### 6. Update Configuration Files

- **Edit `init-letsencrypt.sh`:**

  Open the `init-letsencrypt.sh` script and replace the placeholder domains and email with your own.

  ```bash
  nano init-letsencrypt.sh
  ```

  **Update the script with your domain and email:**

  ```bash
  domains=(yourdomain.com www.yourdomain.com)
  email="youremail@example.com" # Adding a valid address is strongly recommended
  ```

- **Edit `nginx.conf`:**

  Replace the placeholder domains with your own in the Nginx configuration.

  ```bash
  nano nginx.conf
  ```

  **Update `server_name`:**

  ```nginx
  server_name yourdomain.com www.yourdomain.com;
  ```

### 7. Initialize SSL Certificates

Run the `init-letsencrypt.sh` script to obtain and install SSL certificates.

```bash
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh
```

**Note:** Ensure that your DNS records have propagated before running the script. This typically takes a few hours.

### 8. Build and Run Docker Containers

Use Docker Compose to build and start your application.

```bash
docker-compose up --build -d
```

**Commands Explained:**
- `--build`: Builds the Docker images before starting the containers.
- `-d`: Runs the containers in detached mode.

### 9. Finalize Deployment

After the containers are up and running, execute the following commands to apply migrations and collect static files.

```bash
# Apply migrations
docker-compose run web python manage.py migrate

# Collect static files
docker-compose run web python manage.py collectstatic --noinput

# Restart Docker containers to apply changes
docker-compose down
docker-compose up -d --build
```

**Summary of Steps:**
1. **Migrate Database:** Ensure your database schema is up-to-date.
2. **Collect Static Files:** Collect all static assets for serving.
3. **Restart Containers:** Apply changes by rebuilding and restarting containers.

## Managing Static and Media Files

### Collecting Static Files

Ensure that all static files are collected and served correctly by Nginx.

```bash
docker-compose run web python manage.py collectstatic --noinput
```

### Serving Media Files

Media files are served from the `/media/` URL. Ensure that `MEDIA_ROOT` is correctly configured in `settings.py` and that Nginx is set up to serve these files.

## Additional Tips

- **Creating Migrations:**

  Whenever you make changes to your models, create and apply migrations.

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- **Running Tests:**

  To run your application's tests, use:

  ```bash
  python manage.py test
  ```

- **Superuser Panel:**

  Access the Superuser Panel at `http://yourdomain.com/superuser/login/` using your superuser credentials to view all registered users.

- **Security Reminder:**

  Always protect your `SECRET_KEY` and database credentials. Never expose them in public repositories.

- **Version Control:**

  Ensure that `.env` and other sensitive files are included in your `.gitignore` to prevent accidental commits.

## Troubleshooting

- **Template Not Found:**
  - Ensure that your templates are located in the correct directories (e.g., `templates/main/` and `templates/superuserapp/`).
  - Verify that `APP_DIRS` is set to `True` in `settings.py`.

- **Database Connection Issues:**
  - Confirm that your database credentials in `.env` are correct.
  - Ensure that the Supabase PostgreSQL service is running and accessible.

- **Nginx Errors:**
  - Check Nginx logs for detailed error messages.
    ```bash
    sudo tail -f /var/log/nginx/error.log
    ```

- **Docker Containers Not Starting:**
  - View Docker logs to identify issues.
    ```bash
    docker-compose logs
    ```

- **SSL Certificate Problems:**
  - Verify that your domain's DNS records are correctly pointing to your VPS.
  - Ensure that ports `80` and `443` are open and not blocked by a firewall.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgements

- **Django**: The web framework used.
- **Docker**: For containerization.
- **Nginx**: For efficient web serving.
- **Let's Encrypt**: For free SSL certificates.
- **Tailwind CSS**: For frontend styling.
- **Certbot**: For automated SSL management.