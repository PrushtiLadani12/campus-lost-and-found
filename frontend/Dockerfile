# Frontend Nginx Container with API Reverse Proxy
FROM nginx:alpine

# Copy custom reverse-proxy config
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy static assets into Nginx html directory
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
