import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    # print("Hello from bootdev-ai!")
    load_dotenv()
    # print("env loaded")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("API key is missing or empty!")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    # messages=[
    #         {
    #             "role": "user",
    #             "content": args.user_prompt,
    #         }
    #     ]
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        if response.usage == None:
            raise RuntimeError("Failed API request")
        message = response.choices[0].message
        messages.append(message)
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call)
                if not result_message["content"]:
                    raise RuntimeError("Tool return empty value")
                print(f"-> {result_message['content']}")
                messages.append(result_message)
                
                # function_args = json.loads(tool_call.function.arguments or "{}")
                # print(f"Calling function: {tool_call.function.name}({function_args})")
        else:
            # return
            print("Response:")
            print(message.content)
        
        # if response.choices[0].message.content:
        if response.choices[0].finish_reason == "stop":
            break
        
    if response.choices[0].message.content:
        print("Final Response: ")
        print(response.choices[0].message.content)
    else:
        print("No final response produced")
        sys.exit(1)


if __name__ == "__main__":
    main()
