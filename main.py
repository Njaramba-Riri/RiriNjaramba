import os
from app import create_app

env = os.environ.get("APP_ENV", 'dev')
app = create_app("config.%sConfig" % env.capitalize())


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)