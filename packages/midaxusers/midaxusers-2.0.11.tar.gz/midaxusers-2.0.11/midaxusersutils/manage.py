from midaxusers import create_app
from midaxusers.models import db
#from myapp.database import database_manager #sub manager for creating/dropping db
from flask_migrate import Migrate, MigrateCommand

def create_db():
    app = create_app()  

    # create the database and load test data
    with app.app_context():            
        db.create_all()     

def create_test_user():
    app = create_app()

    with app.app_context():          
        test_user = User()
        test_user.domain = 'midax'
        test_user.email = 'test@midax.com'
        test_user.password = 'm1dax'
        test_user.role = 1     

        db.session.add(test_user)
        db.session.commit()

        #dbuser = UserLogin.get_user({'login_type': 'WEBSITE', 'login_key': 'test@midax.com'})

        loginws = UserLogin()
        loginws.login_type = 'WEBSITE'
        loginws.login_key= 'test@midax.com'
        loginws.password = 'm1dax'
        loginws.user = test_user
        logintm = UserLogin()
        logintm.login_type = 'TERMINAL'
        logintm.login_key= 'HONOLULU^1'
        logintm.password = '123'
        logintm.user = test_user

        db.session.add(loginws)
        db.session.add(logintm)

        newuser_attributes = UserAttributes()

        newuser_attributes.user = test_user
        newuser_attributes.name = 'test'
        newuser_attributes.value = 'attr'
        db.session.add(newuser_attributes)

        db.session.commit()     

if __name__ == "__main__":
    pass