from midaxusers import create_app
from midaxusers.models import db
#from myapp.database import database_manager #sub manager for creating/dropping db
from flask_migrate import Migrate, MigrateCommand

def create_db():
    app = create_app()  

    # create the database and load test data
    with app.app_context():            
        db.create_all()     

if __name__ == "__main__":
    pass