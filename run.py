import config
from app import app, db
from app.models.settings import Settings

if __name__ == '__main__':
    config.reset_system(db)
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
