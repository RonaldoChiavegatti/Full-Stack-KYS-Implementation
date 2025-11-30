import reflex as rx
from sqlmodel import select, func
from app.models import User, Billing, Revenue, Document
from app.states.auth import AuthState


class AdminState(rx.State):
    users: list[User] = []
    total_users: int = 0
    total_tokens: int = 0
    total_revenue_tracked: float = 0.0

    @rx.event
    async def load_admin_data(self):
        """Load all admin data."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or not auth_state.is_admin:
            return rx.redirect("/dashboard")
        with rx.session() as session:
            self.users = session.exec(select(User)).all()
            self.total_users = len(self.users)
            billing_total = (
                session.exec(select(func.sum(Billing.total_tokens))).one() or 0
            )
            self.total_tokens = billing_total
            revenue_total = session.exec(select(func.sum(Revenue.amount))).one() or 0
            self.total_revenue_tracked = revenue_total

    @rx.event
    async def toggle_admin(self, user_id: int):
        """Toggle admin status for a user."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_admin:
            return
        with rx.session() as session:
            user = session.get(User, user_id)
            if user:
                user.is_admin = not user.is_admin
                session.add(user)
                session.commit()
        return AdminState.load_admin_data