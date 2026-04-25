"""
WebMents Backend Runner
Author: Anuj Singla (2210991317)
Institution: Chitkara University, Rajpura, Punjab

This is the main entry point for running the WebMents backend server.
"""

import os
from app import app, mongo
from models import create_indexes, insert_sample_data

def initialize_database():
    """Initialize database with indexes and sample data"""
    print("\n" + "=" * 60)
    print("Initializing Database...")
    print("=" * 60)
    
    try:
        # Test MongoDB connection
        mongo.db.command('ping')
        print("✅ MongoDB connection successful")
        
        # Create indexes
        create_indexes(mongo.db)
        
        # Optionally insert sample data (comment out if not needed)
        # insert_sample_data(mongo.db)
        
        print("=" * 60)
        print("Database initialization complete!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("Please ensure MongoDB is running on mongodb://127.0.0.1:27017")
        print("=" * 60 + "\n")
        exit(1)


def print_startup_info():
    """Print startup information"""
    print("\n" + "=" * 60)
    print("🚀 WebMents Backend Server")
    print("=" * 60)
    print(f"Author: Anuj Singla (2210991317)")
    print(f"Institution: Chitkara University, Rajpura, Punjab")
    print("=" * 60)
    print(f"Environment: {'Development' if app.debug else 'Production'}")
    print(f"MongoDB URI: {app.config['MONGO_URI']}")
    print(f"Upload Folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Max File Size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.0f}MB")
    print("=" * 60)
    print("Server starting on: http://localhost:3000")
    print("=" * 60)
    print("\n📋 Available Endpoints:")
    print("  - GET  /                    → Landing page")
    print("  - POST /signup              → User registration")
    print("  - POST /login               → User authentication")
    print("  - POST /add-product         → Add product")
    print("  - GET  /products/<email>    → Get manufacturer products")
    print("  - GET  /product/<id>        → Get single product")
    print("  - PUT  /update-product/<id> → Update product")
    print("  - DELETE /delete-product/<id> → Delete product")
    print("  - GET  /manufacturers       → Get all manufacturers")
    print("  - POST /order               → Place order")
    print("  - GET  /orders/<email>      → Get manufacturer orders")
    print("=" * 60)
    print("\n✨ Server is ready! Press Ctrl+C to stop.\n")


if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database
    initialize_database()
    
    # Print startup information
    print_startup_info()
    
    # Run the application
    try:
        app.run(
            host='0.0.0.0',
            port=3000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("🛑 Server stopped by user")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n❌ Server error: {e}\n")
