from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
from datetime import datetime
from loguru import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logger
logger.add("api.log", rotation="500 MB", level="INFO")

app = FastAPI(title="BMI Calculator API")

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DATABASE_HOST', 'localhost'),
    'user': os.getenv('DATABASE_USER', 'root'),
    'password': os.getenv('DATABASE_PASSWORD', ''),
    'database': os.getenv('DATABASE_NAME', 'bmi_database'),
    'port': int(os.getenv('DATABASE_PORT', '3306'))
}

# Database initialization
def init_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create table if it doesn't exist
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
        cursor.close()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise Exception(f"Database initialization failed: {str(e)}")

# Initialize database on startup
init_db()

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
async def calculate_bmi(input_data: BMIInput):
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

        # Save to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

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

        cursor.close()
        conn.close()

        logger.info(f"BMI record saved to database for user: {input_data.name}")
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
async def get_bmi_history():
    logger.info("Retrieving BMI history")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM bmi_history ORDER BY timestamp DESC')
        records = cursor.fetchall()

        cursor.close()
        conn.close()

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

@app.delete("/bmi/history")
async def delete_bmi_history():
    logger.info("Deleting all BMI history")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM bmi_history')
        conn.commit()

        cursor.close()
        conn.close()

        logger.info("Successfully deleted all BMI history")
        return {"message": "All BMI history has been deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting BMI history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)