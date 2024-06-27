from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity 

from init import db
from models.comment import Comment, comment_schema, comments_schema
from models.card import Card

# /cards/<int:card_id>/comments 
comments_bp = Blueprint("comments", __name__, url_prefix="/<int:card_id>/comments")

# we already get the comments while fetching cards, so no need for "get comments" route here

# create comment route
@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(card_id):
    # get the comment message from the request body
    body_data = request.get_json()
    # fetch the card with particular id - card_id
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    # if card exists 
    if card:
        # create an instance of the Comment model 
        comment = Comment(
            message=body_data.get("message"),
            date=date.today(),
            card=card,
            user_id=get_jwt_identity()
        )
        # add and commt the session
        db.session.add(comment)
        db.session.commit()
        # return the created commt 
        return comment_schema.dump(comment), 201
    # else 
    else:
        # return an error - card does not exist 
        return {"error": f"Card with id {card-id} not found"}, 404
    
# delete Comment - /cards/card_id?/comments/comment_id
@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(card_id, comment_id):
    # fetch the comment from the db with that id - comment =_id
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    # if comment exists
    if comment:
        # delete the comment 
        db.session.delete(comment)
        db.session.commit()
        # return message 
        return {"message": f"Comment {comment_id} deleted successfully"}
    # else
    else:
        # return an error saying comment does not exist 
        return {"error": f"Comment id {comment_id} not found"}, 404 
    
# Update comment - /cards/card_id/comments/comment_id
@comments_bp.route("/<int:comment_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_comment(card_id, comment_id):
    # get the values from the body of the request
    body_data = request.get_json()
    # find the comment from the db with the id - comment_id
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    # if comment exists
    if comment:
        # update the fields
        comment.message = body_data.get("message") or comment.message
        # commit
        db.session.commit()
        # return some response to the client
        return comment_schema.dump(comment)
    # else
    else:
        # return error saying comment does not exist
        return {"error": f"Comment with id {comment_id} not found"}, 404



