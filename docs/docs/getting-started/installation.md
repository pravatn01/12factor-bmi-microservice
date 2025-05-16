# Installation Guide

This guide will walk you through the process of setting up the BMI Calculator Microservice on your local machine.

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

## Step 1: Setting Up the Environment

1. Clone the repository (if using Git):

```bash
git clone <repository-url>
cd _12factor_bmi_microservice
```

2. Create a virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Step 2: Database Setup

1. Install MySQL if not already installed
2. Create a new database:

```sql
CREATE DATABASE bmi_database;
```

3. Create a `.env` file in the backend directory:

```bash
DATABASE_HOST=localhost
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_NAME=bmi_database
DATABASE_PORT=3306
```

## Step 3: Verify Installation

1. Check Python installation:

```bash
python --version  # Should be 3.8 or higher
```

2. Verify package installation:

```bash
pip list  # Should show fastapi, streamlit, and other dependencies
```

3. Test database connection:

```bash
python -c "import mysql.connector; mysql.connector.connect(host='localhost', user='your_username', password='your_password', database='bmi_database')"
```

## Common Installation Issues

### Database Connection Issues

- Ensure MySQL service is running
- Verify credentials in `.env` file
- Check if database exists and is accessible

### Package Installation Issues

- Try upgrading pip: `pip install --upgrade pip`
- If installation fails, install packages one by one
- Check Python version compatibility

### Port Conflicts

- Default ports used:
  - Backend: 8000
  - Frontend: 8501
  - MySQL: 3306
- Ensure these ports are available or configure different ports

## Next Steps

After successful installation:

1. See [Configuration](configuration.md) for customizing the application
2. Follow [Running the Application](running.md) to start the services
3. Check [API Reference](../api/endpoints.md) for available endpoints
