from __future__ import annotations

import uuid
import streamlit as st

from src.config import settings
from src.service import run_agent

st.set_page_config(page_title=settings.app_title, page_icon="💸", layout="wide")

st.markdown(
    """
    <style>
    .summary-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px 20px;
        margin: 8px 0 14px 0;
    }
    .summary-title {
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #6b7280;
        margin-bottom: 8px;
    }
    .summary-text {
        font-size: 1.05rem;
        line-height: 1.65;
        color: #111827;
        margin: 0;
    }
    .pill-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 8px 0 4px 0;
    }
    .pill {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
        font-size: 0.92rem;
        color: #111827;
    }
    .section-card {
        background: #fafafa;
        border: 1px solid #ececec;
        border-radius: 14px;
        padding: 14px 16px;
        height: 100%;
    }
    .section-card h4 {
        margin: 0 0 10px 0;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"loan-thread-{uuid.uuid4().hex[:8]}"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💸 Loan Advisor Agent Learning Lab")
st.caption(
    "Learn LangChain agents practically: tools, loop, structured output, memory, and middleware in one clean project."
)

with st.sidebar:
    st.subheader("Session")
    st.write(f"**Thread ID:** `{st.session_state.thread_id}`")
    if st.button("Start new learning session"):
        st.session_state.thread_id = f"loan-thread-{uuid.uuid4().hex[:8]}"
        st.session_state.messages = []
        st.rerun()

    st.subheader("Try these prompts")
    st.markdown(
        """
- My salary is 80000
- Existing EMI is 12000
- Can I afford a 20 lakh loan at 9% for 20 years?
- Compare 20 lakh at 9% for 10 years vs 20 years
- What is a safe loan amount for me at 9% for 20 years?
- Give me a sample home loan rate hint
"""
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask a loan question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            payload = run_agent(prompt, st.session_state.thread_id)
            structured = payload["structured"]

        if structured:
            st.markdown(
                f"""
                <div class="summary-card">
                    <div class="summary-title">Agent Summary</div>
                    <p class="summary-text">{structured.summary}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="pill-row">
                    <span class="pill"><strong>Affordability:</strong> {structured.affordability_status}</span>
                    <span class="pill"><strong>Risk:</strong> {structured.risk_level}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.info(f"Recommended action: {structured.recommended_action}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="section-card"><h4>Reasons</h4></div>', unsafe_allow_html=True)
                if structured.reasons:
                    for item in structured.reasons:
                        st.write(f"• {item}")
                else:
                    st.write("• No reasons returned.")

            with col2:
                st.markdown('<div class="section-card"><h4>Follow-up questions</h4></div>', unsafe_allow_html=True)
                if structured.follow_up_questions:
                    for item in structured.follow_up_questions:
                        st.write(f"• {item}")
                else:
                    st.write("• None. The agent had enough information.")

            assistant_text = (
                f"{structured.summary}\n\n"
                f"Affordability: {structured.affordability_status}\n"
                f"Risk: {structured.risk_level}\n"
                f"Recommended action: {structured.recommended_action}\n\n"
                "Reasons:\n"
                + "\n".join(f"- {r}" for r in structured.reasons)
                + "\n\nFollow-up questions:\n"
                + (
                    "\n".join(f"- {q}" for q in structured.follow_up_questions)
                    if structured.follow_up_questions
                    else "- None"
                )
            )
        else:
            raw = payload["raw"]
            assistant_text = raw.get("output", str(raw))
            st.markdown(assistant_text)

    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
