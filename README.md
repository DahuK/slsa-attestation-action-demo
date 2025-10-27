# SLSA Attestation Action Demo

🚀 A SLSA-compliant AI agent powered by Qwen-Plus with function calling capabilities.

## Features

- 🤖 **Qwen-Plus Integration** - Advanced AI model API integration
- 🎲 **Dice Rolling** - Roll dice with any number of sides
- 🔢 **Prime Checking** - Check if numbers are prime
- 🔒 **SLSA Compliance** - Supply chain security best practices
- 🐳 **Docker Support** - Containerized deployment
- 🔍 **Security Scanning** - Automated vulnerability detection

## Quick Start

### Installation

```bash
# Clone repository
git clone <repository-url>
cd slsa-demo

# Install dependencies
uv sync

# Setup environment (optional)
python setup_env.py

# Set API key
export DASHSCOPE_API_KEY="your-api-key"
```

### Usage

#### Option 1: Use the Test Script (Recommended)

```bash
# Set your API key
export DASHSCOPE_API_KEY="your-api-key-here"

# Run the agent tests
python run_agent.py
```

#### Option 2: Use in Python Code

```python
from basic.agent import root_agent

# Roll a 6-sided die
response = root_agent.chat("Roll a 6-sided die")
print(response)

# Check prime numbers
response = root_agent.chat("Check if 17, 23, 25 are prime")
print(response)
```

#### Option 3: Direct LLM Usage

```python
from basic.agent import QwenLLM
import asyncio

async def test_llm():
    llm = QwenLLM()
    # Use the LLM directly with streaming or non-streaming
    async for response in llm.generate_content_async(request, stream=False):
        print(response.content.parts[0].text)

asyncio.run(test_llm())
```

### Docker

```bash
# Build image
docker build -t qwen-agent .

# Run container
docker run -e DASHSCOPE_API_KEY="your-key" qwen-agent
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `DASHSCOPE_API_KEY` | Qwen API Key | Yes |
| `QWEN_MODEL` | Model name (default: qwen-plus) | No |
| `AGENT_TIMEOUT` | API timeout in seconds | No |

## Tools

### Dice Rolling
- **Function**: `roll_die(sides: int)`
- **Usage**: Roll dice with specified sides

### Prime Checking
- **Function**: `check_prime(nums: List[int])`
- **Usage**: Check which numbers are prime

## Security

- 🔒 **SLSA Level 2+** compliance
- 🛡️ **Trivy** vulnerability scanning
- 🔐 **Non-root** container execution
- 📦 **Minimal dependencies** for security

## Development

```bash
# Install with uv
uv sync

# Run tests
python -m pytest

# Type checking
python -m mypy basic/

# Run agent
python -m basic.agent
```

## API Keys

Get Qwen API key from [DashScope Console](https://dashscope.aliyun.com/).

## Troubleshooting

### Common Issues

1. **400 Bad Request Error**
   - Ensure `DASHSCOPE_API_KEY` is correctly set
   - Check that the API key has proper permissions
   - Verify network connectivity to DashScope API

2. **401 Unauthorized Error**
   - Confirm API key is valid and not expired
   - Check API key format (should not include extra spaces)

3. **Stream Parameter Error**
   - The agent supports both streaming (`stream=True`) and non-streaming (`stream=False`) modes
   - Streaming is enabled by default in the agent configuration
   - If you encounter stream-related errors, check the Google ADK version compatibility

### Debug Mode

Enable debug logging to troubleshoot issues:

```bash
export DEBUG=1
python -c "from basic.agent import root_agent; print('Agent loaded successfully')"
```

### Environment Setup

Use the provided setup script to configure your environment:

```bash
# Setup environment variables and create .env file
python setup_env.py

# This will:
# - Check if DASHSCOPE_API_KEY is set
# - Create a .env file template if it doesn't exist
# - Provide usage instructions
```

## License

MIT

