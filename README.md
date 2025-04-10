# Medical Tracking System

A comprehensive medical tracking system built with React, Django, and Material-UI.

## Features

- Patient management
- Medical history tracking
- User authentication
- Responsive design
- Real-time updates

## Tech Stack

- Frontend: React, Material-UI, Redux Toolkit
- Backend: Django, Django REST Framework
- Database: PostgreSQL
- Deployment: Netlify (Frontend), Railway/Heroku (Backend)

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- PostgreSQL

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file with the following variables:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

4. Start the development server:
   ```bash
   npm start
   ```

### Backend Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/medical_tracking
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Deployment

### Frontend (Netlify)

1. Install Netlify CLI:
   ```bash
   npm install -g netlify-cli
   ```

2. Deploy:
   ```bash
   npm run deploy
   ```

### Backend (Railway/Heroku)

1. Install the respective CLI
2. Follow the platform-specific deployment instructions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.