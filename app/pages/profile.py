import reflex as rx
from app.components.layout import dashboard_layout
from app.components.ui import form_input, primary_button
from app.states.profile import ProfileState
from app.states.auth import AuthState


def profile_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Profile Settings", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Manage your account information and preferences.",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Personal Information",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.form(
                        form_input(
                            "Full Name", "John Doe", "full_name", "text", "user"
                        ),
                        form_input(
                            "CNPJ", "00.000.000/0001-00", "cnpj", "text", "building"
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email Address",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "mail",
                                    class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5",
                                ),
                                rx.el.input(
                                    disabled=True,
                                    class_name="w-full rounded-lg border-gray-200 border p-2.5 text-sm bg-gray-50 pl-10 text-gray-500 cursor-not-allowed",
                                    default_value=ProfileState.email,
                                    key=ProfileState.email,
                                ),
                                class_name="relative",
                            ),
                            class_name="w-full mb-4",
                        ),
                        primary_button("Save Changes", type="submit"),
                        on_submit=ProfileState.save_profile,
                    ),
                ),
                class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm",
            ),
            rx.el.div(
                rx.el.h3(
                    "Change Password", class_name="text-lg font-bold text-gray-900 mb-4"
                ),
                rx.el.form(
                    form_input(
                        "Current Password",
                        "••••••••",
                        "current_password",
                        "password",
                        "lock",
                    ),
                    form_input(
                        "New Password", "••••••••", "new_password", "password", "lock"
                    ),
                    form_input(
                        "Confirm New Password",
                        "••••••••",
                        "confirm_password",
                        "password",
                        "lock",
                    ),
                    primary_button("Update Password", type="submit"),
                    on_submit=ProfileState.change_password,
                ),
                class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm",
            ),
            class_name="grid md:grid-cols-2 gap-8",
        ),
        class_name="p-8 max-w-7xl mx-auto",
    )


def profile_page() -> rx.Component:
    return rx.el.div(
        dashboard_layout(profile_content()),
        on_mount=[AuthState.check_auth, ProfileState.load_profile],
    )