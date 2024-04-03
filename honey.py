from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Honeypot!'

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def honeypot(path):
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

if __name__ == '__main__':
    app.run(debug=True)

