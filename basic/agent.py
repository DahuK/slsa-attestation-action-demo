import json
import os
import random
import requests
from typing import Dict, Any, List, Callable, AsyncGenerator
from google.adk.agents import Agent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.flows.llm_flows.contents import types as adk_types

# Debug mode
DEBUG = os.getenv("DEBUG", "0") == "1"

def roll_die(sides: int) -> int:
    """Roll a die and return the rolled result.
    Args:
      sides: The integer number of sides the die has.
    Returns:
      An integer of the result of rolling the die.
    """
    result = random.randint(1, sides)
    return result


def check_prime(nums: List[int]) -> str:
    """Check if a given list of numbers are prime.
    Args:
      nums: The list of numbers to check.
    Returns:
      A str indicating which number is prime.
    """
    primes = set()
    for number in nums:
        number = int(number)
        if number <= 1:
            continue
        is_prime = True
        for i in range(2, int(number**0.5) + 1):
            if number % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.add(number)
    return "No prime numbers found." if not primes else f"{', '.join(str(num) for num in primes)} are prime numbers."


# Custom Qwen LLM implementation
class QwenLLM(BaseLlm):
    def __init__(self, model: str = "qwen-plus"):
        super().__init__(model=model)
        # Store API config as private attributes
        object.__setattr__(self, '_api_key', os.getenv("DASHSCOPE_API_KEY", ""))
        object.__setattr__(self, '_api_url', "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")

    @property
    def api_key(self) -> str:
        return object.__getattribute__(self, '_api_key')

    @property
    def api_url(self) -> str:
        return object.__getattribute__(self, '_api_url')

    async def generate_content_async(self, request, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        """Generate content using Qwen API"""
        # Check if API key is configured
        if not self.api_key:
            error_msg = "Error: DASHSCOPE_API_KEY environment variable is not set. Please configure your API key to use this agent."
            if DEBUG:
                print(f"DEBUG: {error_msg}")
            error_part = adk_types.Part(text=error_msg)
            error_content = adk_types.Content(parts=[error_part])
            error_response = LlmResponse(content=error_content)
            yield error_response
            return


        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Extract message from request contents
        if hasattr(request, 'contents') and request.contents:
            # Get the first content's text
            content = request.contents[0]
            if hasattr(content, 'parts') and content.parts:
                # Extract text from the first part
                part = content.parts[0]
                if hasattr(part, 'text') and part.text:
                    message = part.text
                else:
                    message = str(part)
            else:
                message = str(content)
        else:
            message = str(request)

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": stream
        }


        try:
            # Handle streaming vs non-streaming differently
            if stream:
                # For streaming, we need to handle the response as a stream
                response = requests.post(self.api_url, headers=headers, json=data, timeout=30, stream=True)
                response.raise_for_status()

                current_text = ""
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data_str = line[6:]  # Remove 'data: ' prefix
                            if data_str == '[DONE]':
                                break
                            try:
                                chunk = json.loads(data_str)
                                if "choices" in chunk and chunk["choices"] and "delta" in chunk["choices"][0]:
                                    delta = chunk["choices"][0]["delta"]
                                    if "content" in delta and delta["content"]:
                                        current_text += delta["content"]
                                        # Create Content with Part
                                        part = adk_types.Part(text=current_text)
                                        content = adk_types.Content(parts=[part])
                                        llm_response = LlmResponse(content=content)
                                        yield llm_response
                            except json.JSONDecodeError:
                                continue

                # Yield final complete response
                if current_text:
                    part = adk_types.Part(text=current_text)
                    content = adk_types.Content(parts=[part])
                    llm_response = LlmResponse(content=content)
                    yield llm_response
            else:
                # Non-streaming request
                response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
                response.raise_for_status()

                result = response.json()
                # Handle OpenAI-compatible format
                if "choices" in result and result["choices"] and "message" in result["choices"][0]:
                    text = result["choices"][0]["message"]["content"]
                # Handle legacy format as fallback
                elif "output" in result and "text" in result["output"]:
                    text = result["output"]["text"]
                else:
                    text = "I apologize, but I couldn't process your request properly."

                # Non-streaming: yield single complete response
                part = adk_types.Part(text=text)
                content = adk_types.Content(parts=[part])
                llm_response = LlmResponse(content=content)
                yield llm_response

        except requests.exceptions.RequestException as e:
            error_part = adk_types.Part(text=f"I encountered an error while processing your request: {str(e)}")
            error_content = adk_types.Content(parts=[error_part])
            error_response = LlmResponse(content=error_content)
            yield error_response
        except Exception as e:
            error_part = adk_types.Part(text=f"An unexpected error occurred: {str(e)}")
            error_content = adk_types.Content(parts=[error_part])
            error_response = LlmResponse(content=error_content)
            yield error_response


# Create Qwen LLM instance
qwen_llm = QwenLLM(model="qwen-plus")

# Create the agent instance using Google ADK with Qwen backend
root_agent = Agent(
    name="hello_world_agent",
    description="hello world agent that can roll a dice of 8 sides and check prime numbers.",
    model=qwen_llm,  # Use custom Qwen LLM
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
      You can roll dice of different sizes.
      You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
      It is ok to discuss previous dice roles, and comment on the dice rolls.
      When you are asked to roll a die, you must call the roll_die tool with the number of sides. Be sure to pass in an integer. Do not pass in a string.
      You should never roll a die on your own.
      When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
      You should not check prime numbers before calling the tool.
      When you are asked to roll a die and check prime numbers, you should always make the following two function calls:
      1. You should first call the roll_die tool to get a roll. Wait for the function response before calling the check_prime tool.
      2. After you get the function response from roll_die tool, you should call the check_prime tool with the roll_die result.
        2.1 If user asks you to check primes based on previous rolls, make sure you include the previous rolls in the list.
      3. When you respond, you must include the roll_die result from step 1.
      You should always perform the previous 3 steps when asking for a roll and checking prime numbers.
      You should not rely on the previous history on prime results.
    """,
    tools=[roll_die, check_prime],
)
