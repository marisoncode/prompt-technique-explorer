"""
Prompt Technique Explorer — a tiny UI over your existing GeminiClient.

This file's ONE job: collect input from the browser and display output.
It does NOT know how the API call works internally — that's still
gemini_client.py's job. Same separation-of-concerns pattern as before,
just with a UI file added on top.
"""

import streamlit as st
from gemini_client import GeminiClient

st.set_page_config(page_title="Prompt Technique Explorer", page_icon="🧪")
st.title("🧪 Prompt Technique Explorer")
st.caption("See zero-shot, few-shot, and chain-of-thought side by side, on your own input.")

technique = st.selectbox(
    "Choose a technique",
    ["Zero-shot", "Few-shot (Sentiment Classifier)", "Chain-of-thought (Reasoning)"],
)

user_input = st.text_area(
    "Your input",
    placeholder="e.g. 'The plot was confusing but the acting was great.'",
    height=100,
)

run = st.button("Run", type="primary")

FEW_SHOT_TEMPLATE = """Classify the sentiment as Positive, Negative, or Neutral.

Review: "This movie was a waste of time."
Sentiment: Negative

Review: "Absolutely loved every second of it!"
Sentiment: Positive

Review: "It was okay, nothing special."
Sentiment: Neutral

Review: "{input}"
Sentiment:"""

COT_TEMPLATE = "{input}\n\nThink step by step before giving the final answer."


def build_prompt(technique: str, user_input: str) -> str:
    """Pick the right prompt shape for the selected technique.
    This function is the whole point of the demo — same input text,
    three different prompt structures, three different behaviors."""
    if technique == "Few-shot (Sentiment Classifier)":
        return FEW_SHOT_TEMPLATE.format(input=user_input)
    if technique == "Chain-of-thought (Reasoning)":
        return COT_TEMPLATE.format(input=user_input)
    return user_input  # zero-shot: send exactly what the user typed


if run:
    if not user_input.strip():
        st.warning("Type something first.")
    else:
        prompt = build_prompt(technique, user_input)

        with st.expander("See the actual prompt sent to the model"):
            st.code(prompt)

        with st.spinner("Calling Gemini..."):
            client = GeminiClient()
            result = client.generate(prompt)

        st.subheader("Response")
        st.write(result.text)

        if result.input_tokens is not None:
            st.caption(
                f"Tokens — input: {result.input_tokens}, output: {result.output_tokens}"
            )