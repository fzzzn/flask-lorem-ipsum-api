# Lorem Ipsum Generator API

A simple Flask API for generating Lorem Ipsum placeholder text.

## Features

- Generate Lorem Ipsum text with customizable parameters.
- Supports multiple response formats: JSON, plain text, and HTML.
- CORS enabled for all routes.
- Dockerized for easy deployment.

## Endpoints

### Home

- **URL**: `/`
- **Method**: `GET`
- **Description**: Renders a simple HTML homepage with API documentation.

### Generate Lorem Ipsum

- **URL**: `/api/lorem-ipsum`
- **Method**: `GET`
- **Description**: Generates Lorem Ipsum text based on query parameters.

#### Query Parameters

- `paragraphs` (optional, default=1): Number of paragraphs to generate.
- `words` (optional, default=0): Number of words to generate (overrides paragraphs parameter).
- `format` (optional, default="json"): Response format ("json", "text", or "html").

#### Examples

- `/api/lorem-ipsum?paragraphs=3`
- `/api/lorem-ipsum?words=50`
- `/api/lorem-ipsum?paragraphs=2&format=html`

## Running Locally

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/fzzzn/flask-lorem-ipsum-api.git
   cd flask-lorem-ipsum-api
   ```
2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:

   ```sh
   python app.py
   ```
4. Access the application at [http://localhost:5000](http://localhost:5000)

## Docker Deployment

### Build the Docker image:

```sh
docker build -t flask-lorem-ipsum-api .
```

### Run the Docker container:

```sh
docker run -p 5000:5000 flask-lorem-ipsum-api
```

4. Access the application at [http://localhost:5000](http://localhost:5000)

## Logging

Logs are configured to be compatible with Docker, directing logs to stdout/stderr.

## Error Handling

- 404 errors return a JSON response with an error message.
- 500 errors return a JSON response with an error message and details.

## License

This project is licensed under the MIT License.
