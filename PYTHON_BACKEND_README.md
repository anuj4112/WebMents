# WebMents Python Backend

## 🐍 Python Flask Implementation

This is a complete Python backend implementation for WebMents, providing the same functionality as the Node.js version.

**Author:** Anuj Singla (2210991317)  
**Institution:** Chitkara University, Rajpura, Punjab

---

## 📋 Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Server](#running-the-server)
5. [API Endpoints](#api-endpoints)
6. [Project Structure](#project-structure)
7. [Configuration](#configuration)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

---

## ✨ Features

- ✅ RESTful API with Flask
- ✅ MongoDB integration with PyMongo
- ✅ File upload handling
- ✅ CORS support
- ✅ User authentication
- ✅ Product management
- ✅ Order management
- ✅ Error handling
- ✅ Input validation
- ✅ Database indexing
- ✅ Modular code structure

---

## 📦 Prerequisites

### Required Software

**Python**
- Version: 3.8 or higher
- Download: https://www.python.org/downloads/

**MongoDB**
- Version: 4.4 or higher
- Download: https://www.mongodb.com/try/download/community

**pip**
- Usually comes with Python
- Verify: `pip --version`

### Verify Installation

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check MongoDB version
mongod --version
```

---

## 🚀 Installation

### Step 1: Navigate to Project Directory

```bash
cd webments
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (3.0.0)
- Flask-PyMongo (2.3.0)
- Flask-CORS (4.0.0)
- pymongo (4.6.1)
- bcrypt (4.1.2)
- python-dotenv (1.0.0)

### Step 4: Verify Installation

```bash
pip list
```

You should see all the packages listed above.

---

## 🏃 Running the Server

### Step 1: Start MongoDB

**Windows:**
```bash
net start MongoDB
```

**macOS:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

### Step 2: Start the Flask Server

**Option A: Using run.py (Recommended)**
```bash
python run.py
```

**Option B: Using app.py directly**
```bash
python app.py
```

**Option C: Using Flask CLI**
```bash
set FLASK_APP=app.py
set FLASK_ENV=development
flask run --port=3000
```

### Step 3: Verify Server is Running

You should see output like:
```
============================================================
Initializing Database...
============================================================
✅ MongoDB connection successful
✅ Database indexes created successfully
============================================================
Database initialization complete!
============================================================

============================================================
🚀 WebMents Backend Server
============================================================
Author: Anuj Singla (2210991317)
Institution: Chitkara University, Rajpura, Punjab
============================================================
Environment: Development
MongoDB URI: mongodb://127.0.0.1:27017/webments
Upload Folder: public/uploads
Max File Size: 5MB
============================================================
Server starting on: http://localhost:3000
============================================================

✨ Server is ready! Press Ctrl+C to stop.

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:3000
```

### Step 4: Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

---

## 📡 API Endpoints

### Authentication

#### POST /signup
Register a new user (manufacturer or buyer)

**Request:**
```
Content-Type: multipart/form-data

name: string
email: string
password: string
role: string (manufacturer | buyer)
city: string
logo: file (optional)
```

**Response:**
```
201: "User registered successfully"
400: "User already registered"
500: "Error in signup"
```

#### POST /login
Authenticate user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "role": "manufacturer",
  "email": "user@example.com",
  "name": "User Name"
}
```

### Products

#### POST /add-product
Add a new product

**Request:**
```
Content-Type: multipart/form-data

name: string
price: number
category: string
email: string (manufacturer email)
image: file
```

#### GET /products/:email
Get all products for a manufacturer

**Response:**
```json
[
  {
    "_id": "product_id",
    "name": "Product Name",
    "price": 250,
    "category": "T-Shirts",
    "image": "filename.jpg",
    "manufacturerEmail": "manufacturer@example.com"
  }
]
```

#### GET /product/:id
Get single product details

#### PUT /update-product/:id
Update product details

**Request:**
```json
{
  "name": "Updated Name",
  "price": 300,
  "category": "Updated Category"
}
```

#### DELETE /delete-product/:id
Delete a product

### Manufacturers

#### GET /manufacturers
Get all registered manufacturers

### Orders

#### POST /order
Place a new order

**Request:**
```json
{
  "buyerEmail": "buyer@example.com",
  "manufacturerEmail": "manufacturer@example.com",
  "items": [
    {
      "productId": "product_id",
      "quantity": 100,
      "price": 250
    }
  ],
  "total": 25000
}
```

#### GET /orders/:email
Get all orders for a manufacturer

---

## 📁 Project Structure

```
webments/
├── app.py                  # Main Flask application
├── run.py                  # Application runner with initialization
├── config.py               # Configuration settings
├── models.py               # Database models and schemas
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── public/                 # Frontend files
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── manufacturer.html
│   ├── buyer.html
│   └── uploads/           # Uploaded images
└── venv/                  # Virtual environment (created)
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# MongoDB Configuration
MONGO_URI=mongodb://127.0.0.1:27017/webments

# Server Configuration
PORT=3000
DEBUG=True
```

### Configuration Files

**config.py** contains three configurations:
- `DevelopmentConfig` - For development
- `ProductionConfig` - For production
- `TestingConfig` - For testing

Modify `config.py` to change settings.

---

## 🧪 Testing

### Manual Testing

**Test Signup:**
```bash
curl -X POST http://localhost:3000/signup \
  -F "name=Test User" \
  -F "email=test@example.com" \
  -F "password=test123" \
  -F "role=manufacturer" \
  -F "city=Mumbai"
```

**Test Login:**
```bash
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

**Test Get Manufacturers:**
```bash
curl http://localhost:3000/manufacturers
```

### Using Postman

1. Import the API endpoints
2. Test each endpoint
3. Verify responses

### Automated Testing (Future)

Create `tests/` directory with:
- `test_auth.py`
- `test_products.py`
- `test_orders.py`

Run tests with:
```bash
pytest
```

---

## 🚀 Deployment

### Production Setup

#### 1. Install Production Server

```bash
pip install gunicorn
```

#### 2. Create Production Configuration

Update `.env`:
```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=strong-random-secret-key
MONGO_URI=mongodb://production-db-url
```

#### 3. Run with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

### Deployment Options

#### Option 1: Heroku

```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create webments-python
heroku addons:create mongolab
git push heroku main
```

#### Option 2: DigitalOcean

1. Create Droplet (Ubuntu 20.04)
2. Install Python, pip, MongoDB
3. Clone repository
4. Install dependencies
5. Configure Nginx
6. Set up systemd service
7. Enable SSL with Let's Encrypt

#### Option 3: AWS EC2

1. Launch EC2 instance
2. Configure security groups
3. Install Python and MongoDB
4. Deploy application
5. Set up load balancer

### Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Disable DEBUG mode
- [ ] Use production MongoDB
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure monitoring
- [ ] Set up backups
- [ ] Use environment variables
- [ ] Enable rate limiting
- [ ] Configure firewall

---

## 🔧 Troubleshooting

### Issue 1: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Issue 2: MongoDB Connection Failed

**Error:**
```
pymongo.errors.ServerSelectionTimeoutError
```

**Solution:**
```bash
# Check if MongoDB is running
# Windows
net start MongoDB

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Verify connection
mongo --eval "db.version()"
```

### Issue 3: Port Already in Use

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9

# Or change port in run.py
```

### Issue 4: File Upload Not Working

**Solution:**
```bash
# Create uploads directory
mkdir public\uploads  # Windows
mkdir -p public/uploads  # macOS/Linux

# Check permissions (macOS/Linux)
chmod 755 public/uploads
```

### Issue 5: Virtual Environment Issues

**Solution:**
```bash
# Delete and recreate virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

---

## 🔄 Switching from Node.js to Python

### Steps to Switch

1. **Stop Node.js server** (Ctrl+C)
2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Python server**
   ```bash
   python run.py
   ```
4. **Frontend works the same** - No changes needed!

### Comparison

| Feature | Node.js | Python |
|---------|---------|--------|
| Framework | Express.js | Flask |
| Database | Mongoose | PyMongo |
| File Upload | Multer | Werkzeug |
| Port | 3000 | 3000 |
| API Endpoints | Same | Same |
| Frontend | Compatible | Compatible |

---

## 📚 Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)

### Tutorials
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [MongoDB with Python](https://www.mongodb.com/languages/python)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [MongoDB Compass](https://www.mongodb.com/products/compass) - Database GUI
- [VS Code](https://code.visualstudio.com/) - Code editor

---

## 🎯 Quick Commands

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start MongoDB
net start MongoDB  # Windows
brew services start mongodb-community  # macOS
sudo systemctl start mongod  # Linux

# Run server
python run.py

# Deactivate virtual environment
deactivate
```

---

## 📞 Support

**Student:** Anuj Singla  
**Roll No:** 2210991317  
**Institution:** Chitkara University, Rajpura, Punjab

**For Issues:**
- Check troubleshooting section
- Review Flask documentation
- Check MongoDB connection
- Verify Python version

---

## 🎉 Success!

Your Python backend is now running! The frontend will work exactly the same as with the Node.js backend.

**Next Steps:**
1. Test all endpoints
2. Create test accounts
3. Add products
4. Browse as buyer
5. Customize as needed

**Happy Coding! 🐍**

---

**Document Version:** 1.0  
**Last Updated:** April 22, 2026  
**Created by:** Anuj Singla
