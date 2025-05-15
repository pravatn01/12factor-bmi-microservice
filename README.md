# BMI Calculator Microservice

A modern microservice application for calculating Body Mass Index (BMI) using FastAPI backend and Streamlit frontend that applies as many 12-Factor principles as possible.

## Project Structure

```
_12factor_bmi_microservice/
├── data/               # Data directory for any data files
├── docs/              # Documentation files
├── models/            # Model-related files
├── notebooks/         # Jupyter notebooks
├── references/        # Reference materials
├── reports/          # Generated analysis reports
├── tests/            # Test files
├── venv/             # Python virtual environment
├── .gitignore        # Git ignore file
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── Makefile          # Automation commands
├── README.md         # Project documentation
├── pyproject.toml    # Python project configuration
├── requirements.txt  # Project dependencies
└── setup.cfg         # Setup configuration
```

## Features

- Fast and accurate BMI calculation
- User-friendly interface
- BMI category classification
- Informative BMI scale visualization
- Input validation and error handling
- Responsive design

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- Make (for using Makefile commands)

## Installation

1. Create and activate a virtual environment (if not already done):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Install pre-commit hooks (optional):

```bash
pre-commit install
```

## Development

The project uses a Makefile for common development tasks. Here are some available commands:

```bash
make help           # Show available commands
make install       # Install project dependencies
make test          # Run tests
make lint          # Run linting checks
make clean         # Clean up generated files
```

## Running the Application

1. Start the FastAPI backend server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

2. In a new terminal, start the Streamlit frontend:

```bash
streamlit run app.py
```

The web interface will automatically open in your default browser at http://localhost:8501

## API Documentation

Once the backend is running, you can access:

- Interactive API documentation at http://localhost:8000/docs
- Alternative API documentation at http://localhost:8000/redoc

## Technical Details

### Backend (FastAPI)

- RESTful API endpoint for BMI calculation
- Input validation using Pydantic models
- Error handling and proper HTTP status codes
- Async request handling

### Frontend (Streamlit)

- Clean and intuitive user interface
- Real-time BMI calculation
- Visual feedback and animations
- Responsive layout
- Informative BMI scale and categories

## BMI Categories

- Underweight: < 18.5
- Normal weight: 18.5 - 24.9
- Overweight: 25 - 29.9
- Obese: ≥ 30

