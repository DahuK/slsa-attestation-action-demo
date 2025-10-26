import json
import os
import random
import requests
from typing import Dict, Any, List, Callable


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


class QwenAgent:
    def __init__(self, name: str, description: str, instruction: str, tools: List[Callable]):
        self.name = name
        self.description = description
        self.instruction = instruction
        self.tools = tools
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2text/generate"

    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Generate tools schema for Qwen API"""
        tools_schema = []
        for tool in self.tools:
            # Get function signature and docstring
            import inspect
            sig = inspect.signature(tool)
            doc = tool.__doc__ or ""

            # Parse function name and description
            func_name = tool.__name__
            description = doc.split("Args:")[0].strip() if "Args:" in doc else doc.strip()

            # Build parameters schema
            parameters = {"type": "object", "properties": {}, "required": []}
            for param_name, param in sig.parameters.items():
                if param_name == "self":
                    continue

                param_schema = {"description": f"Parameter {param_name}"}

                # Type mapping
                if param.annotation != inspect.Parameter.empty:
                    if param.annotation == int:
                        param_schema["type"] = "integer"
                    elif param.annotation == List[int]:
                        param_schema["type"] = "array"
                        param_schema["items"] = {"type": "integer"}
                    elif param.annotation == str:
                        param_schema["type"] = "string"
                    else:
                        param_schema["type"] = "string"

                parameters["properties"][param_name] = param_schema
                if param.default == inspect.Parameter.empty:
                    parameters["required"].append(param_name)

            tools_schema.append({
                "type": "function",
                "function": {
                    "name": func_name,
                    "description": description,
                    "parameters": parameters
                }
            })

        return tools_schema

    def chat(self, message: str) -> str:
        """Send message to Qwen API and get response"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Combine instruction with user message
        full_instruction = f"{self.instruction}\n\nUser: {message}"

        data = {
            "model": "qwen-plus",
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": self.description
                    },
                    {
                        "role": "user",
                        "content": full_instruction
                    }
                ]
            },
            "parameters": {
                "tools": self._get_tools_schema()
            }
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()

            result = response.json()
            if "output" in result and "text" in result["output"]:
                return result["output"]["text"]
            else:
                return "I apologize, but I couldn't process your request properly."

        except requests.exceptions.RequestException as e:
            return f"I encountered an error while processing your request: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"


# Create the agent instance
root_agent = QwenAgent(
    name="hello_world_agent",
    description="hello world agent that can roll a dice of 8 sides and check prime numbers.",
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
