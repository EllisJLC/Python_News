from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
import bcrypt

salt = bcrypt.gensalt() # Create bcrypt encrypting function

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)
  # primary_key -> adds index
  # String(50) -> string of max length 50
  # nullable = False -> disallow null
  # Column() -> creates a new column in SQL

  def verify_password(self, password):
    return bcrypt.checkpw(
      password.encode('utf-8'),
      self.password.encode('utf-8')
    )

  @validates('email')
  def validate_email(self, key, email):
    assert '@' in email # Validates @ in email
    return email
  
  @validates('password')
  def validate_password(self, key, password):
    assert len(password) > 4 # Ensures length of password string is greater than 4
    return bcrypt.hashpw(password.encode('utf-8'), salt)

  

  