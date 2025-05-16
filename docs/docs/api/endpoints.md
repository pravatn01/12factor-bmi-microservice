# API Endpoints

The BMI Calculator Microservice provides a RESTful API for BMI calculations and history management. All endpoints are available at `http://localhost:8000`.

## Calculate BMI

Calculate BMI for a person and store the result.

```http
POST /calculate-bmi
```

### Request Body

```json
{
  "name": "string",
  "weight": "float", // in kilograms
  "height": "float" // in meters
}
```

### Response

```json
{
  "name": "string",
  "bmi": "float",
  "category": "string",
  "timestamp": "string"
}
```

### BMI Categories

- Underweight: < 18.5
- Normal weight: 18.5 - 24.9
- Overweight: 25 - 29.9
- Obese: ≥ 30

### Example

```bash
curl -X POST http://localhost:8000/calculate-bmi \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "weight": 70, "height": 1.75}'
```

## Get BMI History

Retrieve all BMI calculation records.

```http
GET /bmi/history
```

### Response

```json
[
  {
    "id": "integer",
    "name": "string",
    "height": "float",
    "weight": "float",
    "bmi": "float",
    "category": "string",
    "timestamp": "string"
  }
]
```

### Example

```bash
curl http://localhost:8000/bmi/history
```

## Clear BMI History

Delete all BMI calculation records.

```http
DELETE /bmi/history
```

### Response

```json
{
  "message": "BMI history deleted"
}
```

### Example

```bash
curl -X DELETE http://localhost:8000/bmi/history
```

## Error Responses

The API uses standard HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid input)
- `500`: Internal Server Error

Error response format:

```json
{
  "detail": "Error message"
}
```

## Rate Limiting

Currently, there are no rate limits implemented on the API endpoints.

## Authentication

The API currently does not require authentication. For production deployment, consider adding appropriate authentication mechanisms.
