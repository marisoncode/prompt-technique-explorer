# 🧪 Prompt Technique Explorer

**Prompt Technique Explorer** is an interactive Streamlit web application built in Python using the Google Gemini API. It allows users to test and compare three core Large Language Model (LLM) prompting techniques—**Zero-Shot**, **Few-Shot**, and **Chain-of-Thought**—side-by-side on the exact same input text. This app makes it easy to visually understand how prompt engineering structure influences model output quality, output formatting, and reasoning behavior.

---

## 💡 Prompting Techniques Explained

* **Zero-Shot:** Provides a direct instruction with no examples given.
* **Few-Shot:** Gives the model examples first for consistent and structured output (used here for sentiment classification).
* **Chain-of-Thought:** Asks the model to reason step by step before providing the final answer.

---

## 🚀 Live Demo

Check out the live app running on Streamlit Cloud:  
👉 **[Live Demo Placeholder](https://your-app-name.streamlit.app)** *(Replace with your Streamlit Cloud deployment link)*

---

## 🔍 Example Inputs & Outputs

Here is a preview of what to expect when running each technique:

### 1. Zero-Shot
* **Input:** `"Explain why the sky is blue in simple terms."`
* **Output:** A direct, concise paragraph explaining Rayleigh scattering without any prior examples or reasoning steps.

### 2. Few-Shot (Sentiment Classifier)
* **Input:** `"The plot was confusing, but the acting and visuals were fantastic."`
* **Output:** 
  ```text
  Positive
  ```
  *(Returns a clean, predictable classification matching the provided few-shot examples).*

### 3. Chain-of-Thought (Reasoning)
* **Input:** `"If I have 3 apples, eat 1, and then buy a 6-pack of apples, how many do I have?"`
* **Output:** 
  ```text
  1. Start with 3 apples.
  2. Eat 1 apple: 3 - 1 = 2 apples left.
  3. Buy 6 more apples: 2 + 6 = 8 apples.

  Final Answer: You have 8 apples.
  ```

---

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend UI:** Streamlit
* **LLM Engine:** Google Gemini API (`google-genai` SDK)

---

## 💻 Local Setup Instructions

Follow these steps to set up and run the app locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/prompt-technique-explorer.git
   cd prompt-technique-explorer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API Key:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

4. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your web browser.

---

## 🎓 Learning Note

This is a learning project built while studying Generative AI (GenAI) development, prompt engineering, and LLM application design.
