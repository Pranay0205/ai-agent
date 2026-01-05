import sys
from google.genai import types
from call_functions import available_functions, call_function
from config import MODEL_NAME
from prompts import system_prompt


def model_invoker(client, messages, verbose):
    for _ in range(20):
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[
                    available_functions], system_instruction=system_prompt,
            ),
        )
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.function_calls:
            print("Response:")
            print(response.text)
            return

        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)

            if not function_call_result.parts:
                raise RuntimeError("Function response appears to be malformed")

            if not function_call_result.parts[0].function_response:
                raise RuntimeError("Function response appears to be empty")

            function_results.append(function_call_result.parts[0])

            if verbose:
                print(
                    f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_results))

    print("Model unable to generate response")
    sys.exit(1)
