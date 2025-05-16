from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
import mysql.connector
from mysql.connector import pooling
from datetime import datetime
from loguru import logger
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Loading environment variables
load_dotenv()

# Setting up logging
logger.add("api.log", rotation="500 MB", level="INFO")

# Database config
DB_CONFIG = {
    'host': os.getenv('DATABASE_HOST', 'localhost'),
    'user': os.getenv('DATABASE_USER', 'root'),
    'password': os.getenv('DATABASE_PASSWORD', ''),
    'database': os.getenv('DATABASE_NAME', 'bmi_database'),
    'port': int(os.getenv('DATABASE_PORT', '3306'))
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Starting up: creating db pool
    logger.info("Creating database connection pool")
    app.state.db = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        **DB_CONFIG
    )

    # Initializing database schema
    with app.state.db.get_connection() as conn:
        with conn.cursor() as cursor:
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
            logger.info("Database initialized")

    yield

    # Shutting down: closing connections
    logger.info("Closing database connections")
    try:
        app.state.db._remove_connections()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing db connections: {str(e)}")

app = FastAPI(title="BMI Calculator API", lifespan=lifespan)

class BMIInput(BaseModel):
    name: str
    weight: float  # kg
    height: float  # meters

class BMIResponse(BaseModel):
    name: str
    bmi: float
    category: str
    timestamp: str

class BMIHistoryItem(BMIResponse):
    id: int
    weight: float
    height: float

def get_bmi_category(bmi: float) -> str:
    """Getting BMI category based on value"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    return "Obese"

@app.post("/calculate-bmi", response_model=BMIResponse)
async def calculate_bmi(input_data: BMIInput, request: Request):
    logger.info(f"Calculating BMI for: {input_data.name}")

    if input_data.weight <= 0 or input_data.height <= 0:
        logger.error(f"Invalid input - weight: {input_data.weight}, height: {input_data.height}")
        raise HTTPException(status_code=400, detail="Weight and height must be positive")

    try:
        bmi = input_data.weight / (input_data.height ** 2)
        category = get_bmi_category(bmi)

        logger.info(f"BMI result - User: {input_data.name}, BMI: {round(bmi, 2)}, Category: {category}")

        with request.app.state.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO bmi_history (name, height, weight, bmi, category) VALUES (%s, %s, %s, %s, %s)',
                    (input_data.name, input_data.height, input_data.weight, round(bmi, 2), category)
                )
                conn.commit()

                cursor.execute('SELECT timestamp FROM bmi_history WHERE id = LAST_INSERT_ID()')
                timestamp = cursor.fetchone()[0]

        return BMIResponse(
            name=input_data.name,
            bmi=round(bmi, 2),
            category=category,
            timestamp=str(timestamp)
        )

    except Exception as e:
        logger.error(f"Error calculating BMI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bmi/history", response_model=List[BMIHistoryItem])
async def get_bmi_history(request: Request):
    logger.info("Getting BMI history")

    try:
        with request.app.state.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM bmi_history ORDER BY timestamp DESC')
                records = cursor.fetchall()

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
        logger.error(f"Error getting BMI history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/bmi/history")
async def delete_bmi_history(request: Request):
    logger.info("Deleting BMI history")

    try:
        with request.app.state.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM bmi_history')
                conn.commit()
        return {"message": "BMI history deleted"}
    except Exception as e:
        logger.error(f"Error deleting BMI history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)