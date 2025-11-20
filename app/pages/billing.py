import reflex as rx
from app.components.layout import dashboard_layout
from app.states.billing import BillingState
from app.states.auth import AuthState


def plan_card(
    name: str, price: str, features: list[str], current: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(name, class_name="text-xl font-bold text-gray-900"),
            rx.cond(
                current,
                rx.el.span(
                    "Current Plan",
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800",
                ),
                rx.fragment(),
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.div(
            rx.el.span(price, class_name="text-3xl font-bold text-gray-900"),
            rx.el.span("/month", class_name="text-gray-500 ml-1"),
            class_name="mb-6",
        ),
        rx.el.ul(
            rx.foreach(
                features,
                lambda f: rx.el.li(
                    rx.icon("check", class_name="h-5 w-5 text-emerald-500 mr-2"),
                    rx.el.span(f, class_name="text-gray-600"),
                    class_name="flex items-center",
                ),
            ),
            class_name="space-y-3 mb-8",
        ),
        rx.el.button(
            rx.cond(current, "Current Plan", "Upgrade"),
            disabled=current,
            on_click=lambda: BillingState.upgrade_plan(name),
            class_name=rx.cond(
                current,
                "w-full py-2 px-4 rounded-lg bg-gray-100 text-gray-500 font-medium cursor-not-allowed",
                "w-full py-2 px-4 rounded-lg bg-emerald-600 text-white font-medium hover:bg-emerald-700 transition-colors shadow-sm",
            ),
        ),
        class_name=f"p-6 bg-white rounded-xl border {rx.cond(current, 'border-emerald-500 ring-1 ring-emerald-500', 'border-gray-200')} shadow-sm",
    )


def billing_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Billing & Plans", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Manage your subscription and view usage.",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Current Usage", class_name="text-lg font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Monthly Tokens",
                            class_name="text-sm font-medium text-gray-500",
                        ),
                        rx.el.p(
                            f"{BillingState.current_tokens} / {BillingState.token_limit}",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Estimated Cost",
                            class_name="text-sm font-medium text-gray-500",
                        ),
                        rx.el.p(
                            f"${BillingState.estimated_cost:.2f}",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        class_name="text-right",
                    ),
                    class_name="flex justify-between items-end mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        style={"width": f"{BillingState.usage_percentage}%"},
                        class_name="h-full bg-emerald-500 rounded-full transition-all duration-500",
                    ),
                    class_name="w-full h-3 bg-gray-100 rounded-full overflow-hidden",
                ),
                rx.el.p(
                    "Resets on the 1st of next month",
                    class_name="text-xs text-gray-400 mt-2",
                ),
                class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm mb-8",
            ),
        ),
        rx.el.div(
            rx.el.h2(
                "Available Plans", class_name="text-lg font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                plan_card(
                    "Free",
                    "$0",
                    ["10,000 tokens/month", "Basic Support", "Standard OCR"],
                    BillingState.plan_type == "Free",
                ),
                plan_card(
                    "Pro",
                    "$29",
                    [
                        "100,000 tokens/month",
                        "Priority Support",
                        "Advanced OCR",
                        "Analytics",
                    ],
                    BillingState.plan_type == "Pro",
                ),
                plan_card(
                    "Enterprise",
                    "$99",
                    [
                        "1M tokens/month",
                        "24/7 Support",
                        "Custom Integration",
                        "API Access",
                    ],
                    BillingState.plan_type == "Enterprise",
                ),
                class_name="grid md:grid-cols-3 gap-6",
            ),
        ),
        class_name="p-8 max-w-7xl mx-auto",
    )


def billing_page() -> rx.Component:
    return rx.el.div(
        dashboard_layout(billing_content()),
        on_mount=[AuthState.check_auth, BillingState.load_billing],
    )