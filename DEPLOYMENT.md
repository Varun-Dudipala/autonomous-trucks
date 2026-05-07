# Deployment Guide

This guide covers deploying the Autonomous Trucks Fleet Management System to various production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Production Checklist](#production-checklist)
- [Deployment Options](#deployment-options)
  - [Heroku](#heroku)
  - [AWS EC2](#aws-ec2)
  - [Google Cloud Platform](#google-cloud-platform)
  - [Railway](#railway)
  - [Docker](#docker)
- [MongoDB Setup](#mongodb-setup)
- [Environment Variables](#environment-variables)
- [Monitoring](#monitoring)

## Prerequisites

Before deploying, ensure you have:

- [ ] Tested application locally
- [ ] Set up production MongoDB database
- [ ] Obtained Google Maps API key
- [ ] Generated secure SECRET_KEY
- [ ] Set DEBUG=False for production
- [ ] Configured CORS if needed
- [ ] Set up error monitoring (optional)

## Production Checklist

### Security

- [ ] Use environment variables for all secrets
- [ ] Set strong SECRET_KEY (minimum 32 characters)
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookie settings
- [ ] Disable DEBUG mode
- [ ] Implement rate limiting
- [ ] Add CSRF protection
- [ ] Sanitize all user inputs

### Performance

- [ ] Use production MongoDB (Atlas, etc.)
- [ ] Add database indexes
- [ ] Enable gzip compression
- [ ] Configure CDN for static files
- [ ] Implement caching (Redis)
- [ ] Use Gunicorn with multiple workers

### Monitoring

- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Monitor database performance
- [ ] Track API usage

## Deployment Options

### Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku

   # Ubuntu
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create Heroku app**
   ```bash
   heroku create autonomous-trucks-app
   ```

3. **Add MongoDB Atlas**
   ```bash
   # Sign up for MongoDB Atlas (free tier available)
   # Get connection string and add to Heroku config
   heroku config:set MONGODB_URI="your_mongodb_atlas_uri"
   ```

4. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY="your_secure_random_string"
   heroku config:set GOOGLE_MAPS_API_KEY="your_api_key"
   heroku config:set DEBUG=False
   heroku config:set FLASK_ENV=production
   ```

5. **Create Procfile**
   ```bash
   echo "web: gunicorn app:app" > Procfile
   ```

6. **Deploy**
   ```bash
   git push heroku main
   heroku open
   ```

### AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier) or larger
   - Configure security group (ports 22, 80, 443)

2. **Connect and setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip

   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python, pip, nginx
   sudo apt install python3-pip python3-venv nginx -y
   ```

3. **Clone and setup application**
   ```bash
    git clone https://github.com/your-username/autonomous-trucks.git
   cd autonomous-trucks

   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your values
   ```

5. **Set up Gunicorn systemd service**
   ```bash
   sudo nano /etc/systemd/system/autonomous-trucks.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Autonomous Trucks Fleet Management
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/autonomous-trucks
   Environment="PATH=/home/ubuntu/autonomous-trucks/venv/bin"
   ExecStart=/home/ubuntu/autonomous-trucks/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable autonomous-trucks
   sudo systemctl start autonomous-trucks
   ```

6. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/autonomous-trucks
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/autonomous-trucks /etc/nginx/sites-enabled
   sudo systemctl restart nginx
   ```

7. **Set up SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

### Google Cloud Platform

1. **Install gcloud CLI**
   ```bash
   # Follow instructions at https://cloud.google.com/sdk/docs/install
   ```

2. **Create App Engine app**
   ```bash
   gcloud app create --region=us-central
   ```

3. **Create app.yaml**
   ```yaml
   runtime: python39
   entrypoint: gunicorn -b :$PORT app:app

   env_variables:
     SECRET_KEY: "your_secret_key"
     GOOGLE_MAPS_API_KEY: "your_api_key"
     MONGODB_URI: "your_mongodb_atlas_uri"
     DEBUG: "False"
   ```

4. **Deploy**
   ```bash
   gcloud app deploy
   gcloud app browse
   ```

### Railway

Railway is the easiest deployment option!

1. **Sign up at [Railway.app](https://railway.app)**

2. **Connect GitHub repo**
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose your repository

3. **Add MongoDB**
   - Click "New"
   - Select "Database"
   - Choose "MongoDB"
   - Railway will provide MONGODB_URI automatically

4. **Set environment variables**
   - Go to Variables tab
   - Add:
     - `SECRET_KEY`
     - `GOOGLE_MAPS_API_KEY`
     - `DEBUG=False`
     - `FLASK_ENV=production`

5. **Deploy**
   - Railway automatically builds and deploys
   - Get your URL from the deployment

### Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   # Install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   RUN pip install gunicorn

   # Copy application
   COPY . .

   # Expose port
   EXPOSE 5000

   # Run with gunicorn
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. **Create docker-compose.yml** (for local testing with MongoDB)
   ```yaml
   version: '3.8'

   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - MONGODB_URI=mongodb://mongo:27017/
         - SECRET_KEY=${SECRET_KEY}
         - GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}
       depends_on:
         - mongo

     mongo:
       image: mongo:4.4
       ports:
         - "27017:27017"
       volumes:
         - mongo_data:/data/db

   volumes:
     mongo_data:
   ```

3. **Build and run**
   ```bash
   docker-compose up --build
   ```

## MongoDB Setup

### MongoDB Atlas (Recommended)

1. **Sign up** at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

2. **Create free cluster**
   - Choose M0 (free tier)
   - Select region close to your app

3. **Configure access**
   - Network Access: Add your IP (or 0.0.0.0/0 for any IP)
   - Database Access: Create user with password

4. **Get connection string**
   - Click "Connect"
   - Choose "Connect your application"
   - Copy connection string
   - Replace `<password>` with your password

5. **Set environment variable**
   ```bash
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/autonomous_trucks?retryWrites=true&w=majority
   ```

### Self-hosted MongoDB

If running MongoDB on the same server:

```bash
# Install MongoDB
sudo apt install mongodb-org

# Start service
sudo systemctl start mongod
sudo systemctl enable mongod

# Use in .env
MONGODB_URI=mongodb://localhost:27017/
```

## Environment Variables

### Required Variables

```bash
# Flask
SECRET_KEY=<generate_with_python_-c_'import_secrets;_print(secrets.token_hex(32))'>
DEBUG=False
FLASK_ENV=production

# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db
MONGODB_DATABASE=autonomous_trucks

# Google Maps
GOOGLE_MAPS_API_KEY=your_actual_api_key

# Server
HOST=0.0.0.0
PORT=5000
```

### Generate SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Monitoring

### Error Tracking with Sentry

1. **Install Sentry SDK**
   ```bash
   pip install sentry-sdk[flask]
   ```

2. **Add to app.py**
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.flask import FlaskIntegration

   sentry_sdk.init(
       dsn="your_sentry_dsn",
       integrations=[FlaskIntegration()],
       traces_sample_rate=1.0
   )
   ```

### Uptime Monitoring

Use services like:
- [UptimeRobot](https://uptimerobot.com/) (free)
- [Pingdom](https://www.pingdom.com/)
- [StatusCake](https://www.statuscake.com/)

### Logging

Add proper logging in production:

```python
import logging

if not app.debug:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
```

## Post-Deployment

### Test Your Deployment

- [ ] Can access the site
- [ ] Login/Register works
- [ ] Database connection works
- [ ] Google Maps loads correctly
- [ ] All routes accessible
- [ ] Mobile responsive
- [ ] SSL/HTTPS enabled

### Maintenance

- Regularly update dependencies
- Monitor error logs
- Back up database
- Monitor performance metrics
- Keep MongoDB indexes updated

## Troubleshooting

### Common Issues

**MongoDB connection fails:**
- Check MONGODB_URI is correct
- Verify IP whitelist in MongoDB Atlas
- Check network connectivity

**Google Maps not loading:**
- Verify GOOGLE_MAPS_API_KEY is set
- Check API key has Maps JavaScript API enabled
- Check browser console for errors

**500 Internal Server Error:**
- Check application logs
- Verify all environment variables are set
- Check database connection

**Static files not loading:**
- Configure CDN or serve static files properly
- Check nginx configuration
- Verify file permissions

## Support

For deployment issues, open an issue in this repository.

---

**Happy Deploying!** 🚀
