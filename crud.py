from sqlalchemy.orm import session

import models

def get_user(db:session,username:str):
    return db.query(models.User).filter(models.User.username==username).first()