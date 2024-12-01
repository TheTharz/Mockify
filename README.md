# API Mock Server

A dynamic API mock server built with Python. Automatically generates mock endpoints from an OpenAPI/Swagger specification, enabling quick API testing and frontend development without a live backend.

## Features

- **Dynamic Endpoint Creation**: Reads OpenAPI specs and generates endpoints on the fly.
- **Custom Responses**: Configure error simulation and mock responses via `config.yaml`.
- **Realistic Mock Data**: Uses `Faker` to populate realistic data for responses.
- **Response Delay Simulation**: Mimic real-world API latency.
- **Interactive Swagger UI**: Test endpoints easily using Swagger UI.
- **CORS Support**: Frontend applications can access the mock server.

## Requirements

- Python 3.7+
- Dependencies:
  ```bash
  pip install flask pyswagger faker pyyaml flask-cors
  ```
