# DjangoVPS Boilerplate

![Django Logo](https://static.djangoproject.com/img/logos/django-logo-positive.svg)

## Overview

**DjangoVPS** is a boilerplate/template designed to streamline the process of local development and VPS deployment for Django applications. This setup leverages Docker, Nginx, and Certbot to provide an efficient and secure environment for your Django projects. Whether you're developing locally or deploying to a production server, DjangoVPS offers a robust foundation to build upon.

## Features

- **Dockerized Environment**: Simplify development and deployment with Docker and Docker Compose.
- **Nginx as a Reverse Proxy**: Efficiently handle HTTP/HTTPS requests and serve static/media files.
- **Automated SSL with Let's Encrypt**: Secure your application with free SSL certificates using Certbot.
- **Environment Management**: Easily manage different configurations for development and production using `.env.local` and `.env` files.
- **Gunicorn Application Server**: Serve your Django application with Gunicorn for better performance.

## Project Structure

.
├── .dockerignore
├── .env
├── .env.local
├── .gitignore
├── Dockerfile
├── README.md
├── db.sqlite3
├── docker-compose.yml
├── env
│ ├── bin
│ ├── include
│ ├── lib
│ └── pyvenv.cfg
├── init-letsencrypt.sh
├── main
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── migrations
│ ├── models.py
│ ├── templates
│ │ └── main
│ │ ├── dashboard.html
│ │ ├── index.html
│ │ ├── login.html
│ │ └── register.html
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── manage.py
├── media
├── myproject
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── nginx.conf
├── requirements.txt
└── static


## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your local machine or VPS.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.
- A domain name (e.g., `scriptflows.com`) with DNS configured.
- Access to your domain registrar (e.g., GoDaddy) to manage DNS records.
- Valid email address for Let's Encrypt SSL certificates.

## Setup Instructions

### 1. Clone the Repository
bash
git clone https://github.com/ZachRC/DjangoVPS.git
cd DjangoVPS


### 2. Configure Environment Variables

Create two environment files: `.env.local` for local development and `.env` for production.

#### `.env.local`

This file contains settings specific to your local development environment.

dotenv
.env.local
Common Settings
SECRET_KEY=your-local-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
Debug Mode
DEBUG=1
Database Configuration for Local Development (SQLite)
No need for DATABASE_ variables when using SQLite


#### `.env`

This file contains production settings and should **never** be committed to version control.

dotenv
.env
Common Settings
SECRET_KEY=your-production-secret-key
DJANGO_ALLOWED_HOSTS=yoururl.com,www.yoururl.com,your-VPS-ip
Debug Mode
DEBUG=0
Database Configuration for Production (Supabase PostgreSQL)
DATABASE_NAME=postgres
DATABASE_USER=your-supabase-username
DATABASE_PASSWORD=your-supabase-password
DATABASE_HOST=your-supabase-host
DATABASE_PORT=your-supabase-port


**Important**: Replace placeholders like `your-production-secret-key` and database credentials with your actual values.

### 3. Configure DNS Records

On your domain registrar (e.g., GoDaddy), set up the following DNS records:

1. **A Record for Root Domain**

   - **Type**: A
   - **Name**: @
   - **Value**: `167.172.224.226`
   - **TTL**: 1/2 Hour

2. **A Record for www Subdomain**

   - **Type**: A
   - **Name**: www
   - **Value**: `167.172.224.226`
   - **TTL**: 1/2 Hour

### 4. Build and Run Docker Containers

Ensure that Docker and Docker Compose are installed and running on your machine.

bash
docker-compose up --build -d


This command will:

- Build the Docker images based on the `Dockerfile`.
- Start the Django application using Gunicorn.
- Start Nginx as a reverse proxy.
- Start Certbot for SSL certificate management.

### 5. Initialize Let's Encrypt SSL Certificates

Run the `init-letsencrypt.sh` script to obtain and install SSL certificates.

bash
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh


**Script Breakdown:**

- **Domains & Email**: The script is configured to request certificates for `scriptflows.com` and `www.scriptflows.com` using the provided email (`zacharycherney@gmail.com`). Modify these values in the script as needed.

- **Staging Mode**: By default, `staging=0` is set to obtain real certificates. Use `staging=1` for testing to avoid hitting Let's Encrypt rate limits.

- **SSL Parameters**: The script downloads recommended TLS parameters if not already present.

- **Dummy Certificate**: A temporary certificate is created to allow Nginx to start.

- **Certificate Request**: Certbot requests a real SSL certificate for the specified domains.

- **Nginx Reload**: Nginx is reloaded to apply the new SSL certificates.

**Note**: Ensure that your DNS records have propagated before running the script. This can take up to 48 hours but typically completes within a few hours.

### 6. Access Your Application

After successful setup:

- **Local Development**: Access via `http://localhost:8000`
- **Production**: Access via `https://scriptflows.com` and `https://www.scriptflows.com`

### 7. Managing Static and Media Files

- Static files are served from `/static/`.
- Media files are served from `/media/`.

Ensure that you collect static files during the Docker build process:

bash
docker compose run web python manage.py collectstatic --noinput


### 8. Environment Management

- **Local Development**: Use `.env.local` to override settings for local development.
- **Production**: Use `.env` to set production configurations.

### 9. Security Considerations

- **Secret Keys**: Always keep your `SECRET_KEY` secure and do not expose it publicly.
- **Debug Mode**: Ensure `DEBUG=0` in production to avoid exposing sensitive information.
- **Allowed Hosts**: Configure `DJANGO_ALLOWED_HOSTS` in `.env` to include your domain names and IP address.

### 10. Renewing SSL Certificates

Certbot is set up to automatically renew SSL certificates. The `certbot` service in `docker-compose.yml` runs the renewal process every 12 hours. To manually trigger a renewal:

bash
docker compose run --rm certbot renew


### 11. Contributing

This boilerplate is intended for ease of setup and deployment. Contributions are welcome to enhance its features or improve its documentation. Fork the repository on GitHub and submit pull requests for any improvements.

### 12. Troubleshooting

- **DNS Propagation**: Ensure your DNS records are correctly set and have fully propagated.
- **Port Conflicts**: Ensure ports `80` and `443` are free on your VPS.
- **Permissions**: Verify that `init-letsencrypt.sh` has execute permissions.
- **Logs**: Check Docker logs for any issues.

bash
docker compose logs


### 13. License

This project is open-source and available under the [MIT License](LICENSE).

## References

- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Certbot Documentation](https://certbot.eff.org/)

## Acknowledgements

- **Django**: The web framework used.
- **Docker**: For containerization.
- **Nginx**: For efficient web serving.
- **Let's Encrypt**: For free SSL certificates.
