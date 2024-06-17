from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import bcrypt, db
from models.user import User, user_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # get the data from the body of the request
        body_data = request.get_json()
        # create an instance if the User model 
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email")
        )
        
        # extract the password from the body
        password = body_data.get("password")

        # hash the password
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # add and commit to the DB 
        db.session.add(user)
        db.session.commit()

        # respomd back to front end
        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        # not null violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        # unique violation 
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address is already in use"}, 409
            
