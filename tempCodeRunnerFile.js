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
const User = mongoose.model('User',{
    name:String,
    email:String,
    password:String,
    role:String,
    city:String,
    logo:String
});

const Product = mongoose.model('Product',{
    name:String,
    price:Number,
    category:String,
    image:String,
    manufacturerEmail:String
});

const Order = mongoose.model('Order',{
    buyerEmail:String,
    items:Array,
    total:Number,
    manufacturerEmail:String
});

// ================= AUTH =================

// SIGNUP
app.post('/signup', upload.single('logo'), async(req,res)=>{
    try{
        const exist = await User.findOne({email:req.body.email});
        if(exist) return res.send("User already registered");

        await new User({
            name:req.body.name,
            email:req.body.email,
            password:req.body.password,
            role:req.body.role,
            city:req.body.city,
            logo:req.file ? req.file.filename : ""
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
        const user = await User.findOne(req.body);

        if(user) res.json({role:user.role});
        else res.json({message:"Invalid credentials"});

    }catch(err){
        console.log(err);
        res.json({message:"Server error"});
    }
});

// ================= PRODUCTS =================

// ADD PRODUCT
app.post('/add-product', upload.single('image'), async(req,res)=>{
    try{
        await new Product({
            name:req.body.name,
            price:req.body.price,
            category:req.body.category,
            manufacturerEmail:req.body.email,
            image:req.file ? req.file.filename : ""
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
        const data = await Product.find({manufacturerEmail:req.params.email});
        res.json(data);
    }catch(err){
        console.log(err);
        res.json([]);
    }
});

// 🔥 GET SINGLE PRODUCT (NEW FEATURE)
app.get('/product/:id', async (req,res)=>{
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
        await Product.findByIdAndUpdate(req.params.id,{
            name:req.body.name,
            price:req.body.price,
            category:req.body.category
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
        const data = await User.find({role:"manufacturer"});
        res.json(data);
    }catch(err){
        console.log(err);
        res.json([]);
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
        const data = await Order.find({manufacturerEmail:req.params.email});
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