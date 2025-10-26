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

# Set API key
export DASHSCOPE_API_KEY="your-api-key"
```

### Usage

```python
from basic.agent import root_agent

# Roll a 6-sided die
response = root_agent.chat("Roll a 6-sided die")
print(response)

# Check prime numbers
response = root_agent.chat("Check if 17, 23, 25 are prime")
print(response)
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

## License

MIT

