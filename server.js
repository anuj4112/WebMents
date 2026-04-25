const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const multer = require('multer');

const app = express();

// ================= MIDDLEWARE =================
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// ================= DATABASE =================
mongoose.connect('mongodb://127.0.0.1:27017/webments')
.then(()=>console.log("MongoDB Connected"))
.catch(err=>console.log(err));

// ================= FILE UPLOAD =================
const storage = multer.diskStorage({
    destination: (req,file,cb)=>cb(null,'public/uploads'),
    filename: (req,file,cb)=>cb(null,Date.now()+"-"+file.originalname)
});
const upload = multer({storage});

// ================= MODELS =================
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
    specialization: String,
    credits: { type: Number, default: 0 }   // buyers get 5 free credits
});

const Product = mongoose.model('Product', {
    name: String,
    price: Number,
    category: String,
    image: String,
    manufacturerEmail: String,
    description: String,
    stock: Number,
    minOrder: Number
});

const Order = mongoose.model('Order', {
    buyerEmail: String,
    items: Array,
    total: Number,
    manufacturerEmail: String
});

// ContactUnlock: tracks which buyer has unlocked which manufacturer
const ContactUnlock = mongoose.model('ContactUnlock', {
    buyerEmail: String,
    manufacturerEmail: String,
    unlockedAt: { type: Date, default: Date.now }
});

// ================= AUTH =================

// SIGNUP
app.post('/signup', upload.single('logo'), async(req,res)=>{
    try{
        const exist = await User.findOne({email: req.body.email});
        if(exist) return res.send("User already registered");

        const isbuyer = req.body.role === 'buyer';

        await new User({
            name: req.body.name,
            email: req.body.email,
            password: req.body.password,
            role: req.body.role,
            city: req.body.city,
            logo: req.file ? req.file.filename : "",
            credits: isbuyer ? 5 : 0   // 5 free credits for buyers
        }).save();

        res.send("User registered successfully");

    }catch(err){
        console.log(err);
        res.send("Error in signup");
    }
});

// LOGIN
app.post('/login', async(req,res)=>{
    try{
        const user = await User.findOne({ email: req.body.email, password: req.body.password });

        if(user) res.json({ role: user.role, name: user.name, credits: user.credits || 0 });
        else res.json({ message: "Invalid credentials" });

    }catch(err){
        console.log(err);
        res.json({ message: "Server error" });
    }
});

// GET USER PROFILE
app.get('/profile/:email', async(req,res)=>{
    try{
        const user = await User.findOne({ email: req.params.email });
        if(!user) return res.json({ message: "User not found" });
        // never send password
        const { password, ...safe } = user.toObject();
        res.json(safe);
    }catch(err){
        console.log(err);
        res.json({});
    }
});

// UPDATE MANUFACTURER PROFILE (name, city, phone, address, gst, specialization)
app.put('/update-profile', upload.single('logo'), async(req,res)=>{
    try{
        const updateData = {
            name: req.body.name,
            city: req.body.city,
            phone: req.body.phone,
            address: req.body.address,
            gst: req.body.gst,
            specialization: req.body.specialization
        };
        if(req.file) updateData.logo = req.file.filename;

        await User.findOneAndUpdate({ email: req.body.email }, updateData);
        res.send("Profile updated successfully");
    }catch(err){
        console.log(err);
        res.send("Error updating profile");
    }
});

// ================= PRODUCTS =================

// ADD PRODUCT
app.post('/add-product', upload.single('image'), async(req,res)=>{
    try{
        await new Product({
            name: req.body.name,
            price: req.body.price,
            category: req.body.category,
            manufacturerEmail: req.body.email,
            image: req.file ? req.file.filename : "",
            description: req.body.description || "",
            stock: req.body.stock || 0,
            minOrder: req.body.minOrder || 1
        }).save();

        res.send("Product added successfully");

    }catch(err){
        console.log(err);
        res.send("Error adding product");
    }
});

// GET PRODUCTS BY MANUFACTURER
app.get('/products/:email', async(req,res)=>{
    try{
        const data = await Product.find({ manufacturerEmail: req.params.email });
        res.json(data);
    }catch(err){
        console.log(err);
        res.json([]);
    }
});

// GET SINGLE PRODUCT
app.get('/product/:id', async(req,res)=>{
    try{
        const product = await Product.findById(req.params.id);
        res.json(product);
    }catch(err){
        console.log(err);
        res.json({});
    }
});

// UPDATE PRODUCT
app.put('/update-product/:id', async(req,res)=>{
    try{
        await Product.findByIdAndUpdate(req.params.id, {
            name: req.body.name,
            price: req.body.price,
            category: req.body.category,
            description: req.body.description,
            stock: req.body.stock,
            minOrder: req.body.minOrder
        });
        res.send("Product updated");
    }catch(err){
        console.log(err);
        res.send("Error updating");
    }
});

// DELETE PRODUCT
app.delete('/delete-product/:id', async(req,res)=>{
    try{
        await Product.findByIdAndDelete(req.params.id);
        res.send("Deleted");
    }catch(err){
        console.log(err);
        res.send("Error deleting");
    }
});

// ================= MANUFACTURERS =================

// GET ALL MANUFACTURERS
app.get('/manufacturers', async(req,res)=>{
    try{
        const data = await User.find({ role: "manufacturer" });
        res.json(data);
    }catch(err){
        console.log(err);
        res.json([]);
    }
});

// ================= CREDITS & CONTACT UNLOCK =================

// ADD CREDITS TO BUYER ACCOUNT
app.post('/add-credits', async(req,res)=>{
    try{
        const { email, amount } = req.body;
        const credits = parseInt(amount) || 100;

        const user = await User.findOneAndUpdate(
            { email, role: 'buyer' },
            { $inc: { credits } },
            { new: true }
        );

        if(!user) return res.json({ success: false, message: "Buyer not found" });

        res.json({ success: true, credits: user.credits, message: `${credits} credits added successfully` });
    }catch(err){
        console.log(err);
        res.json({ success: false, message: "Error adding credits" });
    }
});

// GET BUYER CREDITS
app.get('/credits/:email', async(req,res)=>{
    try{
        const user = await User.findOne({ email: req.params.email });
        res.json({ credits: user ? (user.credits || 0) : 0 });
    }catch(err){
        res.json({ credits: 0 });
    }
});

// CHECK IF BUYER HAS ALREADY UNLOCKED A MANUFACTURER
app.get('/check-unlock/:buyerEmail/:manufacturerEmail', async(req,res)=>{
    try{
        const unlock = await ContactUnlock.findOne({
            buyerEmail: req.params.buyerEmail,
            manufacturerEmail: req.params.manufacturerEmail
        });
        res.json({ unlocked: !!unlock });
    }catch(err){
        res.json({ unlocked: false });
    }
});

// UNLOCK MANUFACTURER CONTACT (costs 1 credit)
app.post('/unlock-contact', async(req,res)=>{
    try{
        const { buyerEmail, manufacturerEmail } = req.body;

        // Check if already unlocked
        const existing = await ContactUnlock.findOne({ buyerEmail, manufacturerEmail });
        if(existing) return res.json({ success: true, message: "Already unlocked" });

        // Check buyer credits
        const buyer = await User.findOne({ email: buyerEmail });
        if(!buyer) return res.json({ success: false, message: "Buyer not found" });
        if((buyer.credits || 0) < 1) return res.json({ success: false, message: "Not enough credits" });

        // Deduct 1 credit
        await User.findOneAndUpdate({ email: buyerEmail }, { $inc: { credits: -1 } });

        // Save unlock record
        await new ContactUnlock({ buyerEmail, manufacturerEmail }).save();

        res.json({ success: true, message: "Contact unlocked!", credits: buyer.credits - 1 });

    }catch(err){
        console.log(err);
        res.json({ success: false, message: "Error unlocking contact" });
    }
});

// GET MANUFACTURER CONTACT (only if unlocked)
app.get('/manufacturer-contact/:buyerEmail/:manufacturerEmail', async(req,res)=>{
    try{
        const unlock = await ContactUnlock.findOne({
            buyerEmail: req.params.buyerEmail,
            manufacturerEmail: req.params.manufacturerEmail
        });
        if(!unlock) return res.json({ success: false, message: "Not unlocked" });

        const mfr = await User.findOne({ email: req.params.manufacturerEmail });
        if(!mfr) return res.json({ success: false, message: "Manufacturer not found" });

        res.json({
            success: true,
            phone: mfr.phone || "Not provided",
            address: mfr.address || "Not provided",
            gst: mfr.gst || "Not provided",
            email: mfr.email
        });
    }catch(err){
        res.json({ success: false, message: "Error" });
    }
});

// ================= ORDERS =================

// PLACE ORDER
app.post('/order', async(req,res)=>{
    try{
        await new Order(req.body).save();
        res.send("Order placed");
    }catch(err){
        console.log(err);
        res.send("Error placing order");
    }
});

// GET ORDERS (MANUFACTURER)
app.get('/orders/:email', async(req,res)=>{
    try{
        const data = await Order.find({ manufacturerEmail: req.params.email });
        res.json(data);
    }catch(err){
        console.log(err);
        res.json([]);
    }
});

// ================= SERVER =================
app.listen(3000, ()=>{
    console.log("Server running on http://localhost:3000");
});