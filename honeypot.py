import os
import logging
import requests
from flask import Flask, request
import geoip2.database

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Create file handler
file_handler = logging.FileHandler('honeypot.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logging.getLogger().addHandler(file_handler)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

# Specify the path to the GeoLite2-Country.mmdb file
geoip_database_path = os.path.expanduser('~/honeypot/GeoLite2-Country_20240329/GeoLite2-Country.mmdb')

# Load the GeoIP database
reader = geoip2.database.Reader(geoip_database_path)

# Function to get location details from IP address using GeoIP database
def get_location(ip_address):
    try:
        response = reader.country(ip_address)
        return response.country.name
    except geoip2.errors.AddressNotFoundError:
        return "Unknown"

# Fake login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Log request details including location
        ip_address = request.remote_addr
        location = get_location(ip_address)
        log_entry = f"IP: {ip_address} - Location: {location} - User Agent: {request.user_agent} - Username: {request.form.get('username')} - Password: {request.form.get('password')}"
        logging.info(log_entry)
        return "Login failed. Please try again."

    # Return fake login page HTML
    return """
    <html>
    <head><title>Fake Login Page</title></head>
    <body>
    <h2>Login</h2>
    <form method="post" action="/login">
    <label for="username">Username:</label><br>
    <input type="text" id="username" name="username"><br>
    <label for="password">Password:</label><br>
    <input type="password" id="password" name="password"><br><br>
    <input type="submit" value="Login">
    </form>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

