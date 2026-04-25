"""
WebMents Backend - Python Flask Implementation
Author: Anuj Singla (2210991317)
Institution: Chitkara University, Rajpura, Punjab
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__, static_folder='public', static_url_path='')

# Configuration
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/webments'
app.config['UPLOAD_FOLDER'] = 'public/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize extensions
CORS(app)
mongo = PyMongo(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ================= HELPER FUNCTIONS =================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    doc['_id'] = str(doc['_id'])
    return doc


def serialize_docs(docs):
    """Convert list of MongoDB documents to JSON-serializable list"""
    return [serialize_doc(doc) for doc in docs]


# ================= ROUTES =================

# Serve static files
@app.route('/')
def index():
    """Serve index.html"""
    return send_from_directory('public', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from public directory"""
    return send_from_directory('public', path)


# ================= AUTHENTICATION =================

@app.route('/signup', methods=['POST'])
def signup():
    """Register a new user (manufacturer or buyer)"""
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        city = request.form.get('city')
        
        # Validate required fields
        if not all([name, email, password, role, city]):
            return "All fields are required", 400
        
        # Check if user already exists
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            return "User already registered", 400
        
        # Handle logo upload
        logo_filename = ""
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to make it unique
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                logo_filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))
        
        # Create user document
        user_doc = {
            'name': name,
            'email': email,
            'password': password,  # TODO: Hash password in production
            'role': role,
            'city': city,
            'logo': logo_filename,
            'verified': False,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        # Insert user into database
        mongo.db.users.insert_one(user_doc)
        
        return "User registered successfully", 201
        
    except Exception as e:
        print(f"Signup Error: {e}")
        return "Error in signup", 500


@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and return role"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not email or not password:
            return jsonify({'message': 'Email and password required'}), 400
        
        # Find user
        user = mongo.db.users.find_one({
            'email': email,
            'password': password  # TODO: Compare hashed password in production
        })
        
        if user:
            return jsonify({
                'role': user['role'],
                'email': user['email'],
                'name': user['name']
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify({'message': 'Server error'}), 500


# ================= PRODUCTS =================

@app.route('/add-product', methods=['POST'])
def add_product():
    """Add a new product to manufacturer's catalogue"""
    try:
        # Get form data
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')
        manufacturer_email = request.form.get('email')
        
        # Validate required fields
        if not all([name, price, category, manufacturer_email]):
            return "All fields are required", 400
        
        # Handle image upload
        image_filename = ""
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                image_filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            else:
                return "Invalid image file", 400
        else:
            return "Product image is required", 400
        
        # Create product document
        product_doc = {
            'name': name,
            'price': float(price),
            'category': category,
            'manufacturerEmail': manufacturer_email,
            'image': image_filename,
            'stock': 0,
            'description': '',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        # Insert product into database
        mongo.db.products.insert_one(product_doc)
        
        return "Product added successfully", 201
        
    except Exception as e:
        print(f"Add Product Error: {e}")
        return "Error adding product", 500


@app.route('/products/<email>', methods=['GET'])
def get_products(email):
    """Get all products for a specific manufacturer"""
    try:
        products = mongo.db.products.find({
            'manufacturerEmail': email
        }).sort('createdAt', -1)
        
        return jsonify(serialize_docs(list(products))), 200
        
    except Exception as e:
        print(f"Get Products Error: {e}")
        return jsonify([]), 500


@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product details"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(product_id):
            return jsonify({'message': 'Invalid product ID'}), 400
        
        product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        return jsonify(serialize_doc(product)), 200
        
    except Exception as e:
        print(f"Get Product Error: {e}")
        return jsonify({}), 500


@app.route('/update-product/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product details"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(product_id):
            return jsonify({'message': 'Invalid product ID'}), 400
        
        data = request.get_json()
        
        # Update fields
        update_doc = {
            'name': data.get('name'),
            'price': float(data.get('price')),
            'category': data.get('category'),
            'updatedAt': datetime.utcnow()
        }
        
        # Update product
        result = mongo.db.products.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_doc}
        )
        
        if result.modified_count > 0:
            return "Product updated", 200
        else:
            return "Product not found or no changes made", 404
            
    except Exception as e:
        print(f"Update Product Error: {e}")
        return "Error updating", 500


@app.route('/delete-product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(product_id):
            return jsonify({'message': 'Invalid product ID'}), 400
        
        # Get product to delete image file
        product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
        
        if product and product.get('image'):
            # Delete image file
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], product['image'])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Delete product from database
        result = mongo.db.products.delete_one({'_id': ObjectId(product_id)})
        
        if result.deleted_count > 0:
            return "Deleted", 200
        else:
            return "Product not found", 404
            
    except Exception as e:
        print(f"Delete Product Error: {e}")
        return "Error deleting", 500


# ================= MANUFACTURERS =================

@app.route('/manufacturers', methods=['GET'])
def get_manufacturers():
    """Get all registered manufacturers"""
    try:
        manufacturers = mongo.db.users.find({'role': 'manufacturer'})
        return jsonify(serialize_docs(list(manufacturers))), 200
        
    except Exception as e:
        print(f"Get Manufacturers Error: {e}")
        return jsonify([]), 500


# ================= ORDERS =================

@app.route('/order', methods=['POST'])
def place_order():
    """Place a new order"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all([data.get('buyerEmail'), data.get('manufacturerEmail'), 
                   data.get('items'), data.get('total')]):
            return "Missing required fields", 400
        
        # Create order document
        order_doc = {
            'buyerEmail': data.get('buyerEmail'),
            'manufacturerEmail': data.get('manufacturerEmail'),
            'items': data.get('items'),
            'total': float(data.get('total')),
            'status': 'pending',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        # Insert order into database
        mongo.db.orders.insert_one(order_doc)
        
        return "Order placed", 201
        
    except Exception as e:
        print(f"Place Order Error: {e}")
        return "Error placing order", 500


@app.route('/orders/<email>', methods=['GET'])
def get_orders(email):
    """Get all orders for a manufacturer"""
    try:
        orders = mongo.db.orders.find({
            'manufacturerEmail': email
        }).sort('createdAt', -1)
        
        return jsonify(serialize_docs(list(orders))), 200
        
    except Exception as e:
        print(f"Get Orders Error: {e}")
        return jsonify([]), 500


# ================= ERROR HANDLERS =================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'message': 'Route not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({'message': 'Internal server error'}), 500


@app.errorhandler(413)
def request_entity_too_large(e):
    """Handle file too large errors"""
    return jsonify({'message': 'File too large. Maximum size is 5MB'}), 413


# ================= MAIN =================

if __name__ == '__main__':
    print("=" * 50)
    print("WebMents Backend - Python Flask")
    print("=" * 50)
    print("Starting server...")
    print("MongoDB URI: mongodb://127.0.0.1:27017/webments")
    print("Server will run on: http://localhost:3000")
    print("=" * 50)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=3000,
        debug=True
    )
