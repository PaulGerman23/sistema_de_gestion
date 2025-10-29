from app import create_app, db
from app.models import crear_bd

app = create_app()

with app.app_context():
    crear_bd()

if __name__ == '__main__':
    app.run(debug=True)