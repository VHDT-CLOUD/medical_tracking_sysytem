const express = require('express');
const mysql = require('mysql2/promise');
const session = require('express-session');
const path = require('path');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Security middleware with specific configurations
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Body parser with size limits
app.use(bodyParser.json({ limit: '10kb' }));
app.use(bodyParser.urlencoded({ extended: true, limit: '10kb' }));

// Static files with cache control
app.use(express.static('public', {
  maxAge: '1d',
  setHeaders: (res, path) => {
    if (path.endsWith('.html')) {
      res.setHeader('Cache-Control', 'no-cache');
    }
  }
}));

// Session configuration with enhanced security
app.use(session({
  secret: process.env.SESSION_SECRET || 'your-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: { 
    maxAge: 3600000,
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    sameSite: 'strict',
    domain: process.env.COOKIE_DOMAIN || 'localhost'
  }
}));

// MySQL Connection Pool with enhanced configuration
const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'medical_tracking',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  enableKeepAlive: true,
  keepAliveInitialDelay: 0
});

// Initialize database
async function initializeDatabase() {
  try {
    const connection = await pool.getConnection();
    
    // Create users table with hashed password
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    // Create patients table
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        aadhaar VARCHAR(255) NOT NULL UNIQUE,
        history TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    // Check if we need to insert sample data
    const [userCount] = await connection.execute('SELECT COUNT(*) as count FROM users');
    if (userCount[0].count === 0) {
      const hashedPassword = await bcrypt.hash('hospitalpass789', 10);
      await connection.execute(
        'INSERT INTO users (email, password, role) VALUES (?, ?, ?)',
        ['hospital@example.com', hashedPassword, 'hospital']
      );
    }
    
    const [patientCount] = await connection.execute('SELECT COUNT(*) as count FROM patients');
    if (patientCount[0].count === 0) {
      await connection.execute(
        'INSERT INTO patients (name, aadhaar, history) VALUES (?, ?, ?)',
        ['Alex Carter', '1234-5678-9012', 'Broken arm - April 2025']
      );
    }
    
    connection.release();
    console.log('Database initialized successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
    process.exit(1);
  }
}

// Initialize database on startup
initializeDatabase();

// Middleware to check if user is logged in
const isLoggedIn = (req, res, next) => {
  if (req.session.userId && req.session.role === 'hospital') {
    next();
  } else {
    res.status(401).json({ error: 'Unauthorized. Please log in.' });
  }
};

// Input validation middleware
const validateLogin = (req, res, next) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }
  if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
    return res.status(400).json({ error: 'Invalid email format' });
  }
  next();
};

// Routes
app.post('/login', validateLogin, async (req, res) => {
  try {
    const { email, password } = req.body;
    const connection = await pool.getConnection();
    
    const [users] = await connection.execute(
      'SELECT * FROM users WHERE email = ?',
      [email]
    );
    
    connection.release();
    
    if (users.length === 0) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }
    
    const user = users[0];
    const isValidPassword = await bcrypt.compare(password, user.password);
    
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }
    
    req.session.userId = user.id;
    req.session.email = user.email;
    req.session.role = user.role;
    
    res.json({ 
      success: true, 
      message: 'Login successful', 
      user: { id: user.id, email: user.email, role: user.role } 
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/logout', (req, res) => {
  req.session.destroy();
  res.json({ success: true, message: 'Logged out successfully' });
});

// Get all patients (protected route)
app.get('/patients', isLoggedIn, (req, res) => {
  const query = 'SELECT id, name, aadhaar FROM patients';
  
  pool.getConnection().then(connection => {
    connection.execute(query, (err, results) => {
      connection.release();
      if (err) {
        console.error('Error fetching patients:', err);
        return res.status(500).json({ error: 'Database error while fetching patients' });
      }
      
      res.json(results);
    });
  }).catch(err => {
    console.error('Error getting connection:', err);
    res.status(500).json({ error: 'Database error while fetching patients' });
  });
});

// Get specific patient by ID (protected route)
app.get('/patient/:id', isLoggedIn, (req, res) => {
  const patientId = req.params.id;
  const query = 'SELECT * FROM patients WHERE id = ?';
  
  pool.getConnection().then(connection => {
    connection.execute(query, [patientId], (err, results) => {
      connection.release();
      if (err) {
        console.error('Error fetching patient:', err);
        return res.status(500).json({ error: 'Database error while fetching patient' });
      }
      
      if (results.length === 0) {
        return res.status(404).json({ error: 'Patient not found' });
      }
      
      res.json(results[0]);
    });
  }).catch(err => {
    console.error('Error getting connection:', err);
    res.status(500).json({ error: 'Database error while fetching patient' });
  });
});

// Serve static files
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'hospital-login.html'));
});

app.get('/patient-list', isLoggedIn, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'hospital-patient-list.html'));
});

app.get('/patient-dashboard', isLoggedIn, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'patient-dashboard.html'));
});

// Enhanced error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  
  // Don't expose internal errors in production
  const errorMessage = process.env.NODE_ENV === 'production' 
    ? 'Something went wrong!' 
    : err.message;
    
  res.status(500).json({ 
    error: errorMessage,
    timestamp: new Date().toISOString(),
    path: req.path
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  pool.end(() => {
    console.log('Database pool closed');
    process.exit(0);
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});