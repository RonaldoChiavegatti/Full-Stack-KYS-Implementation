import reflex as rx


def form_input(
    label: str, placeholder: str, name: str, type: str = "text", icon: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.div(
            rx.cond(
                icon != "",
                rx.icon(
                    icon,
                    class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5",
                ),
                rx.fragment(),
            ),
            rx.el.input(
                placeholder=placeholder,
                name=name,
                type=type,
                class_name=f"w-full rounded-lg border-gray-200 border p-2.5 text-sm shadow-sm transition-colors focus:border-emerald-500 focus:ring-emerald-500 focus:outline-none {('pl-10' if icon else '')}",
            ),
            class_name="relative",
        ),
        class_name="w-full mb-4",
    )


def primary_button(
    text: str, type: str = "button", loading: bool = False
) -> rx.Component:
    return rx.el.button(
        rx.cond(
            loading,
            rx.el.span(
                "Processing...", class_name="flex items-center justify-center gap-2"
            ),
            text,
        ),
        type=type,
        class_name="w-full rounded-lg bg-gradient-to-r from-emerald-500 to-emerald-600 px-5 py-3 text-sm font-medium text-white shadow-md hover:from-emerald-600 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 transform transition-all active:scale-[0.98]",
    )


def outline_button(text: str, on_click=None) -> rx.Component:
    return rx.el.button(
        text,
        on_click=on_click,
        class_name="rounded-lg border border-gray-300 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 transition-colors",
    )