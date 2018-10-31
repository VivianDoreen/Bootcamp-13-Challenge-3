from app.views import users
from app.views import products
from app import app
if __name__ == '__main__':
    app.run(debug=True, port=8080)