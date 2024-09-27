# ScriptFlows Django Application

This is a Django application deployed with Docker, Nginx, and Let's Encrypt SSL.

## Deployment Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/scriptflows.git
   cd scriptflows
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in the necessary details.

3. Initialize SSL certificates:
   ```
   ./init-letsencrypt.sh
   ```

4. Build and start the Docker containers:
   ```
   docker-compose up -d --build
   ```

5. Your application should now be accessible at https://scriptflows.com

## Maintenance

- To update the application:
  ```
  git pull
  docker-compose up -d --build
  ```

- SSL certificates will auto-renew every 60 days.

