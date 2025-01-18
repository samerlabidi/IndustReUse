# IndustReUse - Industrial Waste Management Platform

## Overview
IndustReUse is a web-based platform designed to facilitate the exchange of industrial waste materials between companies, promoting circular economy practices. The platform enables businesses to list their waste materials and connect with potential buyers, reducing waste and promoting sustainable resource usage.

## Features
- User Authentication & Authorization
- Material Listing & Management
- Transaction System
- Real-time Notifications
- Analytics Dashboard
- Interactive Map Interface

## Tech Stack
### Backend
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy ORM
- JWT Authentication
- Pydantic for data validation

### Frontend
- React.js
- Material-UI (MUI)
- React Query for state management
- Axios for API calls
- Leaflet for maps

## Project Structure

IndustReUse/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── models/
│ │ ├── schemas/
│ │ ├── services/
│ │ └── main.py
│ └── requirements.txt
└── frontend/
├── src/
│ ├── components/
│ ├── services/
│ ├── App.js
│ └── index.js
└── package.json

\\\
IndustReUse/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── services/
    │   ├── App.js
    │   └── index.js
    └── package.json
\\\

## Setup Instructions

### Backend Setup
1. Create and activate virtual environment:
   \\\ash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \\\

2. Install dependencies:
   \\\ash
   cd backend
   pip install -r requirements.txt
   \\\

3. Set up environment variables:
   - Create a .env file with:
     - DATABASE_URL
     - SECRET_KEY
     - ALGORITHM
     - ACCESS_TOKEN_EXPIRE_MINUTES

4. Run the application:
   \\\ash
   uvicorn app.main:app --reload
   \\\

### Frontend Setup
1. Install dependencies:
   \\\ash
   cd frontend
   npm install
   \\\

2. Start the development server:
   \\\ash
   npm start
   \\\

## API Endpoints

### Authentication
- POST /api/auth/register - Register new user
- POST /api/auth/login - User login
- POST /api/auth/logout - User logout

### Materials
- GET /api/materials - List all materials
- POST /api/materials - Create new material
- GET /api/materials/{id} - Get material details
- PUT /api/materials/{id} - Update material
- DELETE /api/materials/{id} - Delete material

### Transactions
- GET /api/transactions - List all transactions
- POST /api/transactions - Create new transaction
- GET /api/transactions/{id} - Get transaction details
- PATCH /api/transactions/{id}/status - Update transaction status

## Contributors
- Samer Labidi
