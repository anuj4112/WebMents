/**
 * Database Seeder for WebMents
 * Author: Anuj Singla (2210991317)
 * Institution: Chitkara University, Rajpura, Punjab
 * 
 * This script populates the database with sample data for demonstration
 */

const mongoose = require('mongoose');
const fs = require('fs');

// Connect to MongoDB
mongoose.connect('mongodb://127.0.0.1:27017/webments')
    .then(() => console.log("✅ MongoDB Connected"))
    .catch(err => console.log("❌ MongoDB Connection Error:", err));

// Define Models
const User = mongoose.model('User', {
    name: String,
    email: String,
    password: String,
    role: String,
    city: String,
    logo: String,
    phone: String,
    address: String,
    gst: String,
    established: String,
    specialization: String,
    business_type: String,
    verified: Boolean,
    createdAt: Date,
    updatedAt: Date
});

const Product = mongoose.model('Product', {
    name: String,
    price: Number,
    category: String,
    image: String,
    manufacturerEmail: String,
    description: String,
    stock: Number,
    minOrder: Number,
    colors: [String],
    sizes: [String],
    material: String,
    gsm: String,
    createdAt: Date,
    updatedAt: Date
});

const Order = mongoose.model('Order', {
    orderId: String,
    buyerEmail: String,
    items: Array,
    total: Number,
    manufacturerEmail: String,
    status: String,
    orderDate: Date,
    expectedDelivery: Date,
    deliveredDate: Date,
    paymentMethod: String,
    shippingAddress: String,
    createdAt: Date,
    updatedAt: Date
});

// Load sample data
const sampleData = JSON.parse(fs.readFileSync('sample_data.json', 'utf8'));

// Seed function
async function seedDatabase() {
    console.log("\n" + "=".repeat(60));
    console.log("🌱 WebMents Database Seeder");
    console.log("=".repeat(60));
    console.log("\n");

    try {
        // Clear existing data
        console.log("🗑️  Clearing existing data...");
        await User.deleteMany({});
        await Product.deleteMany({});
        await Order.deleteMany({});
        console.log("✅ Existing data cleared\n");

        // Seed Users
        console.log("👥 Seeding users...");
        const users = sampleData.users.map(user => ({
            ...user,
            credits: user.role === 'buyer' ? 5 : 0,   // 5 free credits for buyers
            createdAt: new Date(),
            updatedAt: new Date()
        }));
        await User.insertMany(users);
        console.log(`✅ ${users.length} users added`);
        console.log(`   - ${users.filter(u => u.role === 'manufacturer').length} Manufacturers`);
        console.log(`   - ${users.filter(u => u.role === 'buyer').length} Buyers\n`);

        // Seed Products
        console.log("📦 Seeding products...");
        const products = sampleData.products.map(product => ({
            ...product,
            image: 'sample-product.jpg', // Placeholder image
            createdAt: new Date(),
            updatedAt: new Date()
        }));
        await Product.insertMany(products);
        console.log(`✅ ${products.length} products added`);
        
        // Count products by category
        const categories = {};
        products.forEach(p => {
            categories[p.category] = (categories[p.category] || 0) + 1;
        });
        Object.entries(categories).forEach(([cat, count]) => {
            console.log(`   - ${cat}: ${count} products`);
        });
        console.log("");

        // Seed Orders
        console.log("📋 Seeding orders...");
        const orders = sampleData.orders.map(order => ({
            ...order,
            orderDate: new Date(order.orderDate),
            expectedDelivery: new Date(order.expectedDelivery),
            deliveredDate: order.deliveredDate ? new Date(order.deliveredDate) : null,
            createdAt: new Date(),
            updatedAt: new Date()
        }));
        await Order.insertMany(orders);
        console.log(`✅ ${orders.length} orders added`);
        
        // Calculate total revenue
        const totalRevenue = orders.reduce((sum, order) => sum + order.total, 0);
        console.log(`   - Total Revenue: ₹${totalRevenue.toLocaleString('en-IN')}\n`);

        // Display statistics
        console.log("=".repeat(60));
        console.log("📊 Database Statistics");
        console.log("=".repeat(60));
        console.log(`Total Users:         ${await User.countDocuments()}`);
        console.log(`Total Products:      ${await Product.countDocuments()}`);
        console.log(`Total Orders:        ${await Order.countDocuments()}`);
        console.log(`Total Revenue:       ₹${totalRevenue.toLocaleString('en-IN')}`);
        console.log("=".repeat(60));

        // Display sample login credentials
        console.log("\n" + "=".repeat(60));
        console.log("🔑 Sample Login Credentials");
        console.log("=".repeat(60));
        console.log("\n📍 MANUFACTURERS:");
        sampleData.users.filter(u => u.role === 'manufacturer').forEach(u => {
            console.log(`   ${u.name}`);
            console.log(`   Email: ${u.email}`);
            console.log(`   Password: ${u.password}`);
            console.log(`   City: ${u.city}\n`);
        });
        
        console.log("📍 BUYERS:");
        sampleData.users.filter(u => u.role === 'buyer').forEach(u => {
            console.log(`   ${u.name}`);
            console.log(`   Email: ${u.email}`);
            console.log(`   Password: ${u.password}`);
            console.log(`   City: ${u.city}\n`);
        });
        console.log("=".repeat(60));

        console.log("\n✅ Database seeding completed successfully!\n");
        console.log("🚀 You can now start the server and login with above credentials\n");

    } catch (error) {
        console.error("\n❌ Error seeding database:", error);
    } finally {
        mongoose.connection.close();
        console.log("🔌 Database connection closed\n");
    }
}

// Run seeder
seedDatabase();
