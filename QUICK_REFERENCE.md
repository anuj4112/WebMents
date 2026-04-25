# WebMents Quick Reference Card

## 🚀 Quick Start (Choose One)

### Node.js Backend
```bash
npm install
net start MongoDB
npm run seed
npm start
```

### Python Backend
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
net start MongoDB
python seed_database.py
python run.py
```

**Access:** http://localhost:3000

---

## 🔑 Sample Login Credentials

### Manufacturers
| Email | Password | City | Products |
|-------|----------|------|----------|
| abc@manufacturer.com | test123 | Mumbai | T-Shirts |
| xyz@manufacturer.com | test123 | Delhi | Shirts |
| fashion@manufacturer.com | test123 | Bangalore | Jeans |
| premium@manufacturer.com | test123 | Ludhiana | Winter Wear |
| ethnic@manufacturer.com | test123 | Jaipur | Ethnic Wear |

### Buyers
| Email | Password | City | Type |
|-------|----------|------|------|
| wholesale@buyer.com | test123 | Mumbai | Wholesale |
| retail@buyer.com | test123 | Delhi | Retail |
| export@buyer.com | test123 | Bangalore | Export |
| boutique@buyer.com | test123 | Chennai | Boutique |
| online@buyer.com | test123 | Pune | E-commerce |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signup | Register user |
| POST | /login | Authenticate |
| POST | /add-product | Add product |
| GET | /products/:email | Get products |
| GET | /product/:id | Get single product |
| PUT | /update-product/:id | Update product |
| DELETE | /delete-product/:id | Delete product |
| GET | /manufacturers | Get all manufacturers |
| POST | /order | Place order |
| GET | /orders/:email | Get orders |

---

## 📊 Sample Data

- **Users:** 10 (5 manufacturers + 5 buyers)
- **Products:** 15 across 6 categories
- **Orders:** 5 with ₹24,44,500 revenue
- **Categories:** T-Shirts, Shirts, Jeans, Pants, Winter Wear, Ethnic Wear

---

## 🎨 Color Scheme

```css
Primary Gradient: #667eea → #764ba2
Accent: #ffd700
Background: #f5f7fb
Text: #333333
White: #ffffff
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| server.js | Node.js backend |
| app.py | Python backend |
| sample_data.json | Sample data |
| seed_database.js | Node.js seeder |
| seed_database.py | Python seeder |

---

## 🛠️ Common Commands

```bash
# Seed database
npm run seed              # Node.js
python seed_database.py   # Python

# Start server
npm start                 # Node.js
python run.py             # Python

# Check MongoDB
mongo --eval "db.version()"

# View collections
mongo webments --eval "db.users.count()"
```

---

## 📚 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| README.md | Overview | 10 min |
| PROJECT_SUMMARY.md | Quick ref | 5 min |
| PROJECT_OVERVIEW.md | Complete | 15 min |
| TECHNICAL_GUIDE.md | Implementation | 30 min |
| USER_MANUAL.md | Usage | 20 min |
| SAMPLE_DATA_README.md | Data guide | 10 min |

---

## 🎯 Testing Scenarios

### Manufacturer Test
1. Login: abc@manufacturer.com
2. View 3 existing products
3. Add new product
4. Edit product
5. Delete product

### Buyer Test
1. Login: wholesale@buyer.com
2. Search by city: "Mumbai"
3. View manufacturer catalogue
4. Search products: "T-Shirt"
5. View product details

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| MongoDB not connecting | `net start MongoDB` |
| Port 3000 in use | Kill process or change port |
| Module not found | `npm install` or `pip install -r requirements.txt` |
| Images not uploading | Check `public/uploads` exists |

---

## 📊 Project Stats

- **Lines of Code:** 2000+
- **Documentation:** 60,000+ words
- **API Endpoints:** 12+
- **Pages:** 8
- **Collections:** 3
- **Development Time:** 8 weeks

---

## 🎓 Academic Info

**Student:** Anuj Singla  
**Roll No:** 2210991317  
**Institution:** Chitkara University  
**Year:** 2026

---

## 🏆 Key Features

✅ Dual backend (Node.js + Python)  
✅ Modern UI/UX  
✅ File uploads  
✅ Search & filter  
✅ Sample data  
✅ Complete documentation  
✅ Production ready

---

## 📞 Quick Help

- **Setup Issues:** INSTALLATION_GUIDE.md
- **Usage Help:** USER_MANUAL.md
- **Technical:** TECHNICAL_GUIDE.md
- **Data:** SAMPLE_DATA_README.md

---

**Version:** 1.0 | **Date:** April 22, 2026
