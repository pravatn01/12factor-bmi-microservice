# Running the Application

After completing the installation steps, you can start the BMI Calculator Microservice. The application consists of two main components that need to be run separately: the backend service and the frontend service.

## 🚀 Starting the Services

### 1. Start the Backend Service

Open a terminal in your project directory and run:

```bash
cd _12factor_bmi_microservice\backend
uvicorn main:app --reload
```

The backend service will be available at: http://localhost:8000

You can verify the backend is running by visiting:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Start the Frontend Service

Open a new terminal window and run:

```bash
cd _12factor_bmi_microservice/frontend
streamlit run app.py
```

The frontend service will be available at: http://localhost:8501

## 🔍 Verifying the Services

### Backend Verification

1. Visit http://localhost:8000/docs
2. Try the `/calculate-bmi` endpoint with sample data
3. Check if the response is successful

### Frontend Verification

1. Visit http://localhost:8501
2. Enter sample weight and height values
3. Verify that the BMI calculation works
4. Check if the history is being displayed

## 📊 Default Ports

The services use the following default ports:

- Backend (FastAPI): 8000
- Frontend (Streamlit): 8501
- Database (MySQL): 3306

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**

   - Check if another process is using the required ports
   - Kill the process or use different ports

   ```bash
   # For backend, use a different port:
   uvicorn main:app --reload --port 8080

   # For frontend, use a different port:
   streamlit run app.py --server.port 8502
   ```

2. **Backend Connection Issues**

   - Verify the backend service is running
   - Check the console for error messages
   - Ensure the database is accessible

3. **Frontend Connection Issues**
   - Verify the backend URL is correctly configured
   - Check browser console for errors
   - Clear browser cache if needed

## 🛑 Stopping the Services

To stop the services:

1. For the frontend and backend services:

   - Press `Ctrl+C` in their respective terminal windows

2. To stop the MySQL service (if needed):

   ```bash
   # Windows
   net stop mysql80

   # Linux/MacOS
   sudo service mysql stop
   ```
