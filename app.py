from flask import Flask, redirect, url_for
from models import db, Admin, Department
from auth import login_manager
from routes import app as routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(routes)

@app.route('/')
def home():
    return redirect(url_for('app.home'))

def create_initial_data():
    with app.app_context():
        if not Admin.query.first():
            admin = Admin(username='admin', password='admin')
            db.session.add(admin)
        
        if not Department.query.first():
            departments = ['Physiology', 'Dental', 'Physiotherapy']
            for dept in departments:
                department = Department(name=dept)
                db.session.add(department)
        
        db.session.commit()
        print('Initial admin user created: username=admin, password=admin')
        print('Initial departments created')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_initial_data()
    app.run(debug=True)
