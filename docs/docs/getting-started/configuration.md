# Configuration Guide

## Environment Setup

Create a `.env` file in the root directory with the following configuration:

```env
DATABASE_HOST=localhost
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_NAME=bmi_database
DATABASE_PORT=3306
```

## Database Configuration

1. Install MySQL 8.0 or higher
2. Create a new database:
   ```sql
   CREATE DATABASE bmi_database;
   ```

## Application Settings

### Backend Settings

- Default port: 8000
- Debug mode: Enabled in development
- CORS: Enabled for frontend

### Frontend Settings

- Default port: 8501
- Theme: Light/Dark mode support
- Session state: Enabled

## Security Configuration

- Input validation
- Database connection pooling
- Environment variable isolation
- No sensitive data exposure
