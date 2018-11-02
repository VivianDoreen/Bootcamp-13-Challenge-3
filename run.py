from app.views import users
from app.views import products
from app.views import sales
from tests import test_base
from app import app
if __name__ == '__main__':
    app.run(debug=True, port=8080)