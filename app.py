import os
import yaml
import time
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from faker import Faker

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
fake = Faker()

def load_openapi_spec(spec_file):
    """Load OpenAPI spec from a YAML file."""
    with open(spec_file, "r") as file:
        return yaml.safe_load(file)

def generate_mock_data(schema):
    """Generate mock data based on JSON schema."""
    if not schema:
        return None

    if schema.get("type") == "string":
        return fake.word()
    elif schema.get("type") == "integer":
        return fake.random_int()
    elif schema.get("type") == "boolean":
        return fake.boolean()
    elif schema.get("type") == "array":
        return [generate_mock_data(schema["items"])]
    elif schema.get("type") == "object":
        return {key: generate_mock_data(value) for key, value in schema.get("properties", {}).items()}
    return None

def create_routes(api_spec, config):
    """Create Flask routes dynamically."""
    for path, methods in api_spec["paths"].items():
        for method, details in methods.items():
            route = f"/mock{path}"  # Prefix to avoid conflicts
            app.route(route, methods=[method.upper()])(mock_handler(details, config))

def mock_handler(details, config):
    """Handle mock requests."""
    def handler():
        responses = details.get("responses", {})
        response_code = "200"
        
        # Check for custom responses in the config
        custom_response = config.get(request.path, {})
        if custom_response:
            response_code = str(custom_response.get("status_code", 200))
            response_data = custom_response.get("response", {})
            delay = custom_response.get("delay", 0)
            time.sleep(delay)  # Simulate delay
            return jsonify(response_data), int(response_code)
        
        # Default behavior (mock response generation)
        if response_code in responses:
            response_schema = responses[response_code].get("content", {}).get("application/json", {}).get("schema", {})
            mock_data = generate_mock_data(response_schema)
            return jsonify(mock_data), int(response_code)
        
        return jsonify({"error": "Mock response not defined"}), 501
    return handler

def start_mock_server(spec_file, config_file):
    """Start the mock server."""
    config = load_custom_config(config_file)
    api_spec = load_openapi_spec(spec_file)
    create_routes(api_spec, config)
    app.run(debug=True)

def load_custom_config(config_file):
    """Load custom response configuration."""
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return yaml.safe_load(file)
    return {}

if __name__ == "__main__":
    spec_file = input("Enter OpenAPI spec file (e.g., openapi.yaml): ").strip()
    config_file = input("Enter custom response config file (optional): ").strip()

    if not os.path.exists(spec_file):
        print(f"Error: Spec file '{spec_file}' does not exist.")
    else:
        start_mock_server(spec_file, config_file)
