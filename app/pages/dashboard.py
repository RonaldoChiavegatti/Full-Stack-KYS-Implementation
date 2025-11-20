import reflex as rx
from app.components.layout import dashboard_layout
from app.states.auth import AuthState
from app.states.dashboard import DashboardState
from app.components.ui import primary_button

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E8E8E8",
        "borderRadius": "0.75rem",
        "boxShadow": "0px 4px 6px -1px rgba(0, 0, 0, 0.1), 0px 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "fontFamily": "Poppins, sans-serif",
        "fontSize": "0.875rem",
        "padding": "0.5rem 0.75rem",
    },
    "item_style": {"color": "#10B981", "fontWeight": "600"},
    "label_style": {"color": "#374151", "fontWeight": "500", "marginBottom": "0.25rem"},
    "separator": "",
}


def stat_card(
    title: str, value: str, subtitle: str, status: str = "green"
) -> rx.Component:
    return rx.el.div(
        rx.el.p(title, class_name="text-sm font-medium text-gray-500 mb-1"),
        rx.el.div(
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
            rx.el.div(
                rx.cond(
                    status == "green",
                    rx.icon("trending-up", class_name="h-4 w-4 text-emerald-500"),
                    rx.cond(
                        status == "orange",
                        rx.icon("minus", class_name="h-4 w-4 text-orange-500"),
                        rx.icon("badge_alert", class_name="h-4 w-4 text-red-500"),
                    ),
                ),
                class_name="flex items-center justify-center w-8 h-8 rounded-full bg-gray-50",
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.p(subtitle, class_name="text-xs text-gray-400 mt-2"),
        class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )


def revenue_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Monthly Revenue", class_name="text-lg font-bold text-gray-900 mb-6"),
        rx.el.div(
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False, class_name="opacity-25"
                ),
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.area(
                    data_key="revenue",
                    stroke="#10B981",
                    fill="#D1FAE5",
                    type_="monotone",
                    stroke_width=2,
                ),
                rx.recharts.x_axis(
                    data_key="name",
                    axis_line=False,
                    tick_line=False,
                    tick_size=10,
                    custom_attrs={"fontSize": "12px", "fill": "#6B7280"},
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    tick_size=10,
                    custom_attrs={"fontSize": "12px", "fill": "#6B7280"},
                    unit="R$",
                ),
                data=DashboardState.chart_data,
                height=300,
                width="100%",
            ),
            class_name="w-full h-[300px]",
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm w-full",
    )


def add_revenue_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                "Add Revenue",
                class_name="flex items-center px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors text-sm font-medium shadow-sm",
            )
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Add New Revenue", class_name="text-lg font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Amount (R$)",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="number",
                        placeholder="0.00",
                        on_change=DashboardState.set_new_entry_amount,
                        class_name="w-full rounded-lg border-gray-300 border p-2.5 text-sm focus:border-emerald-500 focus:ring-emerald-500",
                        default_value=DashboardState.new_entry_amount,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Description",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        placeholder="Client Payment...",
                        on_change=DashboardState.set_new_entry_description,
                        class_name="w-full rounded-lg border-gray-300 border p-2.5 text-sm focus:border-emerald-500 focus:ring-emerald-500",
                        default_value=DashboardState.new_entry_description,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Category",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("Service", value="Service"),
                        rx.el.option("Product Sale", value="Product Sale"),
                        rx.el.option("Consulting", value="Consulting"),
                        rx.el.option("Other", value="Other"),
                        value=DashboardState.new_entry_category,
                        on_change=DashboardState.set_new_entry_category,
                        class_name="w-full rounded-lg border-gray-300 border p-2.5 text-sm focus:border-emerald-500 focus:ring-emerald-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Date",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="date",
                        on_change=DashboardState.set_new_entry_date,
                        class_name="w-full rounded-lg border-gray-300 border p-2.5 text-sm focus:border-emerald-500 focus:ring-emerald-500",
                        default_value=DashboardState.new_entry_date,
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-lg mr-2",
                        )
                    ),
                    rx.dialog.close(
                        rx.el.button(
                            "Save Revenue",
                            on_click=DashboardState.add_revenue,
                            class_name="px-4 py-2 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg",
                        )
                    ),
                    class_name="flex justify-end",
                ),
            ),
            class_name="bg-white p-6 rounded-xl shadow-xl max-w-md w-full",
        ),
    )


def revenue_table_row(revenue: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(revenue.description, class_name="font-medium text-gray-900"),
                rx.el.p(revenue.category, class_name="text-xs text-gray-500"),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            revenue.date, class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        ),
        rx.el.td(
            rx.el.span(f"R$ {revenue.amount}", class_name="font-medium text-gray-900"),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon(
                    "trash-2", class_name="h-4 w-4 text-red-400 hover:text-red-600"
                ),
                on_click=lambda: DashboardState.delete_revenue(revenue.id),
                class_name="p-1 rounded hover:bg-red-50 transition-colors",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-50 last:border-none",
    )


def revenue_history_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Recent Transactions", class_name="text-lg font-bold text-gray-900"
            ),
            add_revenue_modal(),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Description",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Date",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Amount",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "",
                            class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                    ),
                    class_name="bg-gray-50/50",
                ),
                rx.el.tbody(
                    rx.foreach(DashboardState.revenue_entries, revenue_table_row),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-hidden rounded-lg border border-gray-200",
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm mt-8",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Overview", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Track your revenue and stay within the MEI limits.",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            stat_card(
                "Current Month",
                f"R$ {DashboardState.current_month_revenue}",
                "Revenue this month",
                "green",
            ),
            stat_card(
                "Annual Revenue",
                f"R$ {DashboardState.annual_revenue}",
                f"{DashboardState.mei_limit_percent:.1f}% of limit used",
                DashboardState.limit_status,
            ),
            stat_card(
                "Limit Remaining",
                f"R$ {81000 - DashboardState.annual_revenue}",
                "Available until Dec 31",
                DashboardState.limit_status,
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        revenue_chart(),
        revenue_history_table(),
        class_name="p-8 max-w-7xl mx-auto",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        dashboard_layout(dashboard_content()),
        on_mount=[AuthState.check_auth, DashboardState.load_data],
    )