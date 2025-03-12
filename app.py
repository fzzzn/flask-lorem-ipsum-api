from flask import Flask, jsonify, request, render_template_string
import lorem
import logging
import sys
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging for Docker compatibility
# Direct logs to stdout/stderr which Docker captures
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
# Remove default Flask logger handlers to avoid duplication
app.logger.handlers = []
app.logger.propagate = True

# Simple HTML template for the home page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Lorem Ipsum Generator API</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
        code { background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        pre { background-color: #f8f8f8; padding: 10px; border-radius: 5px; overflow-x: auto; }
        h1 { color: #333; }
        h2 { color: #555; margin-top: 25px; }
        .endpoint { background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
</head>
<body>
    <h1>Lorem Ipsum Generator API</h1>
    <p>A simple API for generating Lorem Ipsum placeholder text.</p>
    
    <div class="endpoint">
        <h2>Generate Lorem Ipsum</h2>
        <p><code>GET /api/lorem-ipsum</code></p>
        <h3>Query Parameters:</h3>
        <ul>
            <li><code>paragraphs</code> (optional, default=1): Number of paragraphs to generate</li>
            <li><code>words</code> (optional, default=0): Number of words to generate (overrides paragraphs parameter)</li>
            <li><code>format</code> (optional, default="json"): Response format ("json", "text", or "html")</li>
        </ul>
        
        <h3>Examples:</h3>
        <p><a href="/api/lorem-ipsum?paragraphs=3">/api/lorem-ipsum?paragraphs=3</a></p>
        <p><a href="/api/lorem-ipsum?words=50">/api/lorem-ipsum?words=50</a></p>
        <p><a href="/api/lorem-ipsum?paragraphs=2&format=html">/api/lorem-ipsum?paragraphs=2&format=html</a></p>
    </div>
</body>
</html>
'''


@app.route('/')
def home():
    """Render a simple HTML homepage with API documentation."""
    logger.info("Homepage accessed")
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/lorem-ipsum')
def generate_lorem_ipsum():
    """
    Generate Lorem Ipsum text based on query parameters.
    Supports multiple formats and customization options.
    """
    try:
        # Get and validate parameters
        paragraphs = max(1, min(10, request.args.get(
            'paragraphs', default=1, type=int)))
        words = max(0, min(1000, request.args.get(
            'words', default=0, type=int)))
        format_type = request.args.get(
            'format', default='json', type=str).lower()

        logger.info(f"Generating lorem ipsum with params: paragraphs={paragraphs}, words={words}, format={format_type}")

        # Generate the text
        if words > 0:
            text = lorem.text()
            words_list = text.split()
            # Ensure we have enough words by generating more text if needed
            while len(words_list) < words:
                text += " " + lorem.text()
                words_list = text.split()

            # Get the requested number of words and join them
            text = ' '.join(words_list[:words])
        else:
            text = '\n\n'.join([lorem.paragraph() for _ in range(paragraphs)])

        # Format the response based on the format parameter
        if format_type == 'text':
            return text, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        elif format_type == 'html':
            paragraphs_html = ''.join(
                [f'<p>{p}</p>' for p in text.split('\n\n')])
            return paragraphs_html, 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:  # default to JSON
            return jsonify({
                "lorem_ipsum": text,
                "meta": {
                    "paragraphs": paragraphs if words == 0 else None,
                    "words": words if words > 0 else len(text.split()),
                    "characters": len(text)
                }
            })

    except Exception as e:
        logger.error(f"Error generating Lorem Ipsum: {str(e)}")
        return jsonify({"error": "Failed to generate Lorem Ipsum text", "details": str(e)}), 500


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.path}")
    return jsonify({"error": "Endpoint not found", "message": "Please check the documentation at the root URL"}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    logger.error(f"500 error: {str(e)}")
    return jsonify({"error": "Server error", "message": "An internal server error occurred"}), 500


if __name__ == '__main__':
    logger.info("Starting Lorem Ipsum Generator API")
    # Bind to 0.0.0.0 to make the server publicly available when running in Docker
    app.run(host='0.0.0.0', port=5000, debug=False)