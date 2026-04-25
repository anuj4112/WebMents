# WebMents Sample Data Guide

## 📊 Understanding the Sample Data

This guide explains the sample/raw data structure used in WebMents for demonstration and testing purposes.

**Author:** Anuj Singla (2210991311)  
**Institution:** Chitkara University, Rajpura, Punjab

---

## 📁 Files Overview

### 1. sample_data.json
Complete sample data in JSON format including:
- 10 Users (5 Manufacturers + 5 Buyers)
- 15 Products across 6 categories
- 5 Sample orders
- Categories, statistics, testimonials, and FAQs

### 2. seed_database.js (Node.js)
Script to populate MongoDB with sample data using Node.js

### 3. seed_database.py (Python)
Script to populate MongoDB with sample data using Python

---

## 🚀 How to Use Sample Data

### Method 1: Using Node.js Seeder

```bash
# Make sure MongoDB is running
net start MongoDB

# Run the seeder
node seed_database.js
```

### Method 2: Using Python Seeder

```bash
# Make sure MongoDB is running
net start MongoDB

# Run the seeder
python seed_database.py
```

### Method 3: Manual Import

```bash
# Import users
mongoimport --db webments --collection users --file users.json --jsonArray

# Import products
mongoimport --db webments --collection products --file products.json --jsonArray

# Import orders
mongoimport --db webments --collection orders --file orders.json --jsonArray
```

---

## 👥 Sample Users

### Manufacturers (5)

#### 1. ABC Garments Pvt Ltd
- **Email:** abc@manufacturer.com
- **Password:** test123
- **City:** Mumbai
- **Specialization:** Cotton Garments
- **Products:** T-Shirts (3 products)

#### 2. XYZ Textiles Manufacturing
- **Email:** xyz@manufacturer.com
- **Password:** test123
- **City:** Delhi
- **Specialization:** Formal Wear
- **Products:** Shirts (3 products)

#### 3. Fashion Hub Industries
- **Email:** fashion@manufacturer.com
- **Password:** test123
- **City:** Bangalore
- **Specialization:** Casual Wear
- **Products:** Jeans & Pants (3 products)

#### 4. Premium Garments Co
- **Email:** premium@manufacturer.com
- **Password:** test123
- **City:** Ludhiana
- **Specialization:** Winter Wear
- **Products:** Sweaters, Hoodies, Jackets (3 products)

#### 5. Ethnic Wear Manufacturers
- **Email:** ethnic@manufacturer.com
- **Password:** test123
- **City:** Jaipur
- **Specialization:** Traditional Wear
- **Products:** Kurtas, Nehru Jackets (3 products)

### Buyers (5)

#### 1. Wholesale Traders Pvt Ltd
- **Email:** wholesale@buyer.com
- **Password:** test123
- **City:** Mumbai
- **Business Type:** Wholesale

#### 2. Retail Chain Solutions
- **Email:** retail@buyer.com
- **Password:** test123
- **City:** Delhi
- **Business Type:** Retail Chain

#### 3. Export House International
- **Email:** export@buyer.com
- **Password:** test123
- **City:** Bangalore
- **Business Type:** Export

#### 4. Fashion Boutique Network
- **Email:** boutique@buyer.com
- **Password:** test123
- **City:** Chennai
- **Business Type:** Boutique Chain

#### 5. Online Marketplace Ventures
- **Email:** online@buyer.com
- **Password:** test123
- **City:** Pune
- **Business Type:** E-commerce

---

## 📦 Sample Products (15 Total)

### T-Shirts (3 products)
1. **Premium Cotton T-Shirt** - ₹250
   - Stock: 5000 units
   - Min Order: 100 units
   - Colors: White, Black, Navy Blue, Grey
   - Sizes: S, M, L, XL, XXL

2. **Polo Neck T-Shirt** - ₹350
   - Stock: 3000 units
   - Min Order: 50 units
   - Colors: White, Black, Red, Green

3. **V-Neck Cotton T-Shirt** - ₹280
   - Stock: 4000 units
   - Min Order: 100 units

### Shirts (3 products)
1. **Formal Dress Shirt** - ₹450
2. **Casual Check Shirt** - ₹380
3. **Denim Casual Shirt** - ₹420

### Jeans (2 products)
1. **Slim Fit Jeans** - ₹650
2. **Regular Fit Jeans** - ₹580

### Pants (1 product)
1. **Cargo Pants** - ₹550

### Winter Wear (3 products)
1. **Woolen Sweater** - ₹850
2. **Hooded Sweatshirt** - ₹680
3. **Winter Jacket** - ₹1200

### Ethnic Wear (3 products)
1. **Kurta Pajama Set** - ₹750
2. **Embroidered Kurta** - ₹950
3. **Nehru Jacket** - ₹1100

---

## 📋 Sample Orders (5 Total)

### Order 1: ORD001
- **Buyer:** Wholesale Traders
- **Manufacturer:** ABC Garments
- **Items:** 500 T-Shirts + 200 Polo Shirts
- **Total:** ₹1,95,000
- **Status:** Confirmed

### Order 2: ORD002
- **Buyer:** Retail Chain Solutions
- **Manufacturer:** XYZ Textiles
- **Items:** 300 Formal Shirts
- **Total:** ₹1,35,000
- **Status:** Shipped

### Order 3: ORD003
- **Buyer:** Export House International
- **Manufacturer:** Fashion Hub
- **Items:** 1000 Slim Fit + 800 Regular Fit Jeans
- **Total:** ₹11,14,000
- **Status:** Pending

### Order 4: ORD004
- **Buyer:** Fashion Boutique Network
- **Manufacturer:** Ethnic Wear
- **Items:** 150 Kurtas + 100 Nehru Jackets
- **Total:** ₹2,52,500
- **Status:** Delivered

### Order 5: ORD005
- **Buyer:** Online Marketplace
- **Manufacturer:** Premium Garments
- **Items:** 600 Hoodies + 400 Sweaters
- **Total:** ₹7,48,000
- **Status:** Confirmed

---

## 📊 Statistics

### Business Metrics
- **Total Manufacturers:** 5
- **Total Buyers:** 5
- **Total Products:** 15
- **Total Orders:** 5
- **Total Revenue:** ₹24,44,500
- **Average Order Value:** ₹4,88,900

### Product Distribution
- T-Shirts: 3 products (20%)
- Shirts: 3 products (20%)
- Jeans: 2 products (13%)
- Pants: 1 product (7%)
- Winter Wear: 3 products (20%)
- Ethnic Wear: 3 products (20%)

### Geographic Distribution
- Mumbai: 2 users
- Delhi: 2 users
- Bangalore: 2 users
- Ludhiana: 1 user
- Jaipur: 1 user
- Chennai: 1 user
- Pune: 1 user

---

## 🎯 Testing Scenarios

### Scenario 1: Manufacturer Workflow
1. Login as: abc@manufacturer.com
2. View existing products (3 T-Shirts)
3. Add new product
4. Edit existing product
5. Delete a product
6. View orders

### Scenario 2: Buyer Workflow
1. Login as: wholesale@buyer.com
2. Browse all manufacturers
3. Search by city: "Mumbai"
4. View ABC Garments catalogue
5. Search products: "T-Shirt"
6. View product details

### Scenario 3: Search & Filter
1. Login as buyer
2. Search manufacturers by city
3. Filter products by category
4. Search products by name
5. View multiple catalogues

### Scenario 4: Order Management
1. Login as manufacturer
2. View received orders
3. Check order details
4. Update order status (future feature)

---

## 🔧 Data Structure

### User Object
```json
{
  "name": "Company Name",
  "email": "email@example.com",
  "password": "test123",
  "role": "manufacturer|buyer",
  "city": "City Name",
  "phone": "+91-XXXXXXXXXX",
  "address": "Full Address",
  "gst": "GST Number",
  "established": "Year",
  "specialization": "Area of expertise",
  "verified": true|false
}
```

### Product Object
```json
{
  "name": "Product Name",
  "price": 250,
  "category": "Category Name",
  "manufacturerEmail": "manufacturer@example.com",
  "description": "Product description",
  "stock": 5000,
  "minOrder": 100,
  "colors": ["Color1", "Color2"],
  "sizes": ["S", "M", "L"],
  "material": "Material type",
  "gsm": "GSM value"
}
```

### Order Object
```json
{
  "orderId": "ORD001",
  "buyerEmail": "buyer@example.com",
  "manufacturerEmail": "manufacturer@example.com",
  "items": [
    {
      "productName": "Product Name",
      "quantity": 500,
      "price": 250,
      "subtotal": 125000
    }
  ],
  "total": 125000,
  "status": "pending|confirmed|shipped|delivered",
  "orderDate": "2026-04-15",
  "expectedDelivery": "2026-05-15",
  "paymentMethod": "Bank Transfer",
  "shippingAddress": "Full Address"
}
```

---

## 🎨 Categories

1. **T-Shirts** 👕
   - Casual and comfortable t-shirts
   - 3 products

2. **Shirts** 👔
   - Formal and casual shirts
   - 3 products

3. **Jeans** 👖
   - Denim jeans in various fits
   - 2 products

4. **Pants** 👖
   - Casual and formal pants
   - 1 product

5. **Winter Wear** 🧥
   - Warm clothing for winter
   - 3 products

6. **Ethnic Wear** 🥻
   - Traditional Indian clothing
   - 3 products

---

## 💡 Tips for Demonstration

### For Presentations
1. **Start with Statistics**
   - Show total users, products, orders
   - Highlight revenue numbers
   - Demonstrate market reach

2. **Show User Diversity**
   - Different cities
   - Various specializations
   - Multiple business types

3. **Demonstrate Features**
   - Search by city
   - Filter by category
   - View catalogues
   - Product management

### For Testing
1. **Test All User Types**
   - Login as different manufacturers
   - Login as different buyers
   - Test admin features (future)

2. **Test All Features**
   - Add/Edit/Delete products
   - Search and filter
   - View orders
   - Browse catalogues

3. **Test Edge Cases**
   - Empty search results
   - No products for manufacturer
   - Large orders
   - Multiple items in order

---

## 🔄 Resetting Data

### Clear All Data
```javascript
// In MongoDB shell
use webments
db.users.deleteMany({})
db.products.deleteMany({})
db.orders.deleteMany({})
```

### Re-seed Data
```bash
# Node.js
node seed_database.js

# Python
python seed_database.py
```

---

## 📈 Extending Sample Data

### Adding More Users
1. Edit `sample_data.json`
2. Add new user objects to `users` array
3. Run seeder script

### Adding More Products
1. Edit `sample_data.json`
2. Add new product objects to `products` array
3. Ensure `manufacturerEmail` matches existing user
4. Run seeder script

### Adding More Orders
1. Edit `sample_data.json`
2. Add new order objects to `orders` array
3. Ensure emails match existing users
4. Run seeder script

---

## 🎓 Educational Value

### For Students
- **Database Design:** Learn MongoDB schema design
- **Data Modeling:** Understand relationships
- **Sample Data:** See realistic business data
- **Testing:** Practice with real scenarios

### For Evaluators
- **Quick Setup:** Instant demo-ready data
- **Comprehensive:** Covers all features
- **Realistic:** Based on actual industry
- **Professional:** Well-structured data

---

## 🚀 Quick Start Commands

```bash
# 1. Start MongoDB
net start MongoDB

# 2. Seed database (choose one)
node seed_database.js
# OR
python seed_database.py

# 3. Start server (choose one)
node server.js
# OR
python run.py

# 4. Open browser
http://localhost:3000

# 5. Login with sample credentials
# See credentials above
```

---

## 📞 Support

**For Issues:**
- Check MongoDB is running
- Verify sample_data.json exists
- Ensure correct file paths
- Check console for errors

**For Questions:**
- Refer to main documentation
- Check USER_MANUAL.md
- Review TECHNICAL_GUIDE.md

---

## ✅ Verification Checklist

After seeding, verify:
- [ ] 10 users created (5 manufacturers + 5 buyers)
- [ ] 15 products created across 6 categories
- [ ] 5 orders created with correct totals
- [ ] Can login with sample credentials
- [ ] Products appear in manufacturer dashboard
- [ ] Buyers can see all manufacturers
- [ ] Search functionality works
- [ ] Orders visible to manufacturers

---

**Document Version:** 1.0  
**Last Updated:** April 22, 2026  
**Created by:** Anuj Singla  
**Institution:** Chitkara University, Rajpura, Punjab

**Happy Testing! 🎉**
