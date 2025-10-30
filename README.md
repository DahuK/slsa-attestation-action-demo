# SLSA Attestation Action Demo

🚀 A SLSA-compliant AI agent powered by Qwen-Plus.

## Features

- 🔒 **SLSA Compliance** - Supply chain security best practices
- 🐳 **Kagent BYO agent** - Kagent BYO Agent
- 🤖 **Qwen-Plus Integration** - Advanced AI model API integration
- 🔍 **Security Scanning** - Automated vulnerability detection

## Quick Start

🚀 [quickstart doc](doc/quickstart.md) 

## Tools

### Dice Rolling
- **Function**: `roll_die(sides: int)`
- **Usage**: Roll dice with specified sides

### Prime Checking
- **Function**: `check_prime(nums: List[int])`
- **Usage**: Check which numbers are prime

## Security
- 🔒 **SLSA Level 3** compliance
- 🛡️ **Trivy** vulnerability scanning

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

