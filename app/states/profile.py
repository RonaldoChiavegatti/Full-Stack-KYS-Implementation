import reflex as rx
from sqlmodel import select
import bcrypt
from app.models import User
from app.states.auth import AuthState


class ProfileState(rx.State):
    full_name: str = ""
    email: str = ""
    cnpj: str = ""
    current_password: str = ""
    new_password: str = ""
    confirm_password: str = ""
    is_editing: bool = False

    @rx.event
    async def load_profile(self):
        """Load user profile data."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        self.full_name = auth_state.user_full_name
        self.email = auth_state.user_email
        with rx.session() as session:
            user = session.get(User, auth_state.user_id)
            if user:
                self.cnpj = user.cnpj

    @rx.event
    async def save_profile(self, form_data: dict):
        """Update user profile."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        new_name = form_data.get("full_name")
        new_cnpj = form_data.get("cnpj")
        with rx.session() as session:
            user = session.get(User, auth_state.user_id)
            if user:
                user.full_name = new_name
                user.cnpj = new_cnpj
                session.add(user)
                session.commit()
                auth_state.user_full_name = new_name
                self.full_name = new_name
                self.cnpj = new_cnpj
        self.is_editing = False
        return rx.toast.success("Profile updated successfully")

    @rx.event
    async def change_password(self, form_data: dict):
        """Change user password."""
        auth_state = await self.get_state(AuthState)
        current = form_data.get("current_password")
        new = form_data.get("new_password")
        confirm = form_data.get("confirm_password")
        if new != confirm:
            return rx.toast.error("New passwords do not match")
        with rx.session() as session:
            user = session.get(User, auth_state.user_id)
            if not user or not bcrypt.checkpw(
                current.encode("utf-8"), user.password_hash.encode("utf-8")
            ):
                return rx.toast.error("Invalid current password")
            hashed = bcrypt.hashpw(new.encode("utf-8"), bcrypt.gensalt()).decode(
                "utf-8"
            )
            user.password_hash = hashed
            session.add(user)
            session.commit()
        return rx.toast.success("Password changed successfully")

    @rx.event
    def toggle_edit(self):
        self.is_editing = not self.is_editing