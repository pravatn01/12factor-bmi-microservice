# Running the Application

## Prerequisites

- Python 3.8 or higher installed
- MySQL 8.0 or higher installed
- Virtual environment activated
- Dependencies installed
- Configuration completed

## Starting the Backend

1. Navigate to the backend directory:

   ```bash
   cd _12factor_bmi_microservice/backend
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

The backend will be available at: http://localhost:8000

## Starting the Frontend

1. Open a new terminal
2. Navigate to the frontend directory:

   ```bash
   cd _12factor_bmi_microservice/frontend
   ```

3. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

The frontend will be available at: http://localhost:8501

## Verifying the Setup

1. Check API documentation:

   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

2. Test BMI calculation:
   - Open frontend at http://localhost:8501
   - Enter sample height and weight
   - Check calculation result

## Troubleshooting

### Common Issues

1. Port already in use:

   ```bash
   # For backend
   uvicorn main:app --reload --port 8001

   # For frontend
   streamlit run app.py --server.port 8502
   ```

2. Database connection issues:

   - Verify MySQL is running
   - Check .env configuration
   - Ensure database exists

3. Module not found errors:
   - Activate virtual environment
   - Reinstall dependencies:
     ```bash
     pip install -r requirements.txt
     ```
