import reflex as rx
import bcrypt
import jwt
from datetime import datetime, timedelta
from app.models import User
import os
import logging
from sqlmodel import select

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-dev-key-change-me")
ALGORITHM = "HS256"


class AuthState(rx.State):
    token: str = rx.Cookie("auth_token")
    user_full_name: str = ""
    user_email: str = ""
    user_id: int = -1
    is_admin: bool = False
    is_authenticated: bool = False
    error_message: str = ""
    loading: bool = False

    @rx.event
    def on_load(self):
        """Check if user is authenticated on page load."""
        if self.token:
            try:
                payload = jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
                self.user_email = payload.get("sub")
                self.user_full_name = payload.get("name", "")
                self.user_id = payload.get("user_id", -1)
                self.is_admin = payload.get("is_admin", False)
                self.is_authenticated = True
            except jwt.ExpiredSignatureError as e:
                logging.exception(f"Error: {e}")
                self.logout()
            except jwt.InvalidTokenError as e:
                logging.exception(f"Error: {e}")
                self.logout()

    @rx.event
    def register(self, form_data: dict):
        """Handle user registration."""
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        full_name = form_data.get("full_name")
        cnpj = form_data.get("cnpj", "")
        if not email or not password or (not full_name):
            self.error_message = "Please fill in all required fields."
            return
        if password != confirm_password:
            self.error_message = "Passwords do not match."
            return
        self.loading = True
        with rx.session() as session:
            existing_user = session.exec(
                select(User).where(User.email == email)
            ).first()
            if existing_user:
                self.error_message = "Email already registered."
                self.loading = False
                return
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
                "utf-8"
            )
            new_user = User(
                email=email,
                password_hash=hashed,
                full_name=full_name,
                cnpj=cnpj,
                created_at=datetime.now(),
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        self.loading = False
        self.error_message = ""
        return AuthState.login({"email": email, "password": password})

    @rx.event
    def login(self, form_data: dict):
        """Handle user login."""
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            self.error_message = "Please enter email and password."
            return
        self.loading = True
        with rx.session() as session:
            user = session.exec(select(User).where(User.email == email)).first()
            if not user:
                self.error_message = "Invalid credentials."
                self.loading = False
                return
            if not bcrypt.checkpw(
                password.encode("utf-8"), user.password_hash.encode("utf-8")
            ):
                self.error_message = "Invalid credentials."
                self.loading = False
                return
            expiration = datetime.utcnow() + timedelta(days=7)
            payload = {
                "sub": user.email,
                "name": user.full_name,
                "user_id": user.id,
                "is_admin": user.is_admin,
                "exp": expiration,
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            self.token = token
            self.user_email = user.email
            self.user_full_name = user.full_name
            self.user_id = user.id
            self.is_admin = user.is_admin
            self.is_authenticated = True
            self.error_message = ""
        self.loading = False
        return rx.redirect("/dashboard")

    @rx.event
    def logout(self):
        """Handle user logout."""
        self.token = ""
        self.user_email = ""
        self.user_full_name = ""
        self.user_id = -1
        self.is_admin = False
        self.is_authenticated = False
        return rx.redirect("/")

    @rx.event
    def check_auth(self):
        """Event to check auth and redirect if needed (for protected pages)."""
        if (
            not self.token
            or not isinstance(self.token, str)
            or len(self.token.strip().split(".")) != 3
        ):
            return rx.redirect("/login")
        try:
            jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
        except Exception as e:
            logging.exception(f"Auth check failed: {e}")
            return rx.redirect("/login")