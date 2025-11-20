import reflex as rx
from app.states.auth import AuthState


def sidebar_item(
    text: str, icon_name: str, href: str, active: bool = False
) -> rx.Component:
    base_classes = "flex items-center gap-3 rounded-lg px-4 py-2.5 text-sm font-medium transition-all"
    active_classes = "bg-emerald-50 text-emerald-700"
    inactive_classes = "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
    return rx.el.a(
        rx.icon(
            icon_name,
            class_name=f"h-5 w-5 {('text-emerald-600' if active else 'text-gray-400')}",
        ),
        rx.el.span(text),
        href=href,
        class_name=f"{base_classes} {(active_classes if active else inactive_classes)}",
    )


def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.aside(
            rx.el.div(
                rx.el.div(
                    rx.icon("sparkles", class_name="h-8 w-8 text-emerald-500"),
                    rx.el.span(
                        "Fiscal Assistant", class_name="text-xl font-bold text-gray-900"
                    ),
                    class_name="flex items-center gap-2 px-2",
                ),
                class_name="flex h-20 items-center border-b border-gray-100 px-6",
            ),
            rx.el.div(
                rx.el.nav(
                    rx.el.div(
                        rx.el.p(
                            "Main",
                            class_name="px-4 text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2",
                        ),
                        sidebar_item(
                            "Dashboard", "layout-dashboard", "/dashboard", active=True
                        ),
                        sidebar_item("Documents", "file-text", "/dashboard/documents"),
                        sidebar_item("AI Assistant", "bot", "/dashboard/chat"),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Settings",
                            class_name="px-4 text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2",
                        ),
                        sidebar_item("Profile", "user", "/dashboard/profile"),
                        sidebar_item("Billing", "credit-card", "/dashboard/billing"),
                        rx.cond(
                            AuthState.is_admin,
                            rx.el.div(
                                rx.el.p(
                                    "Admin",
                                    class_name="px-4 text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2 mt-8",
                                ),
                                sidebar_item("System", "shield", "/dashboard/admin"),
                            ),
                            rx.fragment(),
                        ),
                    ),
                    class_name="flex flex-col gap-1 px-4 py-6",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                AuthState.user_full_name,
                                class_name="text-sm font-medium text-gray-900",
                            ),
                            rx.el.p(
                                AuthState.user_email,
                                class_name="text-xs text-gray-500 truncate",
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    rx.el.button(
                        rx.icon(
                            "log-out",
                            class_name="h-5 w-5 text-gray-400 hover:text-red-500 transition-colors",
                        ),
                        on_click=AuthState.logout,
                        class_name="p-2 hover:bg-gray-100 rounded-lg transition-colors",
                    ),
                    class_name="flex items-center justify-between",
                ),
                class_name="border-t border-gray-100 p-4",
            ),
            class_name="fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r border-gray-100 bg-white",
        ),
        rx.el.main(content, class_name="pl-72 min-h-screen bg-gray-50/50"),
        class_name="font-['Poppins'] antialiased min-h-screen",
    )