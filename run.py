import os
from app import create_app

# Read environment (default to development)
env = os.environ.get("FLASK_ENV", "dev")

# Create Flask application
app = create_app(env)

def main():
    # Read server port (default 5000)
    port = int(os.environ.get("PORT", 5000))

    # Start the Flask development server
    app.run(
        host="0.0.0.0",
        port=port,
        debug=app.config.get("DEBUG", False)
    )

if __name__ == "__main__":
    main()