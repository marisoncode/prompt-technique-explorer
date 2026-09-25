"""
Prompt Technique Explorer — a tiny UI over your existing GeminiClient.

This file's ONE job: collect input from the browser and display output.
It does NOT know how the API call works internally — that's still
gemini_client.py's job. Same separation-of-concerns pattern as before,
just with a UI file added on top.
"""

import json

import streamlit as st
from gemini_client import GeminiClient

st.set_page_config(page_title="Prompt Technique Explorer", page_icon="🧪")
st.title("🧪 Prompt Technique Explorer")
st.caption("See zero-shot, few-shot, and chain-of-thought side by side, on your own input.")

st.markdown(
    "This tool sends the **same input** to Google's Gemini model using three "
    "different prompting techniques, so you can see how the technique changes "
    "the output — not just the wording, but the *shape* of the answer."
)

TECHNIQUE_INFO = {
    "Zero-shot": "No examples given — a direct answer. **Expect:** a free-form response, length and format vary.",
    "Few-shot (Sentiment Classifier)": "3 example reviews are shown to the model first. **Expect:** a single word — Positive, Negative, or Neutral.",
    "Chain-of-thought (Reasoning)": "The model is asked to reason step by step first. **Expect:** a short explanation followed by a final answer.",
    "System Prompt (Persona)": "A persona/role instruction shapes the model's behavior for the whole answer, separate from your question. **Expect:** the same question, answered in a completely different tone or style depending on the persona.",
    "Structured Output (JSON)": "The model is forced to reply in strict JSON instead of a sentence. **Expect:** a valid JSON object with fixed keys — this is what real code parses, not what a human reads.",
}

technique = st.selectbox(
    "Choose a technique",
    ["Zero-shot", "Few-shot (Sentiment Classifier)", "Chain-of-thought (Reasoning)", "System Prompt (Persona)", "Structured Output (JSON)"],
)
st.info(TECHNIQUE_INFO[technique])

persona = None
if technique == "System Prompt (Persona)":
    persona = st.text_input(
        "System instruction (the model's persona/role)",
        placeholder="e.g. 'You are a sarcastic pirate' or 'You are a strict code reviewer who only replies in bullet points'",
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

JSON_TEMPLATE = """Analyze this text and return ONLY a valid JSON object, no extra words, no markdown formatting, no code fences — just the raw JSON.

Use exactly these keys:
- "summary": a one-sentence summary (string)
- "sentiment": one of "Positive", "Negative", "Neutral"
- "key_topics": an array of 1-3 short topic strings

Text: "{input}"

JSON:"""


def build_prompt(technique: str, user_input: str) -> str:
    """Pick the right prompt shape for the selected technique.
    This function is the whole point of the demo — same input text,
    three different prompt structures, three different behaviors."""
    if technique == "Few-shot (Sentiment Classifier)":
        return FEW_SHOT_TEMPLATE.format(input=user_input)
    if technique == "Chain-of-thought (Reasoning)":
        return COT_TEMPLATE.format(input=user_input)
    if technique == "Structured Output (JSON)":
        return JSON_TEMPLATE.format(input=user_input)
    return user_input  # zero-shot: send exactly what the user typed


if run:
    if not user_input.strip():
        st.warning("Type something first.")
    elif technique == "System Prompt (Persona)" and not persona.strip():
        st.warning("Enter a persona/system instruction first.")
    else:
        prompt = build_prompt(technique, user_input)

        with st.expander("See the actual prompt sent to the model"):
            st.code(prompt)
            if technique == "System Prompt (Persona)":
                st.caption(f"System instruction: {persona}")

        with st.spinner("Calling Gemini..."):
            client = GeminiClient()
            if technique == "System Prompt (Persona)":
                result = client.generate(prompt, system_instruction=persona)
            else:
                result = client.generate(prompt)

        st.subheader("Response")

        if technique == "Structured Output (JSON)":
            raw = result.text.strip()
            # Models sometimes wrap JSON in ```json ... ``` even when told not to —
            # this is a real quirk you'll handle the same way in RAG/agents later.
            if raw.startswith("```"):
                raw = raw.strip("`").removeprefix("json").strip()

            try:
                parsed = json.loads(raw)
                st.json(parsed)
                st.caption("Parsed successfully with json.loads() — this is what your code would use downstream.")
            except json.JSONDecodeError:
                st.error("Model didn't return valid JSON. Raw response shown below:")
                st.code(raw)
        else:
            st.write(result.text)

        if result.input_tokens is not None:
            st.caption(
                f"Tokens — input: {result.input_tokens}, output: {result.output_tokens}"
            )