"""
WebMents - Seed Database
Author: Anuj Singla (2210991317)

Populates MongoDB with realistic sample data:
  - 6 manufacturers across Indian cities
  - 1 buyer account
  - 30+ products across categories
  - Some contact unlocks and orders

Run:  python seed_database.py
"""

from pymongo import MongoClient, ASCENDING, TEXT
from datetime import datetime, timedelta
from bson import ObjectId
import bcrypt
import random

MONGO_URI = 'mongodb://127.0.0.1:27017/webments'
client    = MongoClient(MONGO_URI)
db        = client['webments']


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def pw(plain):
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def ago(days=0, hours=0):
    return datetime.utcnow() - timedelta(days=days, hours=hours)


# ─────────────────────────────────────────────
#  CLEAR EXISTING DATA
# ─────────────────────────────────────────────

def clear():
    db.users.delete_many({})
    db.products.delete_many({})
    db.orders.delete_many({})
    db.contact_unlocks.delete_many({})
    print('🗑️  Cleared existing data')


# ─────────────────────────────────────────────
#  INDEXES
# ─────────────────────────────────────────────

def create_indexes():
    db.users.create_index([('email', ASCENDING)], unique=True)
    db.users.create_index([('role', ASCENDING), ('city', ASCENDING)])
    db.products.create_index([('manufacturerEmail', ASCENDING)])
    db.products.create_index([('category', ASCENDING)])
    db.products.create_index([('name', TEXT), ('description', TEXT)])
    db.orders.create_index([('buyerEmail', ASCENDING)])
    db.orders.create_index([('manufacturerEmail', ASCENDING)])
    db.orders.create_index([('status', ASCENDING)])
    db.contact_unlocks.create_index(
        [('buyerEmail', ASCENDING), ('manufacturerEmail', ASCENDING)], unique=True
    )
    print('📑  Indexes created')


# ─────────────────────────────────────────────
#  USERS
# ─────────────────────────────────────────────

MANUFACTURERS = [
    {
        'name':           'Sharma Garments Pvt Ltd',
        'email':          'sharma@manufacturer.com',
        'password':       pw('test123'),
        'role':           'manufacturer',
        'city':           'Mumbai',
        'logo':           '',
        'phone':          '+91-9876543210',
        'address':        '14, Dharavi Industrial Area, Mumbai - 400017',
        'gst':            '27AABCS1429B1ZB',
        'specialization': 'T-Shirts & Casual Wear',
        'credits':        0,
        'verified':       True,
        'createdAt':      ago(60),
        'updatedAt':      ago(5)
    },
    {
        'name':           'Rajput Textiles',
        'email':          'rajput@manufacturer.com',
        'password':       pw('test123'),
        'role':           'manufacturer',
        'city':           'Surat',
        'logo':           '',
        'phone':          '+91-9812345678',
        'address':        '22, Ring Road, Surat Textile Market, Surat - 395002',
        'gst':            '24AABCR5678D1ZA',
        'specialization': 'Sarees & Ethnic Wear',
        'credits':        0,
        'verified':       True,
        'createdAt':      ago(55),
        'updatedAt':      ago(3)
    },
    {
        'name':           'Delhi Denim Co.',
        'email':          'delhidenim@manufacturer.com',
        'password':       pw('test123'),
        'role':           'manufacturer',
        'city':           'Delhi',
        'logo':           '',
        'phone':          '+91-9911223344',
        'address':        'Plot 7, Okhla Industrial Estate Phase II, New Delhi - 110020',
        'gst':            '07AABCD1234E1ZC',
        'specialization': 'Denim & Jeans',
        'credits':        0,
        'verified':       True,
        'createdAt':      ago(45),
        'updatedAt':      ago(2)
    },
    {
        'name':           'Tirupur Knits',
        'email':          'tirupur@manufacturer.com',
        'password':       pw('test123'),
        'role':           'manufacturer',
        'city':           'Tirupur',
        'logo':           '',
        'phone':          '+91-9944556677',
        'address':        '88, Avinashi Road, Tirupur - 641604',
        'gst':            '33AABCT9988F1ZD',
        'specialization': 'Knitwear & Sportswear',
        'credits':        0,
        'verified':       True,
        'createdAt':      ago(40),
        'updatedAt':      ago(1)
    },
    {
        'name':           'Jaipur Craft House',
        'email':          'jaipur@manufacturer.com',
        'password':       pw('test123'),
        'role':           'manufacturer',
        'city':           'Jaipur',
        'logo':           '',
        'phone':          '+91-9001122334',
        'address':        'B-12, Sitapura Industrial Area, Jaipur - 302022',
        'gst':            '08AABCJ4567G1ZE',
        'specialization': 'Handloom & Embroidery',
        'credits':        0,
        'verified':       True,
        'createdAt':      ago(35),
        'updatedAt':      ago(4)
    },
    {
        'name':           'Ludhiana Woollens',
        'email':          'ludhiana@manufacturer.com',
        'password':       pw('test123'),
        'role':           'manufacturer',
        'city':           'Ludhiana',
        'logo':           '',
        'phone':          '+91-9855667788',
        'address':        'G.T. Road, Focal Point, Ludhiana - 141010',
        'gst':            '03AABCL7890H1ZF',
        'specialization': 'Woollens & Winter Wear',
        'credits':        0,
        'verified':       True,
        'createdAt':      ago(30),
        'updatedAt':      ago(6)
    }
]

BUYERS = [
    {
        'name':      'Rahul Wholesale',
        'email':     'rahul@buyer.com',
        'password':  pw('test123'),
        'role':      'buyer',
        'city':      'Pune',
        'logo':      '',
        'phone':     '+91-9700112233',
        'address':   '45, MG Road, Pune - 411001',
        'gst':       '',
        'credits':   25,
        'verified':  True,
        'createdAt': ago(20),
        'updatedAt': ago(1)
    },
    {
        'name':      'Priya Fashion Store',
        'email':     'priya@buyer.com',
        'password':  pw('test123'),
        'role':      'buyer',
        'city':      'Bangalore',
        'logo':      '',
        'phone':     '+91-9600223344',
        'address':   '12, Commercial Street, Bangalore - 560001',
        'gst':       '',
        'credits':   10,
        'verified':  True,
        'createdAt': ago(15),
        'updatedAt': ago(2)
    }
]


def seed_users():
    result = db.users.insert_many(MANUFACTURERS + BUYERS)
    print(f'👤  Inserted {len(result.inserted_ids)} users')
    return {u['email']: u for u in MANUFACTURERS + BUYERS}


# ─────────────────────────────────────────────
#  PRODUCTS
# ─────────────────────────────────────────────

def make_products(mfr_email, items):
    now = datetime.utcnow()
    return [
        {
            'name':              p['name'],
            'price':             p['price'],
            'category':          p['category'],
            'manufacturerEmail': mfr_email,
            'image':             '',
            'description':       p.get('desc', ''),
            'stock':             p.get('stock', random.randint(100, 2000)),
            'minOrder':          p.get('min', random.choice([10, 25, 50])),
            'createdAt':         now - timedelta(days=random.randint(1, 30)),
            'updatedAt':         now
        }
        for p in items
    ]


PRODUCT_DATA = {
    'sharma@manufacturer.com': [
        {'name': 'Premium Cotton Round-Neck T-Shirt', 'price': 180, 'category': 'T-Shirts',
         'desc': '180 GSM 100% combed cotton, pre-shrunk, available in 12 colours.', 'stock': 5000, 'min': 50},
        {'name': 'Polo Collar T-Shirt', 'price': 240, 'category': 'T-Shirts',
         'desc': 'Pique fabric polo with 3-button placket, ideal for corporate gifting.', 'stock': 3000, 'min': 25},
        {'name': 'Oversized Drop-Shoulder Tee', 'price': 320, 'category': 'T-Shirts',
         'desc': 'Trendy oversized fit, 220 GSM, unisex sizing S–3XL.', 'stock': 1500, 'min': 20},
        {'name': 'Printed Graphic T-Shirt', 'price': 210, 'category': 'T-Shirts',
         'desc': 'DTG printed, fade-resistant ink, 100% cotton.', 'stock': 2000, 'min': 30},
        {'name': 'Casual Linen Shirt', 'price': 450, 'category': 'Shirts',
         'desc': '55% linen 45% cotton blend, breathable summer shirt.', 'stock': 800, 'min': 20},
    ],
    'rajput@manufacturer.com': [
        {'name': 'Banarasi Silk Saree', 'price': 2800, 'category': 'Sarees',
         'desc': 'Pure Banarasi silk with zari border, 6.3 metres.', 'stock': 200, 'min': 5},
        {'name': 'Georgette Printed Saree', 'price': 950, 'category': 'Sarees',
         'desc': 'Lightweight georgette with digital print, blouse piece included.', 'stock': 600, 'min': 10},
        {'name': 'Cotton Handloom Saree', 'price': 650, 'category': 'Sarees',
         'desc': 'Handwoven cotton, natural dyes, eco-friendly.', 'stock': 400, 'min': 10},
        {'name': 'Anarkali Suit Set', 'price': 1200, 'category': 'Ethnic Wear',
         'desc': 'Full flared anarkali with dupatta, sizes XS–3XL.', 'stock': 300, 'min': 10},
        {'name': 'Lehenga Choli Set', 'price': 3500, 'category': 'Ethnic Wear',
         'desc': 'Embroidered lehenga with matching choli and dupatta.', 'stock': 150, 'min': 5},
    ],
    'delhidenim@manufacturer.com': [
        {'name': 'Slim Fit Stretch Jeans', 'price': 580, 'category': 'Jeans',
         'desc': '98% cotton 2% elastane, 5-pocket slim fit, 30–40 waist.', 'stock': 2000, 'min': 20},
        {'name': 'Regular Fit Classic Jeans', 'price': 480, 'category': 'Jeans',
         'desc': 'Classic 5-pocket regular fit, stonewash finish.', 'stock': 2500, 'min': 25},
        {'name': 'Skinny Ripped Jeans', 'price': 620, 'category': 'Jeans',
         'desc': 'Distressed skinny jeans, mid-rise, ankle length.', 'stock': 1200, 'min': 15},
        {'name': 'Denim Jacket', 'price': 850, 'category': 'Jackets',
         'desc': 'Classic trucker jacket, 12 oz denim, button front.', 'stock': 800, 'min': 10},
        {'name': 'Cargo Pants', 'price': 520, 'category': 'Trousers',
         'desc': '6-pocket cargo, cotton twill, relaxed fit.', 'stock': 1500, 'min': 20},
    ],
    'tirupur@manufacturer.com': [
        {'name': 'Dry-Fit Sports T-Shirt', 'price': 220, 'category': 'Sportswear',
         'desc': '100% polyester moisture-wicking, UPF 30+.', 'stock': 4000, 'min': 50},
        {'name': 'Compression Shorts', 'price': 280, 'category': 'Sportswear',
         'desc': '4-way stretch compression shorts, anti-odour treatment.', 'stock': 2000, 'min': 30},
        {'name': 'Fleece Hoodie', 'price': 480, 'category': 'Sweatshirts',
         'desc': '320 GSM fleece, kangaroo pocket, unisex.', 'stock': 1500, 'min': 20},
        {'name': 'Ribbed Crew-Neck Sweatshirt', 'price': 380, 'category': 'Sweatshirts',
         'desc': 'French terry fabric, ribbed cuffs and hem.', 'stock': 1800, 'min': 25},
        {'name': 'Track Pants', 'price': 320, 'category': 'Sportswear',
         'desc': 'Polyester track pants with side stripe, elastic waist.', 'stock': 2500, 'min': 30},
        {'name': 'Cycling Jersey', 'price': 550, 'category': 'Sportswear',
         'desc': 'Full-zip cycling jersey, 3 rear pockets, reflective strips.', 'stock': 600, 'min': 10},
    ],
    'jaipur@manufacturer.com': [
        {'name': 'Block Print Kurta', 'price': 680, 'category': 'Kurtas',
         'desc': 'Hand block-printed cotton kurta, Rajasthani motifs.', 'stock': 500, 'min': 10},
        {'name': 'Embroidered Nehru Jacket', 'price': 1400, 'category': 'Jackets',
         'desc': 'Silk blend Nehru jacket with hand embroidery.', 'stock': 200, 'min': 5},
        {'name': 'Bandhani Dupatta', 'price': 350, 'category': 'Accessories',
         'desc': 'Traditional tie-dye bandhani, pure cotton, 2.5m.', 'stock': 800, 'min': 20},
        {'name': 'Jaipuri Quilt (Razai)', 'price': 1200, 'category': 'Home Textiles',
         'desc': 'Hand-stitched cotton quilt with floral print, double size.', 'stock': 300, 'min': 5},
        {'name': 'Mirror Work Blouse', 'price': 480, 'category': 'Ethnic Wear',
         'desc': 'Cotton blouse with traditional mirror and thread work.', 'stock': 400, 'min': 10},
    ],
    'ludhiana@manufacturer.com': [
        {'name': 'Merino Wool Sweater', 'price': 1800, 'category': 'Sweaters',
         'desc': '100% merino wool, crew neck, machine washable.', 'stock': 600, 'min': 10},
        {'name': 'Acrylic V-Neck Pullover', 'price': 650, 'category': 'Sweaters',
         'desc': 'Soft acrylic blend, V-neck, available in 8 colours.', 'stock': 1200, 'min': 20},
        {'name': 'Woollen Shawl', 'price': 900, 'category': 'Accessories',
         'desc': 'Pure wool shawl, 200x70 cm, traditional Ludhiana weave.', 'stock': 400, 'min': 10},
        {'name': 'Thermal Inner Set', 'price': 420, 'category': 'Innerwear',
         'desc': 'Waffle-knit thermal top + bottom set, sizes S–XXL.', 'stock': 2000, 'min': 25},
        {'name': 'Fleece Jacket', 'price': 780, 'category': 'Jackets',
         'desc': 'Anti-pill fleece, full-zip, two side pockets.', 'stock': 900, 'min': 15},
    ]
}


def seed_products():
    all_products = []
    for email, items in PRODUCT_DATA.items():
        all_products.extend(make_products(email, items))
    result = db.products.insert_many(all_products)
    print(f'📦  Inserted {len(result.inserted_ids)} products')
    return list(db.products.find())


# ─────────────────────────────────────────────
#  CONTACT UNLOCKS
# ─────────────────────────────────────────────

def seed_unlocks():
    unlocks = [
        {'buyerEmail': 'rahul@buyer.com',  'manufacturerEmail': 'sharma@manufacturer.com',   'unlockedAt': ago(10)},
        {'buyerEmail': 'rahul@buyer.com',  'manufacturerEmail': 'delhidenim@manufacturer.com','unlockedAt': ago(8)},
        {'buyerEmail': 'priya@buyer.com',  'manufacturerEmail': 'tirupur@manufacturer.com',   'unlockedAt': ago(5)},
        {'buyerEmail': 'priya@buyer.com',  'manufacturerEmail': 'jaipur@manufacturer.com',    'unlockedAt': ago(3)},
    ]
    db.contact_unlocks.insert_many(unlocks)
    print(f'🔓  Inserted {len(unlocks)} contact unlocks')


# ─────────────────────────────────────────────
#  ORDERS
# ─────────────────────────────────────────────

def seed_orders(products):
    def find_products(mfr_email, count=2):
        return [p for p in products if p['manufacturerEmail'] == mfr_email][:count]

    def make_order(buyer, mfr_email, status, days_ago):
        prods = find_products(mfr_email)
        if not prods:
            return None
        items = [
            {'productId': str(p['_id']), 'name': p['name'],
             'quantity': random.randint(50, 200), 'price': p['price']}
            for p in prods
        ]
        total = sum(i['quantity'] * i['price'] for i in items)
        return {
            'buyerEmail':        buyer,
            'manufacturerEmail': mfr_email,
            'items':             items,
            'total':             total,
            'status':            status,
            'createdAt':         ago(days_ago),
            'updatedAt':         ago(max(0, days_ago - 2))
        }

    orders_data = [
        ('rahul@buyer.com',  'sharma@manufacturer.com',    'delivered',  15),
        ('rahul@buyer.com',  'delhidenim@manufacturer.com','shipped',     7),
        ('rahul@buyer.com',  'tirupur@manufacturer.com',   'confirmed',   3),
        ('rahul@buyer.com',  'sharma@manufacturer.com',    'pending',     1),
        ('priya@buyer.com',  'tirupur@manufacturer.com',   'delivered',  12),
        ('priya@buyer.com',  'jaipur@manufacturer.com',    'confirmed',   5),
        ('priya@buyer.com',  'ludhiana@manufacturer.com',  'pending',     2),
    ]

    orders = [make_order(b, m, s, d) for b, m, s, d in orders_data]
    orders = [o for o in orders if o]
    db.orders.insert_many(orders)
    print(f'🛒  Inserted {len(orders)} orders')


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print('\n' + '='*55)
    print('  WebMents — Database Seeder')
    print('='*55)

    try:
        client.admin.command('ping')
        print('✅  MongoDB connected\n')
    except Exception as e:
        print(f'❌  Cannot connect to MongoDB: {e}')
        print('    Make sure MongoDB is running on port 27017')
        exit(1)

    clear()
    create_indexes()
    seed_users()
    products = seed_products()
    seed_unlocks()
    seed_orders(products)

    print('\n' + '='*55)
    print('✅  Seeding complete!')
    print('='*55)
    print('\n📋  Test Accounts:')
    print('  Buyer:        rahul@buyer.com       / test123')
    print('  Buyer:        priya@buyer.com       / test123')
    print('  Manufacturer: sharma@manufacturer.com / test123')
    print('  Manufacturer: rajput@manufacturer.com / test123')
    print('  Manufacturer: delhidenim@manufacturer.com / test123')
    print('  Manufacturer: tirupur@manufacturer.com / test123')
    print('  Manufacturer: jaipur@manufacturer.com / test123')
    print('  Manufacturer: ludhiana@manufacturer.com / test123')
    print('\n  All passwords: test123')
    print('='*55 + '\n')
