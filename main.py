"""
Entry point. This file stays short on purpose — it just wires together
the pieces (config, client) and does one thing. All the real logic
lives in gemini_client.py, where it can be reused and tested.
"""

from gemini_client import GeminiClient


def main() -> None:
    client = GeminiClient()

    prompt = "Say hello in 5 words"
    result = client.generate(prompt)

    print("RESPONSE:", result.text)

    if result.input_tokens is not None:
        print(f"(tokens used — input: {result.input_tokens}, output: {result.output_tokens})")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError) as e:
        # Catch the errors we raised ourselves (config.py, gemini_client.py)
        # and print something a human can act on, instead of a traceback.
        print(f"Something went wrong: {e}")