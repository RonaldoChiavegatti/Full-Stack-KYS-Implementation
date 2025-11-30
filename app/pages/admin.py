import reflex as rx
from app.components.layout import dashboard_layout
from app.states.admin import AdminState
from app.states.auth import AuthState


def admin_stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 text-{color}-600"),
            class_name=f"h-12 w-12 rounded-lg bg-{color}-100 flex items-center justify-center mb-4",
        ),
        rx.el.h3(title, class_name="text-sm font-medium text-gray-500 mb-1"),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm",
    )


def user_row(user: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="h-8 w-8 text-gray-400"),
                    class_name="h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center mr-3",
                ),
                rx.el.div(
                    rx.el.p(user.full_name, class_name="font-medium text-gray-900"),
                    rx.el.p(user.email, class_name="text-xs text-gray-500"),
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                user.is_admin,
                rx.el.span(
                    "Admin",
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800",
                ),
                rx.el.span(
                    "User",
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            user.created_at,
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.button(
                rx.cond(user.is_admin, "Remove Admin", "Make Admin"),
                on_click=lambda: AdminState.toggle_admin(user.id),
                class_name="text-sm font-medium text-emerald-600 hover:text-emerald-700",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-50 last:border-none",
    )


def admin_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "System Administration", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.p(
                "Overview of system metrics and user management.",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            admin_stat_card("Total Users", AdminState.total_users, "users", "blue"),
            admin_stat_card(
                "Total Tokens", AdminState.total_tokens, "database", "purple"
            ),
            admin_stat_card(
                "Revenue Tracked",
                f"R$ {AdminState.total_revenue_tracked:.2f}",
                "bar-chart-3",
                "emerald",
            ),
            class_name="grid md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.h3(
                "User Directory",
                class_name="text-lg font-bold text-gray-900 mb-4 px-6 pt-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "User",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Role",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Joined",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        ),
                        class_name="bg-gray-50/50 border-b border-gray-100",
                    ),
                    rx.el.tbody(
                        rx.foreach(AdminState.users, user_row), class_name="bg-white"
                    ),
                    class_name="min-w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden",
        ),
        class_name="p-8 max-w-7xl mx-auto",
    )


def admin_page() -> rx.Component:
    return rx.el.div(
        dashboard_layout(admin_content()),
        on_mount=[AuthState.check_auth, AdminState.load_admin_data],
    )