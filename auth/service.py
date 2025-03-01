from database.models import User
from .schemas import UserCreateSchema
from .utils import generate_password_hash
from sqlalchemy.orm import Session

class UserService:
    def get_user_by_email(self, email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        return user
    
    def user_exists(self, email: str, db: Session):
        user = self.get_user_by_email(email, db)
        return True if user else False
    
    def create_user(self, user_data: UserCreateSchema, db: Session):
        new_user = User(
            username = user_data.username,
            first_name = user_data.first_name,
            last_name = user_data.last_name,
            email = user_data.email
        )
        new_user.password_hash = generate_password_hash(user_data.password)
        db.add(new_user)
        db.commit()
        return new_user