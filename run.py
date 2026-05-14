"""
WebMents Backend Runner
Author: Anuj Singla (2210991317)
Institution: Chitkara University, Rajpura, Punjab

Usage:
    python run.py              # development (debug on, port 3000)
    PORT=5000 python run.py    # custom port
"""

import os
from app import app, mongo

def check_db():
    try:
        mongo.db.command('ping')
        print('✅  MongoDB connected')
    except Exception as e:
        print(f'❌  MongoDB connection failed: {e}')
        print('    Ensure MongoDB is running: mongod --dbpath /data/db')
        exit(1)

def print_banner():
    print('\n' + '='*60)
    print('  🚀  WebMents Python Backend')
    print('='*60)
    print(f'  Author : Anuj Singla (2210991317)')
    print(f'  Uni    : Chitkara University, Rajpura, Punjab')
    print(f'  DB     : {app.config["MONGO_URI"]}')
    print(f'  Port   : {PORT}')
    print('='*60)
    print('\n  Endpoints:')
    endpoints = [
        ('POST', '/signup',                          'Register user'),
        ('POST', '/login',                           'Login → JWT'),
        ('GET',  '/profile/<email>',                 'User profile'),
        ('PUT',  '/update-profile',                  'Update profile'),
        ('POST', '/add-product',                     'Add product'),
        ('GET',  '/products/<email>',                'Manufacturer products'),
        ('GET',  '/product/<id>',                    'Single product'),
        ('PUT',  '/update-product/<id>',             'Update product'),
        ('DEL',  '/delete-product/<id>',             'Delete product'),
        ('GET',  '/manufacturers',                   'All manufacturers'),
        ('GET',  '/credits/<email>',                 'Buyer credits'),
        ('POST', '/add-credits',                     'Add credits'),
        ('GET',  '/check-unlock/<b>/<m>',            'Check unlock'),
        ('POST', '/unlock-contact',                  'Unlock contact (1 credit)'),
        ('GET',  '/manufacturer-contact/<b>/<m>',   'Get contact details'),
        ('POST', '/order',                           'Place order'),
        ('GET',  '/orders/<email>',                  'Get orders'),
        ('PUT',  '/order-status/<id>',               'Update order status'),
        ('GET',  '/search?q=',                       'Global search'),
        ('GET',  '/stats/<email>',                   'Dashboard stats'),
        ('GET',  '/health',                          'Health check'),
    ]
    for method, path, desc in endpoints:
        print(f'  {method:<5} {path:<40} {desc}')
    print('\n' + '='*60)
    print(f'  Server: http://localhost:{PORT}')
    print('  Press Ctrl+C to stop')
    print('='*60 + '\n')


PORT = int(os.environ.get('PORT', 3000))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    check_db()
    print_banner()
    try:
        app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=True)
    except KeyboardInterrupt:
        print('\n🛑  Server stopped\n')
