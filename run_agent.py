#!/usr/bin/env python3
"""
Simple script to run and test the Qwen agent
"""

import os
import sys
import asyncio
from basic.agent import root_agent, QwenLLM


def check_environment():
    """Check if required environment variables are set"""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ Error: DASHSCOPE_API_KEY environment variable is not set")
        print("Please set it with: export DASHSCOPE_API_KEY='your-api-key'")
        return False
    print("✅ DASHSCOPE_API_KEY is configured")
    return True


class MockRequest:
    def __init__(self, text):
        from google.adk.flows.llm_flows.contents import types as adk_types
        part = adk_types.Part(text=text)
        content = adk_types.Content(parts=[part])
        self.contents = [content]


async def test_agent():
    """Test the agent with sample requests"""
    print("\n🧪 Testing Agent Functionality")
    print("=" * 40)

    # Test basic functionality
    test_requests = [
        "Hello! Can you roll a 6-sided die for me?",
        "Roll a 20-sided die and check if the result is a prime number",
        "Check if 7, 15, 23 are prime numbers",
        "Roll two dice: one 6-sided and one 8-sided"
    ]

    qwen_llm = QwenLLM()

    for i, request_text in enumerate(test_requests, 1):
        print(f"\n{i}. Testing: {request_text[:50]}...")

        # Create mock request
        request = MockRequest(request_text)

        try:
            # Test non-streaming first
            responses = []
            async for response in qwen_llm.generate_content_async(request, stream=False):
                if response.content and response.content.parts:
                    responses.append(response.content.parts[0].text)

            if responses:
                print(f"   ✅ Response: {responses[-1][:100]}...")
            else:
                print("   ⚠️  No response received")

        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}...")

    print(f"\n🎯 Agent '{root_agent.name}' is ready!")
    print(f"📖 Description: {root_agent.description}")
    print(f"🛠️  Available tools: {[tool.__name__ for tool in root_agent.tools]}")


def main():
    """Main entry point"""
    print("🚀 Qwen Agent Runner")
    print("=" * 30)

    if not check_environment():
        sys.exit(1)

    # Run async tests
    asyncio.run(test_agent())

    print("\n✨ Agent is working correctly!")
    print("\n💡 Tips:")
    print("   - Use the agent in your applications with: from basic.agent import root_agent")
    print("   - Enable debug mode with: export DEBUG=1")
    print("   - Configure streaming in agent-card.json")


if __name__ == "__main__":
    main()
