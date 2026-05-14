"""
WebMents Backend - Python Flask (Production-Quality)
Author: Anuj Singla (2210991317)
Institution: Chitkara University, Rajpura, Punjab

Full-featured backend replacing Node.js:
  - bcrypt password hashing
  - JWT authentication
  - Input validation & sanitization
  - Proper error handling
  - All original + new endpoints
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime, timedelta
from functools import wraps
import os
import jwt
import bcrypt
import re

# ─────────────────────────────────────────────
#  APP SETUP
# ─────────────────────────────────────────────
app = Flask(__name__, static_folder='public', static_url_path='')

app.config['MONGO_URI']           = os.environ.get('MONGO_URI', 'mongodb://127.0.0.1:27017/webments')
app.config['SECRET_KEY']          = os.environ.get('SECRET_KEY', 'webments-super-secret-2024')
app.config['UPLOAD_FOLDER']       = 'public/uploads'
app.config['MAX_CONTENT_LENGTH']  = 10 * 1024 * 1024   # 10 MB
app.config['ALLOWED_EXTENSIONS']  = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'jfif'}
app.config['JWT_EXPIRY_HOURS']    = 72

CORS(app)
mongo = PyMongo(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def unique_filename(original):
    safe = secure_filename(original)
    ts   = str(int(datetime.utcnow().timestamp() * 1000))
    return f"{ts}-{safe}"


def serialize(doc):
    """Make a MongoDB doc JSON-safe."""
    if doc is None:
        return None
    doc = dict(doc)
    doc['_id'] = str(doc['_id'])
    for k, v in doc.items():
        if isinstance(v, datetime):
            doc[k] = v.isoformat()
        elif isinstance(v, ObjectId):
            doc[k] = str(v)
    return doc


def serialize_many(docs):
    return [serialize(d) for d in docs]


def valid_email(email):
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email))


def valid_objectid(s):
    return ObjectId.is_valid(s)


def make_token(email, role):
    payload = {
        'email': email,
        'role':  role,
        'exp':   datetime.utcnow() + timedelta(hours=app.config['JWT_EXPIRY_HOURS'])
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


def decode_token(token):
    return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])


# ─── JWT decorator ───────────────────────────
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth  = request.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1]
        if not token:
            return jsonify({'success': False, 'message': 'Token missing'}), 401
        try:
            request.user = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated(*args, **kwargs):
            if request.user.get('role') not in roles:
                return jsonify({'success': False, 'message': 'Access denied'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


# ─────────────────────────────────────────────
#  STATIC FILES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)


# ─────────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────────

@app.route('/signup', methods=['POST'])
def signup():
    """Register a new buyer or manufacturer."""
    try:
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role     = request.form.get('role', '').strip()
        city     = request.form.get('city', '').strip()

        # ── Validation ──
        if not all([name, email, password, role, city]):
            return jsonify({'message': 'All fields are required'}), 400
        if role not in ('buyer', 'manufacturer'):
            return jsonify({'message': 'Invalid role'}), 400
        if not valid_email(email):
            return jsonify({'message': 'Invalid email address'}), 400
        if len(password) < 6:
            return jsonify({'message': 'Password must be at least 6 characters'}), 400

        if mongo.db.users.find_one({'email': email}):
            return jsonify({'message': 'User already registered'}), 409

        # ── Logo upload ──
        logo = ''
        if 'logo' in request.files:
            f = request.files['logo']
            if f and f.filename and allowed_file(f.filename):
                logo = unique_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], logo))

        # ── Hash password ──
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = {
            'name':           name,
            'email':          email,
            'password':       pw_hash,
            'role':           role,
            'city':           city,
            'logo':           logo,
            'phone':          '',
            'address':        '',
            'gst':            '',
            'specialization': '',
            'credits':        5 if role == 'buyer' else 0,
            'verified':       False,
            'createdAt':      datetime.utcnow(),
            'updatedAt':      datetime.utcnow()
        }
        mongo.db.users.insert_one(user)
        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        print(f'[signup] {e}')
        return jsonify({'message': 'Server error'}), 500


@app.route('/login', methods=['POST'])
def login():
    """Authenticate user, return JWT + role."""
    try:
        data     = request.get_json() or {}
        email    = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'message': 'Email and password required'}), 400

        user = mongo.db.users.find_one({'email': email})
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401

        if not bcrypt.checkpw(password.encode(), user['password'].encode()):
            return jsonify({'message': 'Invalid credentials'}), 401

        token = make_token(email, user['role'])
        return jsonify({
            'role':    user['role'],
            'name':    user['name'],
            'email':   user['email'],
            'credits': user.get('credits', 0),
            'token':   token
        }), 200

    except Exception as e:
        print(f'[login] {e}')
        return jsonify({'message': 'Server error'}), 500


@app.route('/profile/<email>', methods=['GET'])
def get_profile(email):
    """Get user profile (password excluded)."""
    try:
        user = mongo.db.users.find_one({'email': email.lower()})
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user = serialize(user)
        user.pop('password', None)
        return jsonify(user), 200
    except Exception as e:
        print(f'[profile] {e}')
        return jsonify({}), 500


@app.route('/update-profile', methods=['PUT'])
def update_profile():
    """Update manufacturer profile."""
    try:
        email = (request.form.get('email') or '').strip().lower()
        if not email:
            return jsonify({'message': 'Email required'}), 400

        update = {
            'name':           request.form.get('name', ''),
            'city':           request.form.get('city', ''),
            'phone':          request.form.get('phone', ''),
            'address':        request.form.get('address', ''),
            'gst':            request.form.get('gst', ''),
            'specialization': request.form.get('specialization', ''),
            'updatedAt':      datetime.utcnow()
        }
        if 'logo' in request.files:
            f = request.files['logo']
            if f and f.filename and allowed_file(f.filename):
                logo = unique_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], logo))
                update['logo'] = logo

        mongo.db.users.update_one({'email': email}, {'$set': update})
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        print(f'[update-profile] {e}')
        return jsonify({'message': 'Server error'}), 500


# ─────────────────────────────────────────────
#  PRODUCTS
# ─────────────────────────────────────────────

@app.route('/add-product', methods=['POST'])
def add_product():
    try:
        name   = request.form.get('name', '').strip()
        price  = request.form.get('price')
        cat    = request.form.get('category', '').strip()
        email  = (request.form.get('email') or '').strip().lower()
        desc   = request.form.get('description', '').strip()
        stock  = request.form.get('stock', 0)
        minord = request.form.get('minOrder', 1)

        if not all([name, price, cat, email]):
            return jsonify({'message': 'name, price, category, email are required'}), 400

        try:
            price  = float(price)
            stock  = int(stock)
            minord = int(minord)
        except ValueError:
            return jsonify({'message': 'Invalid numeric value'}), 400

        image = ''
        if 'image' in request.files:
            f = request.files['image']
            if f and f.filename and allowed_file(f.filename):
                image = unique_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

        product = {
            'name':              name,
            'price':             price,
            'category':          cat,
            'manufacturerEmail': email,
            'image':             image,
            'description':       desc,
            'stock':             stock,
            'minOrder':          minord,
            'createdAt':         datetime.utcnow(),
            'updatedAt':         datetime.utcnow()
        }
        mongo.db.products.insert_one(product)
        return jsonify({'message': 'Product added successfully'}), 201

    except Exception as e:
        print(f'[add-product] {e}')
        return jsonify({'message': 'Server error'}), 500


@app.route('/products/<email>', methods=['GET'])
def get_products(email):
    try:
        products = list(mongo.db.products.find(
            {'manufacturerEmail': email.lower()},
            sort=[('createdAt', -1)]
        ))
        return jsonify(serialize_many(products)), 200
    except Exception as e:
        print(f'[products] {e}')
        return jsonify([]), 500


@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        if not valid_objectid(product_id):
            return jsonify({'message': 'Invalid product ID'}), 400
        p = mongo.db.products.find_one({'_id': ObjectId(product_id)})
        if not p:
            return jsonify({'message': 'Product not found'}), 404
        return jsonify(serialize(p)), 200
    except Exception as e:
        print(f'[product] {e}')
        return jsonify({}), 500


@app.route('/update-product/<product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        if not valid_objectid(product_id):
            return jsonify({'message': 'Invalid product ID'}), 400

        data = request.get_json() or {}
        update = {'updatedAt': datetime.utcnow()}

        for field in ('name', 'category', 'description'):
            if field in data:
                update[field] = str(data[field]).strip()
        for field in ('price',):
            if field in data:
                update[field] = float(data[field])
        for field in ('stock', 'minOrder'):
            if field in data:
                update[field] = int(data[field])

        mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': update})
        return jsonify({'message': 'Product updated'}), 200
    except Exception as e:
        print(f'[update-product] {e}')
        return jsonify({'message': 'Server error'}), 500


@app.route('/delete-product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        if not valid_objectid(product_id):
            return jsonify({'message': 'Invalid product ID'}), 400
        p = mongo.db.products.find_one({'_id': ObjectId(product_id)})
        if p and p.get('image'):
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], p['image'])
            if os.path.exists(img_path):
                os.remove(img_path)
        mongo.db.products.delete_one({'_id': ObjectId(product_id)})
        return jsonify({'message': 'Product deleted'}), 200
    except Exception as e:
        print(f'[delete-product] {e}')
        return jsonify({'message': 'Server error'}), 500


# ─────────────────────────────────────────────
#  MANUFACTURERS
# ─────────────────────────────────────────────

@app.route('/manufacturers', methods=['GET'])
def get_manufacturers():
    """Return all manufacturers (password excluded)."""
    try:
        city   = request.args.get('city', '').strip()
        spec   = request.args.get('specialization', '').strip()
        search = request.args.get('search', '').strip()

        query = {'role': 'manufacturer'}
        if city:
            query['city'] = re.compile(city, re.IGNORECASE)
        if spec:
            query['specialization'] = re.compile(spec, re.IGNORECASE)
        if search:
            pattern = re.compile(search, re.IGNORECASE)
            query['$or'] = [{'name': pattern}, {'city': pattern}, {'specialization': pattern}]

        mfrs = list(mongo.db.users.find(query, {'password': 0}))
        return jsonify(serialize_many(mfrs)), 200
    except Exception as e:
        print(f'[manufacturers] {e}')
        return jsonify([]), 500


# ─────────────────────────────────────────────
#  CREDITS & CONTACT UNLOCK
# ─────────────────────────────────────────────

@app.route('/credits/<email>', methods=['GET'])
def get_credits(email):
    try:
        user = mongo.db.users.find_one({'email': email.lower()})
        return jsonify({'credits': user.get('credits', 0) if user else 0}), 200
    except Exception as e:
        return jsonify({'credits': 0}), 500


@app.route('/add-credits', methods=['POST'])
def add_credits():
    try:
        data   = request.get_json() or {}
        email  = data.get('email', '').strip().lower()
        amount = int(data.get('amount', 100))

        if not email:
            return jsonify({'success': False, 'message': 'Email required'}), 400
        if amount <= 0 or amount > 500:
            return jsonify({'success': False, 'message': 'Invalid amount'}), 400

        user = mongo.db.users.find_one_and_update(
            {'email': email, 'role': 'buyer'},
            {'$inc': {'credits': amount}},
            return_document=True
        )
        if not user:
            return jsonify({'success': False, 'message': 'Buyer not found'}), 404

        return jsonify({
            'success': True,
            'credits': user['credits'],
            'message': f'{amount} credits added successfully'
        }), 200
    except Exception as e:
        print(f'[add-credits] {e}')
        return jsonify({'success': False, 'message': 'Server error'}), 500


@app.route('/check-unlock/<buyer_email>/<manufacturer_email>', methods=['GET'])
def check_unlock(buyer_email, manufacturer_email):
    try:
        unlock = mongo.db.contact_unlocks.find_one({
            'buyerEmail':        buyer_email.lower(),
            'manufacturerEmail': manufacturer_email.lower()
        })
        return jsonify({'unlocked': bool(unlock)}), 200
    except Exception as e:
        return jsonify({'unlocked': False}), 500


@app.route('/unlock-contact', methods=['POST'])
def unlock_contact():
    try:
        data      = request.get_json() or {}
        b_email   = data.get('buyerEmail', '').strip().lower()
        mfr_email = data.get('manufacturerEmail', '').strip().lower()

        if not b_email or not mfr_email:
            return jsonify({'success': False, 'message': 'Both emails required'}), 400

        # Already unlocked?
        if mongo.db.contact_unlocks.find_one({'buyerEmail': b_email, 'manufacturerEmail': mfr_email}):
            return jsonify({'success': True, 'message': 'Already unlocked'}), 200

        buyer = mongo.db.users.find_one({'email': b_email, 'role': 'buyer'})
        if not buyer:
            return jsonify({'success': False, 'message': 'Buyer not found'}), 404
        if buyer.get('credits', 0) < 1:
            return jsonify({'success': False, 'message': 'Not enough credits'}), 400

        # Deduct 1 credit atomically
        updated = mongo.db.users.find_one_and_update(
            {'email': b_email, 'credits': {'$gte': 1}},
            {'$inc': {'credits': -1}},
            return_document=True
        )
        if not updated:
            return jsonify({'success': False, 'message': 'Not enough credits'}), 400

        mongo.db.contact_unlocks.insert_one({
            'buyerEmail':        b_email,
            'manufacturerEmail': mfr_email,
            'unlockedAt':        datetime.utcnow()
        })

        return jsonify({
            'success': True,
            'message': 'Contact unlocked!',
            'credits': updated['credits']
        }), 200

    except Exception as e:
        print(f'[unlock-contact] {e}')
        return jsonify({'success': False, 'message': 'Server error'}), 500


@app.route('/manufacturer-contact/<buyer_email>/<manufacturer_email>', methods=['GET'])
def manufacturer_contact(buyer_email, manufacturer_email):
    try:
        unlock = mongo.db.contact_unlocks.find_one({
            'buyerEmail':        buyer_email.lower(),
            'manufacturerEmail': manufacturer_email.lower()
        })
        if not unlock:
            return jsonify({'success': False, 'message': 'Not unlocked'}), 403

        mfr = mongo.db.users.find_one({'email': manufacturer_email.lower()})
        if not mfr:
            return jsonify({'success': False, 'message': 'Manufacturer not found'}), 404

        return jsonify({
            'success': True,
            'email':   mfr['email'],
            'phone':   mfr.get('phone') or 'Not provided',
            'address': mfr.get('address') or 'Not provided',
            'gst':     mfr.get('gst') or 'Not provided'
        }), 200
    except Exception as e:
        print(f'[manufacturer-contact] {e}')
        return jsonify({'success': False, 'message': 'Server error'}), 500


# ─────────────────────────────────────────────
#  ORDERS
# ─────────────────────────────────────────────

@app.route('/order', methods=['POST'])
def place_order():
    try:
        data = request.get_json() or {}
        required = ['buyerEmail', 'manufacturerEmail', 'items', 'total']
        if not all(data.get(f) for f in required):
            return jsonify({'message': 'Missing required order fields'}), 400

        order = {
            'buyerEmail':        data['buyerEmail'].lower(),
            'manufacturerEmail': data['manufacturerEmail'].lower(),
            'items':             data['items'],
            'total':             float(data['total']),
            'status':            'pending',
            'createdAt':         datetime.utcnow(),
            'updatedAt':         datetime.utcnow()
        }
        result = mongo.db.orders.insert_one(order)
        return jsonify({'message': 'Order placed', 'orderId': str(result.inserted_id)}), 201
    except Exception as e:
        print(f'[order] {e}')
        return jsonify({'message': 'Server error'}), 500


@app.route('/orders/<email>', methods=['GET'])
def get_orders(email):
    """Get orders — for manufacturer by manufacturerEmail, for buyer by buyerEmail."""
    try:
        role = request.args.get('role', 'manufacturer')
        field = 'manufacturerEmail' if role == 'manufacturer' else 'buyerEmail'
        orders = list(mongo.db.orders.find(
            {field: email.lower()},
            sort=[('createdAt', -1)]
        ))
        return jsonify(serialize_many(orders)), 200
    except Exception as e:
        print(f'[orders] {e}')
        return jsonify([]), 500


@app.route('/order-status/<order_id>', methods=['PUT'])
def update_order_status(order_id):
    """Update order status (manufacturer only)."""
    try:
        if not valid_objectid(order_id):
            return jsonify({'message': 'Invalid order ID'}), 400
        data   = request.get_json() or {}
        status = data.get('status', '')
        valid  = ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')
        if status not in valid:
            return jsonify({'message': f'Status must be one of: {", ".join(valid)}'}), 400

        mongo.db.orders.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': status, 'updatedAt': datetime.utcnow()}}
        )
        return jsonify({'message': 'Order status updated'}), 200
    except Exception as e:
        print(f'[order-status] {e}')
        return jsonify({'message': 'Server error'}), 500


# ─────────────────────────────────────────────
#  SEARCH
# ─────────────────────────────────────────────

@app.route('/search', methods=['GET'])
def search():
    """Global search across products and manufacturers."""
    try:
        q = request.args.get('q', '').strip()
        if not q:
            return jsonify({'products': [], 'manufacturers': []}), 200

        pattern = re.compile(q, re.IGNORECASE)

        products = list(mongo.db.products.find(
            {'$or': [{'name': pattern}, {'category': pattern}, {'description': pattern}]},
            sort=[('createdAt', -1)],
            limit=20
        ))
        manufacturers = list(mongo.db.users.find(
            {'role': 'manufacturer',
             '$or': [{'name': pattern}, {'city': pattern}, {'specialization': pattern}]},
            {'password': 0},
            limit=10
        ))
        return jsonify({
            'products':      serialize_many(products),
            'manufacturers': serialize_many(manufacturers)
        }), 200
    except Exception as e:
        print(f'[search] {e}')
        return jsonify({'products': [], 'manufacturers': []}), 500


# ─────────────────────────────────────────────
#  STATS  (dashboard numbers)
# ─────────────────────────────────────────────

@app.route('/stats/<email>', methods=['GET'])
def get_stats(email):
    """Return dashboard stats for a manufacturer or buyer."""
    try:
        email = email.lower()
        user  = mongo.db.users.find_one({'email': email})
        if not user:
            return jsonify({'message': 'User not found'}), 404

        if user['role'] == 'manufacturer':
            products_count = mongo.db.products.count_documents({'manufacturerEmail': email})
            orders_count   = mongo.db.orders.count_documents({'manufacturerEmail': email})
            pending_count  = mongo.db.orders.count_documents({'manufacturerEmail': email, 'status': 'pending'})
            unlocks_count  = mongo.db.contact_unlocks.count_documents({'manufacturerEmail': email})
            return jsonify({
                'products': products_count,
                'orders':   orders_count,
                'pending':  pending_count,
                'unlocks':  unlocks_count
            }), 200
        else:
            orders_count   = mongo.db.orders.count_documents({'buyerEmail': email})
            unlocks_count  = mongo.db.contact_unlocks.count_documents({'buyerEmail': email})
            return jsonify({
                'orders':  orders_count,
                'unlocks': unlocks_count,
                'credits': user.get('credits', 0)
            }), 200

    except Exception as e:
        print(f'[stats] {e}')
        return jsonify({}), 500


# ─────────────────────────────────────────────
#  HEALTH CHECK
# ─────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health():
    try:
        mongo.db.command('ping')
        return jsonify({'status': 'ok', 'db': 'connected', 'time': datetime.utcnow().isoformat()}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'db': str(e)}), 500
