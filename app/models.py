# Add any model classes for Flask-SQLAlchemy here

from app import db 
from sqlalchemy.sql import func
from flask_jwt_extended import (get_current_user)
# This could be expanded to fit the needs of your application. For example,
# it could track who revoked a JWT, when a token expires, notes for why a
# JWT was revoked, an endpoint to un-revoked a JWT, etc.
# Making jti an index can significantly speed up the search when there are
# tens of thousands of records. Remember this query will happen for every
# (protected) request,
# If your database supports a UUID type, this can be used for the jti column
# as well

class Tokenlist(db.Model):
    '''Change table name'''
    __tablename__ = 'jwt_tokens'


    id              = db.Column(db.Integer, primary_key=True)
    fresh           = db.Column(db.Boolean, default=True, nullable=False)
    iat             = db.Column(db.Integer)
    jti             = db.Column(db.String(48), nullable=False, index=True)
    type            = db.Column(db.String(16), nullable=False)
    sub             = db.Column(db.String(32), nullable=False)
    nbf             = db.Column(db.Integer)
    csrf            = db.Column(db.String(32), nullable=False)
    user_id         = db.Column(db.String(32), default=lambda: get_current_user().id, nullable=False ) 
    created_at      = db.Column(db.Integer)
    #created_at      = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    exp             = db.Column(db.Integer)
    valid           = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<Token {self.jti}>'
 

     #id fresh iat jti type sub nbf csrf user_id created_at exp valid            

     