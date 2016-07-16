import config
from app import app, db

if __name__ == '__main__':
    if config.RESET_DB:
        db.drop_all()
    db.create_all()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
