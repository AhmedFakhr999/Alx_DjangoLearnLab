# Deployment Configuration for HTTPS

To support secure HTTPS connections, the following configuration steps should be followed:

## SSL/TLS Certificate Implementation

1. **Obtain an SSL Certificate**: Use a trusted CA like Let's Encrypt (using Certbot) or a commercial provider.
2. **Web Server Configuration (Nginx)**:
   Configure Nginx to handle SSL termination and redirect HTTP traffic to HTTPS.

### Example Nginx Configuration (`/etc/nginx/sites-available/library_project`):

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Strong SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/project/static/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }
}
```

## Django Settings Integration

Ensure the following settings are active in `settings.py` (which they are in this project):

- `SECURE_SSL_REDIRECT = True`
- `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`
- `SECURE_HSTS_SECONDS = 31536000`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- `SECURE_HSTS_PRELOAD = True`
