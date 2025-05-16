import pytest
from fastapi.testclient import TestClient
import sys
import os
from unittest.mock import MagicMock
import mysql.connector

# Adding project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _12factor_bmi_microservice.backend.main import app

@pytest.fixture
def mock_db_pool():
    """Setting up mock database pool"""
    pool = MagicMock()
    conn = MagicMock()
    cursor = MagicMock()

    # Mocking timestamp return value
    cursor.fetchone.return_value = ["2023-01-01 00:00:00"]
    conn.cursor.return_value = cursor
    pool.get_connection.return_value = conn

    return pool

@pytest.fixture
def test_client(mock_db_pool):
    """Setting up test client with mocked db"""
    with TestClient(app) as client:
        app.state.db = mock_db_pool
        yield client

def test_calculate_bmi_normal_weight(test_client):
    """Testing BMI calculation for normal weight"""
    test_input = {
        "name": "John Doe",
        "weight": 70.0,  # kg
        "height": 1.75   # meters
    }

    response = test_client.post("/calculate-bmi", json=test_input)

    assert response.status_code == 200
    data = response.json()

    # Checking response data
    assert all(key in data for key in ["name", "bmi", "category", "timestamp"])
    assert data["name"] == "John Doe"
    assert round(data["bmi"], 2) == round(70 / (1.75 ** 2), 2)
    assert data["category"] == "Normal weight"