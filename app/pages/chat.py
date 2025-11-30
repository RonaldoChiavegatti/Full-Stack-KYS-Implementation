import reflex as rx
from app.components.layout import dashboard_layout
from app.states.chat import ChatState
from app.states.auth import AuthState


def message_bubble(message: dict) -> rx.Component:
    is_user = message.role == "user"
    return rx.el.div(
        rx.el.div(
            rx.cond(
                is_user,
                rx.el.div(
                    rx.icon("user", class_name="h-4 w-4 text-white"),
                    class_name="h-8 w-8 rounded-full bg-emerald-600 flex items-center justify-center shrink-0 order-2",
                ),
                rx.el.div(
                    rx.icon("bot", class_name="h-4 w-4 text-emerald-600"),
                    class_name="h-8 w-8 rounded-full bg-emerald-100 flex items-center justify-center shrink-0 order-1",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.markdown(message.content),
                    class_name=rx.cond(is_user, "text-white", "text-gray-800"),
                ),
                class_name=rx.cond(
                    is_user,
                    "bg-emerald-600 rounded-2xl rounded-tr-none px-4 py-2 max-w-[80%] order-1 mr-2 shadow-sm",
                    "bg-white border border-gray-100 rounded-2xl rounded-tl-none px-4 py-2 max-w-[80%] order-2 ml-2 shadow-sm",
                ),
            ),
            class_name=f"flex items-end mb-4 {rx.cond(is_user, 'justify-end', 'justify-start')}",
        ),
        class_name="w-full",
    )


def chat_interface() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "AI Tax Assistant", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Ask questions about your documents and MEI taxes",
                    class_name="text-sm text-gray-500",
                ),
            ),
            rx.el.div(
                rx.icon("zap", class_name="h-4 w-4 text-yellow-500 mr-1"),
                rx.el.span(
                    f"{ChatState.current_month_tokens} tokens used",
                    class_name="text-sm font-medium text-gray-600",
                ),
                class_name="flex items-center bg-yellow-50 px-3 py-1 rounded-full border border-yellow-100",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.cond(
                    ChatState.messages,
                    rx.foreach(ChatState.messages, message_bubble),
                    rx.el.div(
                        rx.icon(
                            "message-square", class_name="h-12 w-12 text-gray-300 mb-4"
                        ),
                        rx.el.p(
                            "No messages yet. Start a conversation!",
                            class_name="text-gray-400 font-medium",
                        ),
                        class_name="flex flex-col items-center justify-center h-full opacity-50",
                    ),
                ),
                rx.cond(
                    ChatState.is_loading,
                    rx.el.div(
                        rx.el.div(
                            rx.icon("bot", class_name="h-4 w-4 text-emerald-600"),
                            class_name="h-8 w-8 rounded-full bg-emerald-100 flex items-center justify-center shrink-0 mr-2",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                            ),
                            rx.el.div(
                                class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75"
                            ),
                            rx.el.div(
                                class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"
                            ),
                            class_name="bg-white border border-gray-100 rounded-2xl rounded-tl-none px-4 py-3 shadow-sm flex items-center gap-1 w-16",
                        ),
                        class_name="flex items-end mb-4 justify-start animate-pulse",
                    ),
                    rx.fragment(),
                ),
                id="chat-container",
                class_name="flex-1 overflow-y-auto p-4 space-y-4 min-h-0",
            ),
            rx.el.div(
                rx.el.form(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Type your question here...",
                            name="message",
                            class_name="flex-1 rounded-lg border-gray-200 border p-3 text-sm focus:border-emerald-500 focus:ring-emerald-500 shadow-sm",
                        ),
                        rx.el.button(
                            rx.icon("send-horizontal", class_name="h-5 w-5"),
                            type="submit",
                            disabled=ChatState.is_loading,
                            class_name="p-3 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm",
                        ),
                        class_name="flex gap-2",
                    ),
                    on_submit=ChatState.send_message,
                    reset_on_submit=True,
                    class_name="w-full",
                ),
                class_name="p-4 border-t border-gray-100 bg-white rounded-b-xl",
            ),
            class_name="flex flex-col h-[600px] bg-gray-50/50 rounded-xl border border-gray-200 shadow-sm overflow-hidden",
        ),
        class_name="p-8 max-w-5xl mx-auto",
    )


def chat_page() -> rx.Component:
    return rx.el.div(
        dashboard_layout(chat_interface()),
        on_mount=[AuthState.check_auth, ChatState.load_history],
    )