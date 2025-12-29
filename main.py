import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

from config import MODEL_NAME


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument("user_prompt", type=str, help="User prompt")

    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")

    args = parser.parse_args()

    if args.user_prompt is None:
        raise RuntimeError("User prompt is required.")

    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]

    # Load API key from environment variable

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError(
            "gemini api key not found in environment variables.")

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    if response is None:
        raise RuntimeError("No response from Gemini API.")

    if response.text is None:
        raise RuntimeError("No text in response from Gemini API.")

    if bool(args.verbose):

        print("User prompt: " + str(messages) + "\n")

        if response.usage_metadata is None:
            raise RuntimeError(
                "No usage metadata in response from Gemini API.")

        print(
            f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

    print("Response:\n")
    print(response.text)


if __name__ == "__main__":
    main()
