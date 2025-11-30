import reflex as rx
from sqlmodel import select
import os
from google import genai
from google.genai import types
import logging
from datetime import datetime
from app.models import ChatMessage, Document, Billing
from app.states.auth import AuthState


class ChatState(rx.State):
    messages: list[ChatMessage] = []
    is_loading: bool = False
    current_month_tokens: int = 0

    @rx.event
    async def load_history(self):
        """Load chat history and token usage."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        with rx.session() as session:
            query = (
                select(ChatMessage)
                .where(ChatMessage.user_id == auth_state.user_id)
                .order_by(ChatMessage.created_at)
            )
            self.messages = session.exec(query).all()
            billing = session.exec(
                select(Billing).where(Billing.user_id == auth_state.user_id)
            ).first()
            if billing:
                self.current_month_tokens = billing.current_month_tokens

    @rx.event
    async def send_message(self, form_data: dict):
        """Send message to Gemini with RAG context."""
        user_query = form_data.get("message", "")
        if not user_query.strip():
            return
        auth_state = await self.get_state(AuthState)
        self.is_loading = True
        user_msg = ChatMessage(
            user_id=auth_state.user_id, role="user", content=user_query, tokens_used=0
        )
        with rx.session() as session:
            session.add(user_msg)
            session.commit()
            session.refresh(user_msg)
        self.messages.append(user_msg)
        yield
        context_text = ""
        with rx.session() as session:
            docs = session.exec(
                select(Document)
                .where(Document.user_id == auth_state.user_id)
                .where(Document.extracted_text != None)
            ).all()
            relevant_chunks = []
            query_terms = user_query.lower().split()
            for doc in docs:
                if not doc.extracted_text:
                    continue
                score = sum(
                    (1 for term in query_terms if term in doc.extracted_text.lower())
                )
                if score > 0:
                    relevant_chunks.append((score, doc.extracted_text))
            relevant_chunks.sort(key=lambda x: x[0], reverse=True)
            context_text = """

---

""".join([chunk[1] for chunk in relevant_chunks[:3]])
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise Exception("Google API Key not configured")
            client = genai.Client(api_key=api_key)
            system_instruction = "You are a helpful fiscal assistant for Brazilian MEIs (Microentrepreneurs). Answer the user's question accurately. If relevant document context is provided below, strictly use it to answer. If the context doesn't contain the answer, say so but try to help with general knowledge."
            full_prompt = user_query
            if context_text:
                full_prompt = f"Context from user documents:\n{context_text}\n\nUser Question: {user_query}"
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
            )
            response_text = response.text
            tokens_used = 0
            if response.usage_metadata:
                tokens_used = response.usage_metadata.total_token_count
            else:
                tokens_used = len(response_text.split()) + len(full_prompt.split())
        except Exception as e:
            logging.exception(f"Gemini API Error: {e}")
            response_text = "I apologize, but I encountered an error processing your request. Please try again later."
            tokens_used = 0
        with rx.session() as session:
            bot_msg = ChatMessage(
                user_id=auth_state.user_id,
                role="model",
                content=response_text,
                tokens_used=tokens_used,
            )
            session.add(bot_msg)
            billing = session.exec(
                select(Billing).where(Billing.user_id == auth_state.user_id)
            ).first()
            if not billing:
                billing = Billing(
                    user_id=auth_state.user_id, current_month_tokens=0, total_tokens=0
                )
                session.add(billing)
            billing.current_month_tokens += tokens_used
            billing.total_tokens += tokens_used
            session.add(billing)
            session.commit()
            session.refresh(bot_msg)
            self.current_month_tokens = billing.current_month_tokens
        self.messages.append(bot_msg)
        self.is_loading = False