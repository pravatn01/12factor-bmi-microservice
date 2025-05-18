# Installation Guide

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
- Git (optional)

## 🚀 Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/bmi-calculator-microservice.git
   cd bmi-calculator-microservice
   ```

2. **Set up Python virtual environment**

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**

   - Install MySQL if not already installed
   - Create a new database:
     ```sql
     CREATE DATABASE bmi_database;
     ```
   - Create `.env` file in the backend directory:
     ```env
     DATABASE_HOST=localhost
     DATABASE_USER=your_username
     DATABASE_PASSWORD=your_password
     DATABASE_NAME=bmi_database
     DATABASE_PORT=3306
     ```

## ✅ Verify Installation

After completing the installation steps, you can verify that everything is set up correctly by:

1. Checking Python version:

   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. Verifying virtual environment:

   ```bash
   # You should see (venv) at the start of your command prompt
   ```

3. Checking installed packages:

   ```bash
   pip list  # Should show all required packages
   ```

4. Testing database connection:
   ```bash
   mysql -u your_username -p -h localhost
   # Enter your password when prompted
   # Then try:
   USE bmi_database;
   ```

## 🔍 Troubleshooting

If you encounter any issues during installation:

1. **Virtual Environment Issues**

   - Make sure you're in the correct directory
   - Try removing and recreating the virtual environment
   - Check Python path settings

2. **Database Connection Issues**

   - Verify MySQL service is running
   - Check credentials in `.env` file
   - Ensure database port is not blocked by firewall

3. **Package Installation Issues**
   - Try upgrading pip: `pip install --upgrade pip`
   - Check for any error messages in the console
   - Verify internet connection

## Next Steps

After successful installation:

1. See [Configuration](configuration.md) for customizing the application
2. Follow [Running the Application](running.md) to start the services
3. Check [API Reference](../api/endpoints.md) for available endpoints
