# init_db.py
from app import create_app, db, ElectroScooter
def init_database():
    app = create_app()
    with app.app_context():
        # Create the database tables
        db.create_all()
        
        # Initialize the database with sample data (optional)
        sample_scooter_1 = ElectroScooter(name="Scooter 1", battery_level=1000)
        sample_scooter_2 = ElectroScooter(name="Scooter 2", battery_level=5000)
        db.session.add(sample_scooter_1)
        db.session.add(sample_scooter_2)
        db.session.commit()

if __name__ == "__main__":
    init_database()