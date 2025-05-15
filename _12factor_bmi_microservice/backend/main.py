from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime
from loguru import logger

# Configure logger
logger.add("api.log", rotation="500 MB", level="INFO")

app = FastAPI(title="BMI Calculator API")

# Database initialization
def init_db():
    conn = sqlite3.connect('bmi.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bmi_history
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         height REAL NOT NULL,
         weight REAL NOT NULL,
         bmi REAL NOT NULL,
         category TEXT NOT NULL,
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

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
        conn = sqlite3.connect('bmi.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO bmi_history (name, height, weight, bmi, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (input_data.name, input_data.height, input_data.weight, round(bmi, 2), category))
        conn.commit()

        # Get the timestamp of the inserted record
        c.execute('SELECT timestamp FROM bmi_history WHERE id = last_insert_rowid()')
        timestamp = c.fetchone()[0]
        conn.close()

        logger.info(f"BMI record saved to database for user: {input_data.name}")
        return BMIResponse(
            name=input_data.name,
            bmi=round(bmi, 2),
            category=category,
            timestamp=timestamp
        )
    except Exception as e:
        logger.error(f"Error calculating BMI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bmi/history", response_model=List[BMIHistoryItem])
async def get_bmi_history():
    logger.info("Retrieving BMI history")
    try:
        conn = sqlite3.connect('bmi.db')
        c = conn.cursor()
        c.execute('SELECT * FROM bmi_history ORDER BY timestamp DESC')
        records = c.fetchall()
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
                timestamp=record[6]
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
        conn = sqlite3.connect('bmi.db')
        c = conn.cursor()
        c.execute('DELETE FROM bmi_history')
        conn.commit()
        conn.close()
        logger.info("Successfully deleted all BMI history")
        return {"message": "All BMI history has been deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting BMI history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)