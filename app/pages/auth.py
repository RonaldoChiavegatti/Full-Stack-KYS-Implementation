import reflex as rx
from app.states.auth import AuthState
from app.components.ui import form_input, primary_button


def auth_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("sparkles", class_name="h-8 w-8 text-emerald-500"),
                    rx.el.span(
                        "Fiscal Assistant", class_name="text-xl font-bold text-gray-900"
                    ),
                    class_name="flex items-center gap-2 mb-8 justify-center",
                ),
                href="/",
            ),
            content,
            class_name="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg border border-gray-100",
        ),
        class_name="min-h-screen w-full flex items-center justify-center bg-gray-50 font-['Poppins'] p-4",
    )


def login_page() -> rx.Component:
    return auth_layout(
        rx.el.div(
            rx.el.h1(
                "Welcome back",
                class_name="text-2xl font-bold text-gray-900 mb-2 text-center",
            ),
            rx.el.p(
                "Enter your credentials to access your account",
                class_name="text-sm text-gray-500 mb-8 text-center",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    rx.icon("badge_alert", class_name="h-4 w-4 text-red-500"),
                    rx.el.span(
                        AuthState.error_message, class_name="text-sm text-red-600"
                    ),
                    class_name="bg-red-50 p-3 rounded-lg flex items-center gap-2 mb-6",
                ),
                rx.fragment(),
            ),
            rx.el.form(
                form_input(
                    "Email Address", "you@example.com", "email", "email", "mail"
                ),
                form_input("Password", "••••••••", "password", "password", "lock"),
                primary_button("Sign In", type="submit", loading=AuthState.loading),
                on_submit=AuthState.login,
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.span(
                    "Don't have an account? ", class_name="text-sm text-gray-600"
                ),
                rx.el.a(
                    "Sign up",
                    href="/register",
                    class_name="text-sm font-semibold text-emerald-600 hover:text-emerald-700",
                ),
                class_name="mt-6 text-center",
            ),
        )
    )


def register_page() -> rx.Component:
    return auth_layout(
        rx.el.div(
            rx.el.h1(
                "Create an account",
                class_name="text-2xl font-bold text-gray-900 mb-2 text-center",
            ),
            rx.el.p(
                "Get started with Fiscal Assistant for MEIs",
                class_name="text-sm text-gray-500 mb-8 text-center",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    rx.icon("badge_alert", class_name="h-4 w-4 text-red-500"),
                    rx.el.span(
                        AuthState.error_message, class_name="text-sm text-red-600"
                    ),
                    class_name="bg-red-50 p-3 rounded-lg flex items-center gap-2 mb-6",
                ),
                rx.fragment(),
            ),
            rx.el.form(
                form_input("Full Name", "John Doe", "full_name", "text", "user"),
                form_input(
                    "CNPJ (Optional)", "00.000.000/0001-00", "cnpj", "text", "building"
                ),
                form_input(
                    "Email Address", "you@example.com", "email", "email", "mail"
                ),
                form_input("Password", "••••••••", "password", "password", "lock"),
                form_input(
                    "Confirm Password",
                    "••••••••",
                    "confirm_password",
                    "password",
                    "lock",
                ),
                primary_button(
                    "Create Account", type="submit", loading=AuthState.loading
                ),
                on_submit=AuthState.register,
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.span(
                    "Already have an account? ", class_name="text-sm text-gray-600"
                ),
                rx.el.a(
                    "Sign in",
                    href="/login",
                    class_name="text-sm font-semibold text-emerald-600 hover:text-emerald-700",
                ),
                class_name="mt-6 text-center",
            ),
        )
    )