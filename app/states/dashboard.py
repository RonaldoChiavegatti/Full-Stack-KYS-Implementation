import reflex as rx
from sqlmodel import select
from datetime import datetime, date
import logging
from app.models import Revenue
from app.states.auth import AuthState


class DashboardState(rx.State):
    revenue_entries: list[Revenue] = []
    chart_data: list[dict] = []
    current_month_revenue: float = 0.0
    annual_revenue: float = 0.0
    mei_limit_percent: float = 0.0
    limit_status: str = "green"
    is_add_modal_open: bool = False
    new_entry_amount: str = ""
    new_entry_description: str = ""
    new_entry_category: str = "Service"
    new_entry_date: str = datetime.now().strftime("%Y-%m-%d")

    @rx.event
    async def load_data(self):
        """Load all dashboard data."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or auth_state.user_id == -1:
            return
        user_id = auth_state.user_id
        with rx.session() as session:
            query = (
                select(Revenue)
                .where(Revenue.user_id == user_id)
                .order_by(Revenue.date.desc())
            )
            self.revenue_entries = session.exec(query).all()
        self.calculate_stats()
        self.prepare_chart_data()

    @rx.event
    def calculate_stats(self):
        """Calculate dashboard statistics."""
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        self.current_month_revenue = 0.0
        self.annual_revenue = 0.0
        for entry in self.revenue_entries:
            entry_date = datetime.strptime(entry.date, "%Y-%m-%d").date()
            if entry_date.year == current_year:
                self.annual_revenue += entry.amount
                if entry_date.month == current_month:
                    self.current_month_revenue += entry.amount
        limit = 81000.0
        self.mei_limit_percent = self.annual_revenue / limit * 100
        if self.mei_limit_percent >= 100:
            self.limit_status = "red"
        elif self.mei_limit_percent >= 70:
            self.limit_status = "orange"
        else:
            self.limit_status = "green"

    @rx.event
    def prepare_chart_data(self):
        """Prepare data for the revenue chart (monthly breakdown)."""
        current_year = datetime.now().year
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        monthly_totals = {i: 0.0 for i in range(1, 13)}
        for entry in self.revenue_entries:
            entry_date = datetime.strptime(entry.date, "%Y-%m-%d").date()
            if entry_date.year == current_year:
                monthly_totals[entry_date.month] += entry.amount
        self.chart_data = [
            {"name": months[i - 1], "revenue": monthly_totals[i]} for i in range(1, 13)
        ]

    @rx.event
    def toggle_add_modal(self):
        self.is_add_modal_open = not self.is_add_modal_open

    @rx.event
    def set_new_entry_amount(self, value: str):
        self.new_entry_amount = value

    @rx.event
    def set_new_entry_description(self, value: str):
        self.new_entry_description = value

    @rx.event
    def set_new_entry_category(self, value: str):
        self.new_entry_category = value

    @rx.event
    def set_new_entry_date(self, value: str):
        self.new_entry_date = value

    @rx.event
    async def add_revenue(self):
        """Add a new revenue entry."""
        auth_state = await self.get_state(AuthState)
        if not self.new_entry_amount or not self.new_entry_date:
            return
        try:
            amount = float(self.new_entry_amount)
        except ValueError as e:
            logging.exception(f"Error converting amount to float: {e}")
            return
        with rx.session() as session:
            new_revenue = Revenue(
                user_id=auth_state.user_id,
                amount=amount,
                description=self.new_entry_description,
                category=self.new_entry_category,
                date=self.new_entry_date,
            )
            session.add(new_revenue)
            session.commit()
        self.new_entry_amount = ""
        self.new_entry_description = ""
        self.is_add_modal_open = False
        return DashboardState.load_data

    @rx.event
    def delete_revenue(self, revenue_id: int):
        """Delete a revenue entry."""
        with rx.session() as session:
            revenue = session.get(Revenue, revenue_id)
            if revenue:
                session.delete(revenue)
                session.commit()
        return DashboardState.load_data