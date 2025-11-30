import reflex as rx
from app.components.layout import dashboard_layout
from app.states.documents import DocumentState
from app.states.auth import AuthState


def upload_zone() -> rx.Component:
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud-upload", class_name="h-10 w-10 text-emerald-500 mb-3"),
                rx.el.p(
                    "Drag & drop invoices or receipts here",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.p(
                    "Support for PDF, JPG, PNG (Max 10MB)",
                    class_name="text-xs text-gray-500 mt-1",
                ),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-emerald-100 rounded-xl bg-emerald-50/30 hover:bg-emerald-50 transition-colors cursor-pointer",
            ),
            id=DocumentState.upload_id,
            accept={
                "application/pdf": [".pdf"],
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
            },
            max_files=5,
            class_name="w-full",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files(DocumentState.upload_id),
                lambda file: rx.el.div(
                    rx.icon("file", class_name="h-4 w-4 text-emerald-600"),
                    rx.el.span(file, class_name="text-sm text-gray-600 truncate"),
                    class_name="flex items-center gap-2 p-2 bg-white border border-gray-100 rounded-lg shadow-sm",
                ),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-4",
        ),
        rx.cond(
            DocumentState.is_uploading,
            rx.el.div(
                rx.icon("loader", class_name="h-5 w-5 animate-spin text-emerald-600"),
                rx.el.span(
                    "Uploading...", class_name="text-sm font-medium text-emerald-600"
                ),
                class_name="flex items-center gap-2 mt-4 justify-center",
            ),
            rx.el.button(
                "Upload Files",
                on_click=DocumentState.handle_upload(
                    rx.upload_files(upload_id=DocumentState.upload_id)
                ),
                class_name="mt-4 w-full sm:w-auto px-6 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors shadow-sm",
            ),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm mb-8",
    )


def status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "completed",
            rx.el.span(
                "Completed",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            ),
        ),
        (
            "processing",
            rx.el.span(
                "Processing",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
            ),
        ),
        (
            "failed",
            rx.el.span(
                "Failed",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
            ),
        ),
        rx.el.span(
            "Pending",
            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )


def document_row(doc: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("file-text", class_name="h-5 w-5 text-gray-400 mr-3"),
                rx.el.span(
                    doc.filename, class_name="text-sm font-medium text-gray-900"
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(status_badge(doc.status), class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            rx.el.span(doc.created_at, class_name="text-sm text-gray-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "eye", class_name="h-4 w-4 text-gray-500 hover:text-emerald-600"
                    ),
                    on_click=DocumentState.open_preview(doc),
                    class_name="p-1 rounded hover:bg-gray-50 transition-colors",
                ),
                rx.el.button(
                    rx.icon(
                        "trash-2", class_name="h-4 w-4 text-gray-500 hover:text-red-600"
                    ),
                    on_click=DocumentState.delete_document(doc.id, doc.minio_path),
                    class_name="p-1 rounded hover:bg-gray-50 transition-colors",
                ),
                class_name="flex items-center gap-2 justify-end",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50/50 transition-colors border-b border-gray-100 last:border-none",
    )


def preview_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Document Preview", class_name="text-lg font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        "Extracted Text",
                        class_name="text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.div(
                        DocumentState.preview_text,
                        class_name="p-4 bg-gray-50 rounded-lg text-sm text-gray-600 font-mono whitespace-pre-wrap h-64 overflow-y-auto border border-gray-200",
                    ),
                    class_name="w-full lg:w-1/2",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Original File",
                        class_name="text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.iframe(
                        src=DocumentState.preview_url,
                        class_name="w-full h-64 rounded-lg border border-gray-200 bg-white",
                    ),
                    class_name="w-full lg:w-1/2",
                ),
                class_name="flex flex-col lg:flex-row gap-6",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Close",
                        on_click=DocumentState.close_preview,
                        class_name="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors",
                    )
                ),
                class_name="mt-6 flex justify-end",
            ),
            class_name="bg-white p-6 rounded-xl shadow-xl max-w-4xl w-full",
        ),
        open=DocumentState.is_preview_open,
        on_open_change=DocumentState.close_preview,
    )


def documents_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Documents", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Upload and manage your fiscal documents.",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        upload_zone(),
        rx.el.div(
            rx.el.h3(
                "Recent Uploads",
                class_name="text-lg font-bold text-gray-900 mb-4 px-6 pt-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Name",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Date",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        ),
                        class_name="bg-gray-50/50 border-b border-gray-100",
                    ),
                    rx.el.tbody(
                        rx.cond(
                            DocumentState.documents,
                            rx.foreach(DocumentState.documents, document_row),
                            rx.el.tr(
                                rx.el.td(
                                    "No documents found.",
                                    col_span=4,
                                    class_name="px-6 py-8 text-center text-sm text-gray-500",
                                )
                            ),
                        ),
                        class_name="bg-white",
                    ),
                    class_name="min-w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden",
        ),
        preview_modal(),
        class_name="p-8 max-w-7xl mx-auto",
    )


def documents_page() -> rx.Component:
    return rx.el.div(
        dashboard_layout(documents_content()),
        on_mount=[AuthState.check_auth, DocumentState.load_documents],
    )