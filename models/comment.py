from init import db, ma 
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    date = db.Column(db.Date) # created date

    user_id = db.Column(db.Integer, db.ForeignKey("user_id"), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("card_id"), nullable=False)

    user = db.relationship("User", back_populates="comments")
    card = db.relationship("Card", back_populates="comments")

class CommentSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    card = fields.Nested("CardSchema", exclude=["comments"])

    class Meta:
        fields = ("id", "message", "date", "user", "card")

comment_schema = CommentSchema()
comments_schema = CommentSchema(man=True)
