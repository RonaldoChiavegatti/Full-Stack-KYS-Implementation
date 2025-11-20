import reflex as rx
from sqlmodel import select
from app.models import Billing
from app.states.auth import AuthState


class BillingState(rx.State):
    plan_type: str = "Free"
    current_tokens: int = 0
    total_tokens: int = 0
    token_limit: int = 10000
    usage_percentage: float = 0.0
    estimated_cost: float = 0.0
    token_rate: float = 5e-05

    @rx.event
    async def load_billing(self):
        """Load billing data for the user."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        with rx.session() as session:
            billing = session.exec(
                select(Billing).where(Billing.user_id == auth_state.user_id)
            ).first()
            if billing:
                self.plan_type = billing.plan_type.capitalize()
                self.current_tokens = billing.current_month_tokens
                self.total_tokens = billing.total_tokens
            else:
                new_billing = Billing(
                    user_id=auth_state.user_id,
                    current_month_tokens=0,
                    total_tokens=0,
                    plan_type="free",
                )
                session.add(new_billing)
                session.commit()
                session.refresh(new_billing)
                self.plan_type = "Free"
                self.current_tokens = 0
                self.total_tokens = 0
        if self.plan_type.lower() == "pro":
            self.token_limit = 100000
        elif self.plan_type.lower() == "enterprise":
            self.token_limit = 1000000
        else:
            self.token_limit = 10000
        self.usage_percentage = min(self.current_tokens / self.token_limit * 100, 100)
        self.estimated_cost = self.current_tokens * self.token_rate

    @rx.event
    async def upgrade_plan(self, new_plan: str):
        """Simulate plan upgrade."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        with rx.session() as session:
            billing = session.exec(
                select(Billing).where(Billing.user_id == auth_state.user_id)
            ).first()
            if billing:
                billing.plan_type = new_plan.lower()
                session.add(billing)
                session.commit()
        yield rx.toast.success(f"Successfully upgraded to {new_plan} plan!")
        yield BillingState.load_billing