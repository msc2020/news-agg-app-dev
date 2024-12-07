from waitress import serve

from app import app

if __name__ == '__main__':
    #serve(app)
    local_host, local_port = '0.0.0.0', 8080
    print(f'\nListening at: {local_host}:{local_port}')
    serve(app, host=local_host, port=local_port)
    