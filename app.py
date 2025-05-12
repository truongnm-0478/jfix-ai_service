from flask import Flask, jsonify
from apis import init_api
from config import Config
import logging
import os
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    CORS(app, origins="*", supports_credentials=True, allow_headers="*")
    
    # Initialize REST API
    api = init_api(app)
    
    @app.route('/')
    def index():
        """Health check endpoint"""
        return jsonify({
            "status": "ok",
            "message": "Japanese Learning API Server is running"
        })
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            "error": "Not found",
            "message": "The requested URL was not found on the server"
        }), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors"""
        logger.error(f"Server error: {error}")
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 9000))
    app.run(debug=True, host='0.0.0.0', port=9000)