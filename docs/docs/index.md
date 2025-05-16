# BMI Calculator Microservice

Welcome to the BMI Calculator Microservice documentation. This project is a modern, scalable microservice that provides BMI (Body Mass Index) calculation and tracking capabilities.

## Features

- **BMI Calculation**: Accurate BMI calculation based on height and weight
- **History Tracking**: Store and retrieve BMI calculation history
- **Modern UI**: Clean and responsive web interface
- **RESTful API**: Well-documented API endpoints
- **Database Integration**: Persistent storage using MySQL
- **12-Factor Compliance**: Following modern cloud-native application principles

## Quick Start

```bash
# Clone the repository
git clone <repository-url>

# Install dependencies
pip install -r requirements.txt

# Start the backend service
cd backend
uvicorn main:app --reload

# Start the frontend service (in a new terminal)
cd frontend
streamlit run app.py
```

## Project Structure

```
_12factor_bmi_microservice/
├── backend/
│   ├── main.py          # FastAPI application
│   └── requirements.txt  # Backend dependencies
├── frontend/
│   └── app.py           # Streamlit web interface
├── tests/
│   └── test_bmi_api.py  # API tests
└── docs/                # Documentation
```

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **Database**: MySQL
- **Documentation**: MkDocs with Material theme
- **Testing**: pytest

## Contributing

We welcome contributions! Please see our [Contributing Guide](development/contributing.md) for details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
