from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
from mysql.connector import pooling
from datetime import datetime
from loguru import logger
import os
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Configure logger
logger.add("api.log", rotation="500 MB", level="INFO")

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DATABASE_HOST', 'localhost'),
    'user': os.getenv('DATABASE_USER', 'root'),
    'password': os.getenv('DATABASE_PASSWORD', ''),
    'database': os.getenv('DATABASE_NAME', 'bmi_database'),
    'port': int(os.getenv('DATABASE_PORT', '3306'))
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database pool and initialize
    logger.info("Creating database connection pool")
    app.state.db = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        **DB_CONFIG
    )

    # Initialize database
    conn = app.state.db.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                height FLOAT NOT NULL,
                weight FLOAT NOT NULL,
                bmi FLOAT NOT NULL,
                category VARCHAR(50) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise e
    finally:
        cursor.close()
        conn.close()

    yield  # Application runs here

    # Shutdown: close all connections in the pool
    logger.info("Closing database connections")
    try:
        app.state.db._remove_connections()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error closing database connections: {str(e)}")

app = FastAPI(title="BMI Calculator API", lifespan=lifespan)

class BMIInput(BaseModel):
    name: str
    weight: float  # weight in kg
    height: float  # height in meters

class BMIResponse(BaseModel):
    name: str
    bmi: float
    category: str
    timestamp: str

class BMIHistoryItem(BMIResponse):
    id: int
    weight: float
    height: float

@app.post("/calculate-bmi", response_model=BMIResponse)
async def calculate_bmi(input_data: BMIInput, request: Request):
    logger.info(f"Calculating BMI for user: {input_data.name}")
    if input_data.weight <= 0 or input_data.height <= 0:
        logger.error(f"Invalid input - weight: {input_data.weight}, height: {input_data.height}")
        raise HTTPException(status_code=400, detail="Weight and height must be positive numbers")

    try:
        # Calculate BMI
        bmi = input_data.weight / (input_data.height ** 2)

        # Determine BMI category
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        logger.info(f"BMI calculation result - User: {input_data.name}, BMI: {round(bmi, 2)}, Category: {category}")

        # Get database connection from app state
        conn = request.app.state.db.get_connection()
        cursor = conn.cursor()

        try:
            query = '''
                INSERT INTO bmi_history (name, height, weight, bmi, category)
                VALUES (%s, %s, %s, %s, %s)
            '''
            values = (input_data.name, input_data.height, input_data.weight, round(bmi, 2), category)

            cursor.execute(query, values)
            conn.commit()

            # Get the timestamp of the inserted record
            cursor.execute('SELECT timestamp FROM bmi_history WHERE id = LAST_INSERT_ID()')
            timestamp = cursor.fetchone()[0]

            logger.info(f"BMI record saved to database for user: {input_data.name}")
            return BMIResponse(
                name=input_data.name,
                bmi=round(bmi, 2),
                category=category,
                timestamp=str(timestamp)
            )
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"Error calculating BMI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bmi/history", response_model=List[BMIHistoryItem])
async def get_bmi_history(request: Request):
    logger.info("Retrieving BMI history")

    conn = request.app.state.db.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM bmi_history ORDER BY timestamp DESC')
        records = cursor.fetchall()

        logger.info(f"Retrieved {len(records)} BMI records")
        return [
            BMIHistoryItem(
                id=record[0],
                name=record[1],
                height=record[2],
                weight=record[3],
                bmi=record[4],
                category=record[5],
                timestamp=str(record[6])
            )
            for record in records
        ]
    except Exception as e:
        logger.error(f"Error retrieving BMI history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/bmi/history")
async def delete_bmi_history(request: Request):
    logger.info("Deleting all BMI history")

    conn = request.app.state.db.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM bmi_history')
        conn.commit()

        logger.info("Successfully deleted all BMI history")
        return {"message": "All BMI history has been deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting BMI history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)