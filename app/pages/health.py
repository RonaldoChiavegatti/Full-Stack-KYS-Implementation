import reflex as rx
from sqlmodel import text
import redis
import os
import logging
from app.components.layout import dashboard_layout
from app.states.auth import AuthState


class HealthState(rx.State):
    db_status: str = "Checking..."
    redis_status: str = "Checking..."
    overall_status: str = "Checking..."
    status_color: str = "gray"

    @rx.event
    async def check_health(self):
        """Check health of dependencies."""
        try:
            with rx.session() as session:
                session.exec(text("SELECT 1"))
            self.db_status = "Healthy"
        except Exception as e:
            logging.exception(f"Database health check failed: {e}")
            self.db_status = f"Unhealthy: {str(e)}"
        try:
            redis_url = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', '6379')}/0"
            r = redis.from_url(redis_url)
            r.ping()
            self.redis_status = "Healthy"
        except Exception as e:
            logging.exception(f"Redis health check failed: {e}")
            self.redis_status = f"Unhealthy: {str(e)}"
        if self.db_status == "Healthy" and self.redis_status == "Healthy":
            self.overall_status = "Healthy"
            self.status_color = "green"
        else:
            self.overall_status = "Degraded"
            self.status_color = "red"


def health_indicator(label: str, status: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(label, class_name="font-medium text-gray-700"),
        rx.el.span(
            status,
            class_name=rx.cond(
                status == "Healthy",
                "text-emerald-600 font-bold",
                rx.cond(
                    status == "Checking...", "text-gray-500", "text-red-600 font-bold"
                ),
            ),
        ),
        class_name="flex justify-between items-center p-3 bg-gray-50 rounded-lg",
    )


def health_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("System Health", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Monitor system status and connectivity.",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Service Status", class_name="text-lg font-bold text-gray-900 mb-4"
                ),
                rx.el.div(
                    health_indicator("Database", HealthState.db_status),
                    health_indicator("Redis Queue", HealthState.redis_status),
                    class_name="space-y-3 mb-6",
                ),
                rx.el.div(
                    rx.el.span(
                        "Overall Status: ", class_name="font-medium text-gray-700"
                    ),
                    rx.el.span(
                        HealthState.overall_status,
                        class_name=f"text-{HealthState.status_color}-600 font-bold text-lg",
                    ),
                    class_name="pt-4 border-t border-gray-100 flex justify-between items-center",
                ),
                class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm",
            ),
            class_name="max-w-md",
        ),
        class_name="p-8 max-w-7xl mx-auto",
    )


def health_page() -> rx.Component:
    return rx.el.div(
        dashboard_layout(health_content()),
        on_mount=[AuthState.check_auth, HealthState.check_health],
    )