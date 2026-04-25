"""
Database Models for WebMents
Author: Anuj Singla (2210991317)

This file defines the structure of MongoDB collections
"""

from datetime import datetime
from bson import ObjectId


class User:
    """User model for manufacturers, buyers, and admins"""
    
    @staticmethod
    def create(name, email, password, role, city, logo=''):
        """Create a new user document"""
        return {
            'name': name,
            'email': email,
            'password': password,  # Should be hashed in production
            'role': role,  # 'manufacturer', 'buyer', or 'admin'
            'city': city,
            'logo': logo,
            'verified': False,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
    
    @staticmethod
    def validate_role(role):
        """Validate user role"""
        return role in ['manufacturer', 'buyer', 'admin']


class Product:
    """Product model for manufacturer catalogues"""
    
    @staticmethod
    def create(name, price, category, manufacturer_email, image, stock=0, description=''):
        """Create a new product document"""
        return {
            'name': name,
            'price': float(price),
            'category': category,
            'manufacturerEmail': manufacturer_email,
            'image': image,
            'stock': stock,
            'description': description,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
    
    @staticmethod
    def update(name=None, price=None, category=None, stock=None, description=None):
        """Create update document"""
        update_doc = {'updatedAt': datetime.utcnow()}
        
        if name is not None:
            update_doc['name'] = name
        if price is not None:
            update_doc['price'] = float(price)
        if category is not None:
            update_doc['category'] = category
        if stock is not None:
            update_doc['stock'] = stock
        if description is not None:
            update_doc['description'] = description
            
        return update_doc


class Order:
    """Order model for tracking purchases"""
    
    @staticmethod
    def create(buyer_email, manufacturer_email, items, total, status='pending'):
        """Create a new order document"""
        return {
            'buyerEmail': buyer_email,
            'manufacturerEmail': manufacturer_email,
            'items': items,  # Array of {productId, name, quantity, price}
            'total': float(total),
            'status': status,  # 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
    
    @staticmethod
    def validate_status(status):
        """Validate order status"""
        return status in ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    
    @staticmethod
    def update_status(status):
        """Create status update document"""
        if not Order.validate_status(status):
            raise ValueError(f"Invalid status: {status}")
        
        return {
            'status': status,
            'updatedAt': datetime.utcnow()
        }


# Database Indexes
# These should be created when initializing the database

INDEXES = {
    'users': [
        {'keys': [('email', 1)], 'unique': True},
        {'keys': [('role', 1), ('city', 1)]},
    ],
    'products': [
        {'keys': [('manufacturerEmail', 1)]},
        {'keys': [('category', 1)]},
        {'keys': [('name', 'text')]},  # Text index for search
    ],
    'orders': [
        {'keys': [('buyerEmail', 1)]},
        {'keys': [('manufacturerEmail', 1)]},
        {'keys': [('status', 1)]},
        {'keys': [('createdAt', -1)]},
    ]
}


def create_indexes(db):
    """Create database indexes for better performance"""
    try:
        # Create indexes for users collection
        for index in INDEXES['users']:
            db.users.create_index(
                index['keys'],
                unique=index.get('unique', False)
            )
        
        # Create indexes for products collection
        for index in INDEXES['products']:
            db.products.create_index(index['keys'])
        
        # Create indexes for orders collection
        for index in INDEXES['orders']:
            db.orders.create_index(index['keys'])
        
        print("✅ Database indexes created successfully")
        
    except Exception as e:
        print(f"⚠️ Error creating indexes: {e}")


# Sample Data for Testing
SAMPLE_DATA = {
    'users': [
        {
            'name': 'ABC Garments',
            'email': 'abc@manufacturer.com',
            'password': 'test123',
            'role': 'manufacturer',
            'city': 'Mumbai',
            'logo': '',
            'verified': True,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        },
        {
            'name': 'XYZ Wholesale',
            'email': 'xyz@buyer.com',
            'password': 'test123',
            'role': 'buyer',
            'city': 'Delhi',
            'logo': '',
            'verified': True,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
    ],
    'products': [
        {
            'name': 'Cotton T-Shirt',
            'price': 250.0,
            'category': 'T-Shirts',
            'manufacturerEmail': 'abc@manufacturer.com',
            'image': 'sample-tshirt.jpg',
            'stock': 1000,
            'description': 'Premium cotton t-shirt',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
    ]
}


def insert_sample_data(db):
    """Insert sample data for testing"""
    try:
        # Check if data already exists
        if db.users.count_documents({}) > 0:
            print("⚠️ Database already contains data. Skipping sample data insertion.")
            return
        
        # Insert sample users
        db.users.insert_many(SAMPLE_DATA['users'])
        print("✅ Sample users inserted")
        
        # Insert sample products
        db.products.insert_many(SAMPLE_DATA['products'])
        print("✅ Sample products inserted")
        
        print("✅ Sample data inserted successfully")
        
    except Exception as e:
        print(f"⚠️ Error inserting sample data: {e}")
