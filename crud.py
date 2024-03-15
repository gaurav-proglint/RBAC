from sqlalchemy.orm import session

import models

def get_user(db:session,username:str):
    return db.query(models.User).filter(models.User.username==username).first()

def insert_token(db:session,id:int,token:str):
    user=db.query(models.Token).filter(models.Token.id==id).first()
    if user:
        user.token = token
        db.commit()
    else:    
        new_token = models.Token(id=id, token=token)
        db.add(new_token)
        db.commit()
        db.refresh(new_token)

