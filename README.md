# AIWrap

A unified CLI wrapper for **Kimi**, **Gemini**, **Codex**, and **Claude Code** AI coding assistants.

AIWrap provides a single interface to interact with multiple AI CLI tools, allowing you to switch between providers seamlessly using a simple configuration file.

## Supported Providers

| Provider | Command | Description |
|----------|---------|-------------|
| **Kimi** | `kimi` | Moonshot AI's coding assistant |
| **Gemini** | `gemini` | Google's Gemini CLI |
| **Codex** | `codex` | OpenAI's Codex CLI |
| **Claude** | `claude` | Anthropic's Claude Code |

## Installation

1. Clone or download this repository
2. Ensure Python 3.7+ is installed
3. Install `tomli` if using Python < 3.11:
   ```bash
   pip install tomli
   ```
4. Add to your PATH (optional):
   ```bash
   # Add to ~/.bashrc, ~/.zshrc, or equivalent
   export PATH="$PATH:/path/to/aiwrap"
   ```

## Quick Start

1. **Initialize configuration** (optional):
   ```bash
   aiwrap --init
   ```

2. **Start interactive session** (requires `-i` flag):
   ```bash
   aiwrap -i
   ```

3. **Use a specific provider interactively**:
   ```bash
   aiwrap -i -p codex
   aiwrap -i -p claude
   aiwrap -i -p gemini
   aiwrap -i -p kimi
   ```

4. **Run with a prompt** (non-interactive mode, no `-i` needed):
   ```bash
   aiwrap "Explain this codebase"
   aiwrap -p codex "Fix this bug"
   ```

## Configuration

AIWrap uses a TOML configuration file to set defaults and customize provider behavior.

### Configuration File Locations (searched in order):

1. `./aiwrap.toml` (current directory)
2. Project root (where `.git` is found)
3. `~/.config/aiwrap/aiwrap.toml`
4. `~/.aiwrap/aiwrap.toml`

### Example Configuration

```toml
[general]
# Default provider: "kimi", "gemini", "codex", or "claude"
default_provider = "kimi"
verbose = false

[providers.kimi]
enabled = true
command = "kimi"
model = "kimi-k2-0711-preview"  # or omit for default
yolo_disabled = false  # Set to true to disable auto-approve and prompt for confirmations
thinking = false
extra_args = []

[providers.gemini]
enabled = true
command = "gemini"
yolo_disabled = false  # Set to true to disable auto-approve and prompt for confirmations
checkpointing = true

[providers.codex]
enabled = true
command = "codex"
model = "gpt-5.3-codex"
yolo_disabled = false  # Set to true to disable auto-approve and prompt for confirmations
approval_mode = "auto"  # Ignored when yolo_disabled = false

[providers.claude]
enabled = true
command = "claude"
model = "claude-sonnet-4"
yolo_disabled = false  # Set to true to disable auto-approve and prompt for confirmations
permission_mode = "default"  # Ignored when yolo_disabled = false
```

## CLI Reference

### Global Options

```
aiwrap [OPTIONS] [PROMPT]

Arguments:
  PROMPT                Initial prompt to send to the AI

Options:
  -p, --provider        Select provider: kimi, gemini, codex, claude
  -m, --model           Specify model (provider-specific)
  -w, --work-dir        Set working directory
  -v, --verbose         Enable verbose output
  --no-yolo             Disable YOLO mode (prompt for approvals)
  --print               Run in non-interactive mode (Kimi)
  -l, --list            List all providers and their status
  -c, --config          Show current configuration
  --init                Create a sample config file
  --config-file PATH    Use custom config file
  -h, --help            Show help message
```

### Examples

```bash
# List available providers
aiwrap --list

# Show configuration
aiwrap --config

# Interactive mode with Codex
aiwrap -i -p codex

# Interactive mode with specific model
aiwrap -i -p codex -m gpt-5.3-codex

# Non-interactive: Run with a prompt
aiwrap "Explain this codebase"
aiwrap -p claude "Review this code"

# Use Gemini in specific directory (non-interactive with prompt)
aiwrap -p gemini -w /path/to/project "Analyze this code"

# Create config template
aiwrap --init
```

## Installing Provider CLIs

### Kimi CLI
```bash
pip install kimi-cli
```

### Gemini CLI
```bash
npm install -g @google/gemini-cli
```

### Codex CLI
```bash
npm install -g @openai/codex
```

### Claude Code
```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Homebrew
brew install --cask claude-code
```

## Provider Documentation

- **Kimi**: https://moonshotai.github.io/kimi-cli/
- **Gemini**: https://github.com/google-gemini/gemini-cli
- **Codex**: https://github.com/openai/codex
- **Claude**: https://docs.anthropic.com/en/docs/claude-code

## Interactive Mode Commands

Once inside any provider's interactive session, you can use these common slash commands:

| Command | Kimi | Gemini | Codex | Claude |
|---------|------|--------|-------|--------|
| Exit | `/exit` | `/quit` | `/exit` | `/exit` |
| Clear | `/clear` | `/clear` | `/clear` | `/clear` |
| Help | `/help` | `/help` | `/help` | `/help` |
| Compact | `/compact` | `/compress` | `/compact` | `/compact` |
| Model | `/model` | `/settings` | `/model` | `/model` |
| Status | `/debug` | `/stats` | `/status` | `/status` |

## YOLO Mode (Auto-Approve)

By default, **YOLO mode is enabled** for all providers, which means:
- File edits are automatically approved
- Shell commands are automatically executed
- No interruptions for confirmations

To disable YOLO mode for a single interactive session:
```bash
aiwrap -i --no-yolo
```

YOLO mode is controlled by `yolo_disabled` setting:
```toml
[providers.kimi]
yolo_disabled = true   # Prompt for approvals (YOLO off)
yolo_disabled = false  # Auto-approve all actions (YOLO on, default)
```

## Tips

1. **Project-specific configuration**: Place an `aiwrap.toml` in your project root to use different defaults per project.

2. **Quick switching**: Use `-p` to temporarily override the default provider without changing config.

3. **Check availability**: Run `aiwrap --list` to see which providers are installed and available.

4. **Model aliases**: Configure your preferred models in the config file and switch easily.

5. **YOLO safety**: Be careful with YOLO mode on production codebases. Use `--no-yolo` for critical work.

## Troubleshooting

### Command not found
Make sure the provider CLI is installed and in your PATH:
```bash
which kimi
which gemini
which codex
which claude
```

### Permission errors
Ensure the `aiwrap` script is executable:
```bash
chmod +x /path/to/aiwrap/aiwrap
```

### Python version
Requires Python 3.7+. Check with:
```bash
python3 --version
```

## License

MIT License - Feel free to use and modify as needed.
