import json
import os
import streamlit as st
from agent import solve_problem

st.set_page_config(page_title="STEM Problem-Solving Agent", page_icon="🧠", layout="centered")
st.title("🧠 STEM Problem-Solving AI Agent")
st.caption("Cloud-friendly demo · Python · SymPy · Hugging Face Inference API")
st.info("This demo uses a hosted inference endpoint. You need a Hugging Face access token with inference permissions. Never paste your token into public code or commit it to GitHub.")

with st.sidebar:
    st.header("Configuration")
    token = st.text_input("Hugging Face token", type="password", value=os.getenv("HF_TOKEN", ""))
    model = st.text_input("Model ID", value=os.getenv("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct"))
    st.caption("Availability and rate limits depend on the provider and model.")

question = st.text_area("STEM question", placeholder="Example: Solve x^2 - 5x + 6 = 0 and explain the steps.", height=130)
examples = [
    "Solve x^2 - 5x + 6 = 0 and explain the steps.",
    "Differentiate f(x) = x^3 + 2x^2 - 4x.",
    "A body has mass 2 kg and acceleration 3 m/s^2. Find the net force.",
    "Explain Newton's law of cooling and state its assumptions.",
]
selected = st.selectbox("Or choose an example", ["Choose an example…"] + examples)
if st.button("Solve and verify", type="primary", use_container_width=True):
    q = selected if selected != "Choose an example…" and not question.strip() else question.strip()
    if not q:
        st.warning("Enter a question or choose an example.")
    elif not token.strip():
        st.warning("Enter your Hugging Face access token in the sidebar. You can create/manage tokens at https://huggingface.co/settings/tokens.")
    else:
        with st.spinner("Calling hosted model and checking supported calculations…"):
            result = solve_problem(q, token.strip(), model.strip())
        if result.get("error"):
            st.error(result["error"])
        else:
            st.subheader("Answer")
            st.markdown(result["final_answer"])
            st.subheader("Verification details")
            st.write(result["verification_status"])
            st.json(result["checks"])
            with st.expander("Structured model output"):
                st.code(json.dumps(result["structured"], indent=2, ensure_ascii=False), language="json")
