from main import app

from tests import init_test

if __name__ == "__main__":
    with app.app_context():
        init_test()