# app.py
import streamlit as st
from checker import build_chain

st.set_page_config(page_title="Compliance Checker", page_icon="⚖️", layout="wide")

st.title("⚖️ Compliance Policy Checker")
st.caption("Ask whether any action complies with your company policy documents.")

st.divider()

if "chain" not in st.session_state:
    with st.spinner("Loading policy documents and embedding model..."):
        st.session_state.chain = build_chain()

scenario = st.text_area(
    "Describe the action or scenario to assess:",
    placeholder="e.g. We want to share employee attendance data with a third party HR tool.",
    height=120
)

if st.button("Check Compliance", type="primary") and scenario:
    with st.spinner("Checking against policy documents..."):
        result = st.session_state.chain.invoke(scenario)

    st.divider()

    if "NON-COMPLIANT" in result:
        st.error("🚫 " + result)
    elif "COMPLIANT" in result and "NON-COMPLIANT" not in result:
        st.success("✅ " + result)
    else:
        st.warning("⚠️ " + result)