# Braille Autocorrect and Suggestion System

A Django web application that provides real-time autocorrect and suggestions for Braille input using QWERTY keyboard format.

## Features

- **Real-time Suggestions**: Get instant suggestions as you type
- **QWERTY Braille Input**: Use D, W, Q, K, O, P keys for Braille dots 1-6
- **Smart Autocorrect**: Uses Levenshtein distance algorithm for accurate suggestions
- **Learning System**: Improves suggestions based on user interactions
- **Responsive Design**: Works on desktop and mobile devices
- **Performance Optimized**: Fast response times for large dictionaries

## Key Mapping

- **D** → Braille Dot 1
- **W** → Braille Dot 2  
- **Q** → Braille Dot 3
- **K** → Braille Dot 4
- **O** → Braille Dot 5
- **P** → Braille Dot 6

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## Technology Stack

- **Backend**: Django 4.2, Python
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Algorithm**: Levenshtein Distance for autocorrect
- **Database**: SQLite (default), PostgreSQL ready

## API Endpoints

- `/` - Main interface
- `/suggestions/` - Get autocorrect suggestions
- `/convert/` - Convert Braille to text

## Deployment Ready

Configured for easy deployment with:
- Gunicorn WSGI server
- WhiteNoise for static files
- Environment variable support
- Database flexibility

## Developer

Created for Thinkerbell Labs Private Limited
