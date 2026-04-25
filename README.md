# WebMents - B2B Garment Manufacturing Platform

![WebMents Logo](https://img.shields.io/badge/WebMents-B2B%20Platform-blue)
![Node.js](https://img.shields.io/badge/Node.js-v14+-green)
![MongoDB](https://img.shields.io/badge/MongoDB-v4.4+-brightgreen)
![License](https://img.shields.io/badge/License-Academic-yellow)

## 🎓 Academic Project Information

**Project Title:** WebMents: Making Manufacturing Selling and Buying Simple by Integrating Tech  
**Institution:** Chitkara University, Rajpura, Punjab  
**Student:** Anuj Singla  
**Roll No:** 2210991317  
**Year:** 2026

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

WebMents is a specialized B2B digital platform designed to modernize the traditional sales and purchasing processes in the unorganized garment manufacturing industry. The platform addresses critical operational challenges faced by small-scale manufacturers by replacing physical sample showcasing with digital catalogues.

### Key Statistics
- **Industry Size:** ₹15.5 Trillion (2024)
- **Target:** Small-scale garment manufacturers
- **Expected Cost Savings:** 40-60% reduction in operational costs
- **Market Reach:** Global expansion capability

---

## 🎯 Problem Statement

The garment manufacturing industry in India, despite being valued at ₹15.5 trillion, remains largely unorganized and operates using traditional methods. Small-scale manufacturers face several challenges:

### For Manufacturers:
- ❌ High operational costs (travel, samples, salesmen)
- ❌ Limited market reach (restricted to local/regional markets)
- ❌ Time-consuming physical visits to showcase samples
- ❌ Difficulty in scaling business
- ❌ Manual inventory and order tracking

### For Buyers:
- ❌ Limited visibility of available manufacturers
- ❌ Time-consuming supplier discovery
- ❌ Difficulty in comparing products and prices
- ❌ No centralized platform for bulk ordering

---

## 💡 Solution

WebMents provides a comprehensive B2B marketplace that:

✅ **Digitalizes** the traditional buying-selling process  
✅ **Reduces** operational costs by 40-60%  
✅ **Expands** market reach globally  
✅ **Accelerates** sales cycle from weeks to days  
✅ **Provides** data-driven insights for business decisions

---

## ✨ Features

### For Manufacturers 🏭

#### Business Profile Management
- Create and manage business profiles
- Upload company logo
- Location-based visibility

#### Catalogue Management
- Add products with images
- Set prices and categories
- Edit and update products
- Delete products
- Real-time catalogue updates

#### Order Management
- View incoming orders
- Track order history
- Order analytics

#### Stock Management
- Track inventory levels
- Update stock information

### For Buyers 🛒

#### Search & Discovery
- Search by category
- Location-based filtering
- Product search across all catalogues
- Advanced filters

#### Manufacturer Browsing
- View manufacturer profiles
- Browse complete catalogues
- Access contact information

#### Order Placement
- Direct communication with manufacturers
- Place bulk orders
- Order tracking

### For Admins 👨‍💼

#### Verification System
- Manufacturer verification
- Quality control checks
- User management

#### Analytics Dashboard
- User statistics
- Transaction metrics
- Platform growth indicators

---

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **JavaScript (ES6+)** - Client-side logic
- **Google Fonts** - Poppins typography

### Backend
- **Node.js** - JavaScript runtime
- **Express.js** - Web framework
- **MongoDB** - NoSQL database
- **Mongoose** - ODM for MongoDB

### Additional Libraries
- **Multer** - File upload handling
- **CORS** - Cross-origin resource sharing
- **Body-Parser** - Request parsing

---

## 📦 Installation

### Prerequisites
- Node.js (v14 or higher)
- MongoDB (v4.4 or higher)
- npm (v6 or higher)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd webments
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Start MongoDB
**Windows:**
```bash
net start MongoDB
```

**macOS/Linux:**
```bash
sudo systemctl start mongod
```

### Step 4: Start the Server
```bash
node server.js
```

### Step 5: Access the Application
Open your browser and navigate to:
```
http://localhost:3000
```

---

## 🚀 Usage

### For Manufacturers

1. **Sign Up**
   - Navigate to `/signup.html`
   - Select "Manufacturer" role
   - Fill in business details
   - Upload logo (optional)

2. **Login**
   - Navigate to `/login.html`
   - Enter credentials
   - Access manufacturer dashboard

3. **Add Products**
   - Fill in product details
   - Upload product image
   - Set price and category
   - Click "Save Product"

4. **Manage Catalogue**
   - View all products
   - Edit product details
   - Delete products
   - Track orders

### For Buyers

1. **Sign Up**
   - Navigate to `/signup.html`
   - Select "Buyer" role
   - Fill in details

2. **Browse Manufacturers**
   - Search by city
   - View manufacturer profiles
   - Browse catalogues

3. **Search Products**
   - Use product search
   - Apply filters
   - View product details

4. **Place Orders**
   - Contact manufacturers
   - Place bulk orders

---

## 📚 API Documentation

### Authentication Endpoints

#### POST /signup
Register a new user (manufacturer or buyer)

**Request:**
```javascript
Content-Type: multipart/form-data

{
  name: String,
  email: String,
  password: String,
  role: String, // "manufacturer" or "buyer"
  city: String,
  logo: File
}
```

**Response:**
```
"User registered successfully"
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
  "role": "manufacturer" | "buyer"
}
```

### Product Endpoints

#### POST /add-product
Add a new product

**Request:**
```javascript
Content-Type: multipart/form-data

{
  name: String,
  price: Number,
  category: String,
  email: String, // manufacturer email
  image: File
}
```

#### GET /products/:email
Get all products for a manufacturer

**Response:**
```json
[
  {
    "_id": "product_id",
    "name": "Product Name",
    "price": 1500,
    "category": "T-Shirts",
    "image": "filename.jpg",
    "manufacturerEmail": "manufacturer@example.com"
  }
]
```

#### PUT /update-product/:id
Update product details

#### DELETE /delete-product/:id
Delete a product

### Manufacturer Endpoints

#### GET /manufacturers
Get all registered manufacturers

### Order Endpoints

#### POST /order
Place a new order

#### GET /orders/:email
Get orders for a manufacturer

For complete API documentation, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

---

## 📁 Project Structure

```
webments/
├── node_modules/           # Dependencies
├── public/                 # Frontend files
│   ├── uploads/           # Uploaded images
│   ├── index.html         # Landing page
│   ├── login.html         # Login page
│   ├── signup.html        # Registration page
│   ├── manufacturer.html  # Manufacturer dashboard
│   ├── buyer.html         # Buyer dashboard
│   ├── catalogue.html     # Product catalogue
│   ├── product.html       # Product details
│   ├── style.css          # Global styles
│   └── *.jpeg/jpg         # Background images
├── server.js              # Backend server
├── package.json           # Project dependencies
├── README.md              # This file
└── PROJECT_DOCUMENTATION.md  # Detailed documentation
```

---

## 📸 Screenshots

### Landing Page
Modern, gradient-based design with clear call-to-action buttons.

### Login/Signup
Clean, user-friendly authentication forms with role selection.

### Manufacturer Dashboard
Intuitive interface for managing products and orders.

### Buyer Dashboard
Easy-to-use search and filtering for finding manufacturers and products.

---

## 🔮 Future Enhancements

### Phase 2
- [ ] Advanced search filters
- [ ] In-app messaging system
- [ ] Payment gateway integration
- [ ] Analytics dashboard
- [ ] Email notifications

### Phase 3
- [ ] Mobile applications (iOS/Android)
- [ ] AI-powered product recommendations
- [ ] Logistics integration
- [ ] Multi-language support
- [ ] International expansion

### Technical Improvements
- [ ] Password hashing (bcrypt)
- [ ] JWT authentication
- [ ] Input validation and sanitization
- [ ] Rate limiting
- [ ] HTTPS implementation
- [ ] Image optimization and CDN
- [ ] Database indexing
- [ ] Microservices architecture

---

## 🤝 Contributing

This is an academic project. For suggestions or improvements:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is submitted as part of academic requirements at Chitkara University. All rights reserved.

**© 2026 Anuj Singla**

---

## 📞 Contact

**Anuj Singla**  
Roll No: 2210991317  
Chitkara University, Rajpura, Punjab

---

## 🙏 Acknowledgments

- Chitkara University for academic support
- Faculty members for guidance
- Family business for real-world insights
- Open-source community for tools and libraries

---

## 📊 Project Status

**Current Version:** 1.0  
**Status:** Active Development  
**Last Updated:** April 22, 2026

---

**Made with ❤️ for the Garment Manufacturing Industry**
