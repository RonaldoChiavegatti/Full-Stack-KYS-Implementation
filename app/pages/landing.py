import reflex as rx
from app.components.ui import primary_button, outline_button


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.icon("sparkles", class_name="h-6 w-6 text-emerald-500"),
                rx.el.span(
                    "Fiscal Assistant", class_name="text-lg font-bold text-gray-900"
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.a(
                    "Features",
                    href="#features",
                    class_name="text-sm font-medium text-gray-600 hover:text-emerald-600 transition-colors",
                ),
                rx.el.a(
                    "Pricing",
                    href="#pricing",
                    class_name="text-sm font-medium text-gray-600 hover:text-emerald-600 transition-colors",
                ),
                rx.el.a(
                    "Login",
                    href="/login",
                    class_name="text-sm font-medium text-gray-600 hover:text-emerald-600 transition-colors",
                ),
                rx.el.a(
                    rx.el.button(
                        "Get Started",
                        class_name="bg-emerald-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-emerald-600 transition-colors",
                    ),
                    href="/register",
                ),
                class_name="flex items-center gap-8",
            ),
            class_name="container mx-auto flex items-center justify-between h-20 px-4",
        ),
        class_name="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md border-b border-gray-100 z-50",
    )


def hero_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "SaaS for Brazilian MEIs",
                class_name="inline-block rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-600 mb-6",
            ),
            rx.el.h1(
                "Simplify your Tax Declarations with AI",
                class_name="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight tracking-tight",
            ),
            rx.el.p(
                "Automate your MEI obligations, track revenue limits, and get instant answers to tax questions with our AI-powered assistant.",
                class_name="text-lg text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed",
            ),
            rx.el.div(
                rx.el.a(
                    primary_button("Start Free Trial"),
                    href="/register",
                    class_name="w-full sm:w-auto",
                ),
                rx.el.a(
                    outline_button("View Demo"), href="#", class_name="w-full sm:w-auto"
                ),
                class_name="flex flex-col sm:flex-row items-center justify-center gap-4",
            ),
            class_name="container mx-auto px-4 pt-32 pb-20 text-center",
        ),
        class_name="bg-gradient-to-b from-white to-gray-50",
    )


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-emerald-500"),
            class_name="h-12 w-12 rounded-lg bg-emerald-50 flex items-center justify-center mb-4",
        ),
        rx.el.h3(title, class_name="text-lg font-bold text-gray-900 mb-2"),
        rx.el.p(description, class_name="text-gray-600 leading-relaxed"),
        class_name="p-6 rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )


def landing_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        hero_section(),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Everything you need to stay compliant",
                        class_name="text-3xl font-bold text-gray-900 mb-4",
                    ),
                    rx.el.p(
                        "Powerful tools designed specifically for the needs of Microentrepreneurs.",
                        class_name="text-gray-600 max-w-2xl mx-auto",
                    ),
                    class_name="text-center mb-16",
                ),
                rx.el.div(
                    feature_card(
                        "bar-chart-3",
                        "Revenue Tracking",
                        "Monitor your annual R$81,000 limit with real-time charts and alerts.",
                    ),
                    feature_card(
                        "scan-text",
                        "Smart OCR",
                        "Upload invoices and receipts. Our system automatically extracts the data you need.",
                    ),
                    feature_card(
                        "bot",
                        "AI Tax Assistant",
                        "Chat with our LLM to answer complex tax questions instantly and accurately.",
                    ),
                    class_name="grid md:grid-cols-3 gap-8",
                ),
                class_name="container mx-auto px-4 py-20",
            ),
            class_name="bg-white",
        ),
        class_name="font-['Poppins'] min-h-screen",
    )