import os
from flask import Flask, request
import geoip2.database

app = Flask(__name__)

# Specify the path to the GeoLite2-Country.mmdb file
geoip_database_path = os.path.expanduser('~/honeypot/GeoLite2-Country_20240329/GeoLite2-Country.mmdb')

# Load the GeoIP database
reader = geoip2.database.Reader(geoip_database_path)

@app.route('/')
def index():
    return 'Welcome to the Honeypot!'

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def honeypot(path):
    # Trace the user's IP address and location
    ip_address = request.remote_addr
    location = get_location(ip_address)
    print(f"IP Address: {ip_address}")
    print(f"Location: {location}")

    # Log the incoming request
    log_request(request)

    # Respond with something generic to avoid detection
    return '404 Not Found', 404

def log_request(request):
    # Log the request method, path, and headers
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print("Headers:")
    for key, value in request.headers.items():
        print(f"\t{key}: {value}")
    print("Body:")
    print(request.data.decode('utf-8'))

def get_location(ip_address):
    try:
        response = reader.country(ip_address)
        return response.country.name
    except geoip2.errors.AddressNotFoundError:
        return "Unknown"

if __name__ == '__main__':
    # Change host to '0.0.0.0' to make the app accessible from other computers
    app.run(host='0.0.0.0', debug=True)

