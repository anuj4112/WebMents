# WebMents Installation Guide

## Quick Start Guide for Setting Up WebMents

This guide will help you install and run WebMents on your local machine.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Production Deployment](#production-deployment)

---

## 1. Prerequisites

### Required Software

#### Node.js
- **Version:** 14.0.0 or higher
- **Download:** https://nodejs.org/
- **Verify Installation:**
  ```bash
  node --version
  npm --version
  ```

#### MongoDB
- **Version:** 4.4 or higher
- **Download:** https://www.mongodb.com/try/download/community
- **Verify Installation:**
  ```bash
  mongod --version
  ```

#### Git (Optional)
- **Download:** https://git-scm.com/
- **Verify Installation:**
  ```bash
  git --version
  ```

### System Requirements

**Minimum:**
- RAM: 4GB
- Storage: 500MB free space
- OS: Windows 10, macOS 10.14+, or Linux

**Recommended:**
- RAM: 8GB or more
- Storage: 1GB free space
- SSD for better performance

---

## 2. Installation Steps

### Step 1: Download/Clone Project

**Option A: Download ZIP**
1. Download project ZIP file
2. Extract to desired location
3. Open terminal in extracted folder

**Option B: Clone with Git**
```bash
git clone <repository-url>
cd webments
```

### Step 2: Install Dependencies

Open terminal in project directory and run:

```bash
npm install
```

This will install:
- express (v5.2.1)
- mongoose (v9.4.1)
- cors (v2.8.6)
- body-parser (v2.2.2)
- multer (v2.1.1)

**Expected Output:**
```
added 50 packages, and audited 51 packages in 10s
```

### Step 3: Verify Installation

Check if all dependencies are installed:

```bash
npm list --depth=0
```

**Expected Output:**
```
webments@1.0.0
├── body-parser@2.2.2
├── cors@2.8.6
├── express@5.2.1
├── mongoose@9.4.1
└── multer@2.1.1
```

---

## 3. Configuration

### Step 1: Create Uploads Directory

The uploads directory should already exist. If not, create it:

**Windows:**
```bash
mkdir public\uploads
```

**macOS/Linux:**
```bash
mkdir -p public/uploads
```

### Step 2: Configure MongoDB

**Default Configuration:**
- Host: localhost (127.0.0.1)
- Port: 27017
- Database: webments

**Custom Configuration (Optional):**

Edit `server.js` line 13:
```javascript
mongoose.connect('mongodb://127.0.0.1:27017/webments')
```

Change to your MongoDB connection string if different.

### Step 3: Environment Variables (Optional)

Create `.env` file in project root:

```env
PORT=3000
MONGODB_URI=mongodb://127.0.0.1:27017/webments
NODE_ENV=development
```

**Note:** Current version doesn't use .env file. This is for future enhancement.

---

## 4. Running the Application

### Step 1: Start MongoDB

**Windows:**

**Option A: As Service**
```bash
net start MongoDB
```

**Option B: Manual Start**
```bash
"C:\Program Files\MongoDB\Server\4.4\bin\mongod.exe" --dbpath="C:\data\db"
```

**macOS:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

**Verify MongoDB is Running:**
```bash
mongo --eval "db.version()"
```

### Step 2: Start Application Server

In project directory, run:

```bash
node server.js
```

**Expected Output:**
```
MongoDB Connected
Server running on http://localhost:3000
```

### Step 3: Access Application

Open your web browser and navigate to:
```
http://localhost:3000
```

You should see the WebMents landing page.

---

## 5. Verification

### Test Checklist

#### Backend Verification
- [ ] MongoDB is running
- [ ] Server starts without errors
- [ ] Console shows "MongoDB Connected"
- [ ] Console shows "Server running on http://localhost:3000"

#### Frontend Verification
- [ ] Landing page loads
- [ ] Images display correctly
- [ ] Navigation works
- [ ] Signup page accessible
- [ ] Login page accessible

#### Functionality Verification
- [ ] Can register new user
- [ ] Can login successfully
- [ ] Manufacturer can add products
- [ ] Buyer can view manufacturers
- [ ] Search functionality works
- [ ] Images upload successfully

### Quick Test

**Test Manufacturer Flow:**
1. Go to http://localhost:3000
2. Click "Get Started"
3. Select "Manufacturer"
4. Fill in details and signup
5. Login with credentials
6. Add a test product
7. Verify product appears in list

**Test Buyer Flow:**
1. Logout from manufacturer account
2. Signup as buyer
3. Login as buyer
4. Search for manufacturers
5. Browse products
6. Test search functionality

---

## 6. Troubleshooting

### Common Issues

#### Issue 1: MongoDB Connection Failed

**Error Message:**
```
MongoServerError: connect ECONNREFUSED 127.0.0.1:27017
```

**Solutions:**
1. Check if MongoDB is running:
   ```bash
   # Windows
   tasklist | findstr mongod
   
   # macOS/Linux
   ps aux | grep mongod
   ```

2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # macOS
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```

3. Check MongoDB port:
   ```bash
   netstat -an | findstr 27017
   ```

4. Verify MongoDB installation:
   ```bash
   mongod --version
   ```

#### Issue 2: Port Already in Use

**Error Message:**
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solutions:**

**Option A: Kill Process Using Port**

**Windows:**
```bash
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:3000 | xargs kill -9
```

**Option B: Change Port**

Edit `server.js`:
```javascript
const PORT = 3001; // Change to different port
```

#### Issue 3: Module Not Found

**Error Message:**
```
Error: Cannot find module 'express'
```

**Solution:**
```bash
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install
```

#### Issue 4: File Upload Not Working

**Error Message:**
```
Error: ENOENT: no such file or directory, open 'public/uploads/...'
```

**Solution:**
```bash
# Create uploads directory
mkdir public/uploads

# Check directory permissions (macOS/Linux)
chmod 755 public/uploads
```

#### Issue 5: Images Not Displaying

**Possible Causes:**
1. Uploads directory doesn't exist
2. File permissions issue
3. Incorrect file path

**Solutions:**
1. Verify uploads directory exists
2. Check file was uploaded successfully
3. Check browser console for errors
4. Verify file path in database

#### Issue 6: Cannot Access Application

**Solutions:**
1. Check if server is running
2. Verify correct URL: http://localhost:3000
3. Try different browser
4. Clear browser cache
5. Check firewall settings

---

## 7. Production Deployment

### Preparation

#### 1. Environment Setup

Create `.env` file:
```env
NODE_ENV=production
PORT=3000
MONGODB_URI=mongodb://your-production-db-url
```

#### 2. Security Enhancements

**Install Additional Packages:**
```bash
npm install helmet compression dotenv
```

**Update server.js:**
```javascript
const helmet = require('helmet');
const compression = require('compression');
require('dotenv').config();

app.use(helmet());
app.use(compression());
```

#### 3. Database Backup

```bash
# Backup MongoDB
mongodump --db webments --out ./backup

# Restore MongoDB
mongorestore --db webments ./backup/webments
```

### Deployment Options

#### Option 1: Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create webments-app

# Add MongoDB addon
heroku addons:create mongolab

# Deploy
git push heroku main

# Open app
heroku open
```

#### Option 2: DigitalOcean

1. Create Droplet (Ubuntu 20.04)
2. SSH into server
3. Install Node.js and MongoDB
4. Clone repository
5. Install dependencies
6. Configure PM2 for process management
7. Set up Nginx as reverse proxy
8. Configure SSL with Let's Encrypt

#### Option 3: AWS EC2

1. Launch EC2 instance
2. Configure security groups
3. Install Node.js and MongoDB
4. Deploy application
5. Set up load balancer
6. Configure auto-scaling

### Production Checklist

- [ ] Environment variables configured
- [ ] Database backed up
- [ ] Security packages installed
- [ ] HTTPS enabled
- [ ] Error logging configured
- [ ] Monitoring set up
- [ ] Performance optimized
- [ ] Load testing completed
- [ ] Backup strategy in place
- [ ] Documentation updated

---

## Additional Resources

### Documentation
- [Node.js Documentation](https://nodejs.org/docs)
- [Express.js Guide](https://expressjs.com/guide)
- [MongoDB Manual](https://docs.mongodb.com/manual)
- [Mongoose Documentation](https://mongoosejs.com/docs)

### Tutorials
- [Node.js Tutorial](https://nodejs.dev/learn)
- [MongoDB University](https://university.mongodb.com)
- [Express.js Tutorial](https://expressjs.com/starter/installing.html)

### Community Support
- [Stack Overflow](https://stackoverflow.com)
- [Node.js Community](https://nodejs.org/community)
- [MongoDB Community](https://community.mongodb.com)

---

## Development Tools

### Recommended Tools

**Code Editor:**
- Visual Studio Code
- Sublime Text
- Atom

**API Testing:**
- Postman
- Insomnia
- Thunder Client (VS Code extension)

**Database Management:**
- MongoDB Compass
- Robo 3T
- Studio 3T

**Version Control:**
- Git
- GitHub Desktop
- GitKraken

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor server logs
- Check error reports
- Verify backups

**Weekly:**
- Update dependencies
- Review performance
- Clean up old files

**Monthly:**
- Security audit
- Database optimization
- Performance testing

### Update Process

```bash
# Check for updates
npm outdated

# Update packages
npm update

# Update specific package
npm update express

# Verify updates
npm list
```

---

## Support

### Getting Help

**Documentation:**
- README.md - Project overview
- PROJECT_DOCUMENTATION.md - Detailed documentation
- TECHNICAL_GUIDE.md - Technical details
- USER_MANUAL.md - User instructions

**Contact:**
- Student: Anuj Singla
- Roll No: 2210991317
- Institution: Chitkara University

**Resources:**
- Project repository
- Issue tracker
- Documentation files

---

## Conclusion

You should now have WebMents running on your local machine. If you encounter any issues not covered in this guide, please refer to the troubleshooting section or contact support.

**Next Steps:**
1. Explore the application
2. Test all features
3. Review documentation
4. Customize as needed
5. Deploy to production

---

**Document Version:** 1.0  
**Last Updated:** April 22, 2026  
**Created by:** Anuj Singla  
**Institution:** Chitkara University

**Happy Coding! 🚀**
