from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship("Recipe", back_populates = 'user')
    
    serialize_rules = ("-recipes.user", "-_password_hash")
    
    @hybrid_property
    def password_hash(self):
# sourcery skip: raise-specific-error
        raise AttributeError("Password hashes may not be viewed.")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8')
        )
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )
    
    def __repr__(self):
        return f"User {self.username}, ID: {self.id}"


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    __table_args__ = (db.CheckConstraint('length(instructions) > 50'), )
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship("User", back_populates="recipes")
    
    # @validates("instructions")
    # def validate_instruction(self, _, text):
    #     if not isinstance(text, str):
    #         raise TypeError("Instructions must be string")
    #     elif len(text) < 50:
    #         raise ValueError("Instruction must be at least 50 characters")
    #     return text
    def __repr__(self):
        return f'<Recipe {self.id} | {self.title}: {self.instructions}>'