import os
from app import create_app

# env = os.environ.get("APP_ENV" or 'default')

# app = create_app("config.%sConfig" % env.capitalize())
app = create_app(os.getenv('APP_ENV') or 'testing')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)