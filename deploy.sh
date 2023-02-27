#!/bin/bash

# Install and activate virtual environment
pip install pipenv
pipenv --python 3.8
pipenv install --dev

# Load environment variables
cp .env.example .env
source .env

# Install dependencies
pipenv install --ignore-pipfile

# Configure firewall
sudo ufw allow 5000/tcp

# Install and configure MySQL
sudo apt-get update
sudo apt-get install -y mysql-server
sudo systemctl start mysql.service

# Create database and user
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE ${MYSQL_DATABASE}"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE USER ${MYSQL_USER}@localhost IDENTIFIED BY '${MYSQL_PASSWORD}'"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO ${MYSQL_USER}@localhost"

# Install and configure Nginx
sudo apt-get install -y nginx
sudo rm /etc/nginx/sites-enabled/default
sudo tee /etc/nginx/sites-available/your_app_name > /dev/null <<EOF
server {
    listen 80;
    server_name your_domain_name_or_server_ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
sudo ln -s /etc/nginx/sites-available/your_app_name /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

