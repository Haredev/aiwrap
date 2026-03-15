# AIWrap

**One command. Multiple AI providers. Zero friction.**

AIWrap is a unified CLI wrapper that lets you seamlessly switch between **Kimi**, **Gemini**, **Codex**, and **Claude Code** without changing your workflow. Stop memorizing different commands for each AI assistant—use one consistent interface everywhere.

Whether you're experimenting with different models, working across teams with different preferences, or just want a standardized AI coding experience, AIWrap eliminates the friction of context switching between AI providers.

---

## Features

- **🔄 Unified Interface for Multiple AI Providers**  
  Use the same commands and workflow across Kimi, Gemini, Codex, and Claude Code. No need to remember different CLI syntax for each provider.

- **⚡ Easy Provider Switching with `-p` Flag**  
  Switch between AI providers instantly with a simple flag: `aiwrap -p codex` or `aiwrap -p claude`. Override your default provider on-the-fly.

- **⚙️ Configuration File Support (TOML)**  
  Customize defaults, models, and behavior per provider using a simple TOML configuration file. Set it once, use it everywhere.

- **🚀 YOLO Mode for Auto-Approval**  
  Enable automatic approval of file edits and shell commands to stay in flow. Disable with `--no-yolo` when you need more control.

- **💻 Interactive and Non-Interactive Modes**  
  Start an interactive REPL session with `-i` for back-and-forth conversations, or pass a prompt directly for quick one-off tasks.

- **📁 Project-Specific Configurations**  
  Place an `aiwrap.toml` in your project root to use different defaults per project—perfect for teams with varying AI preferences.

---

## Supported Providers

| Provider | Command | Description | Install Command |
|----------|---------|-------------|-----------------|
| **Kimi** | `kimi` | Moonshot AI's coding assistant | `pip install kimi-cli` |
| **Gemini** | `gemini` | Google's Gemini CLI | `npm install -g @google/gemini-cli` |
| **Codex** | `codex` | OpenAI's Codex CLI | `npm install -g @openai/codex` |
| **Claude** | `claude` | Anthropic's Claude Code | `curl -fsSL https://claude.ai/install.sh \| bash` |

---

## Requirements

Before installing AIWrap, ensure you have:

- **Python 3.7+** (check with `python3 --version`)
- **At least one AI provider CLI** installed (see [Installing Provider CLIs](#installing-provider-clis))
- **TOML library** (included in Python 3.11+; for older versions: `pip install tomli`)

---

## Installation

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/yourusername/aiwrap.git
cd aiwrap
```

Or download the `aiwrap` and `aiwrap.py` files directly to a directory of your choice.

### Step 2: Ensure Python 3.7+ is Installed

```bash
python3 --version
```

### Step 3: Install TOML Library (Python < 3.11 only)

```bash
pip install tomli
```

Python 3.11+ users can skip this step as `tomllib` is included in the standard library.

### Step 4: Make the Script Executable (Linux/macOS)

```bash
chmod +x aiwrap
```

### Step 5: Add to PATH (Optional but Recommended)

**Linux/macOS:**
```bash
# Add to ~/.bashrc, ~/.zshrc, or equivalent
export PATH="$PATH:/path/to/aiwrap"
```

**Windows:**
Add the AIWrap directory to your system PATH environment variable.

### Step 6: Verify Installation

```bash
aiwrap --help
```

---

## Quick Start

### 1. Initialize Configuration (Optional)

Create a sample configuration file in your current directory:

```bash
aiwrap --init
```

### 2. Check Available Providers

```bash
aiwrap --list
```

### 3. Start Interactive Session

```bash
aiwrap -i                    # Use default provider
aiwrap -i -p codex           # Use Codex specifically
aiwrap -i -p claude          # Use Claude specifically
```

### 4. Run with a Prompt (Non-Interactive)

```bash
aiwrap "Explain this codebase"
aiwrap -p gemini "Analyze this function"
```

---

## Usage Examples

### Basic Usage

```bash
# Start interactive session with default provider
aiwrap -i

# Run a quick task without entering interactive mode
aiwrap "Refactor this function to use async/await"

# List all configured providers and their status
aiwrap --list

# Show current configuration
aiwrap --config
```

### Working with Specific Directories

```bash
# Run AI in a specific directory
aiwrap -w /path/to/project "Review this code"

# Interactive session in a different directory
aiwrap -i -w /path/to/project

# Combining provider and directory
aiwrap -p codex -w /path/to/project "Implement error handling"
```

### Configuration Examples

```bash
# Create a new configuration file in current directory
aiwrap --init

# Use a custom configuration file
aiwrap --config-file /path/to/custom/config.toml -i

# Show current configuration
aiwrap --config
```

### Common Workflows

**Code Review Workflow:**
```bash
# Quick code review without interactive mode
aiwrap "Review the main.py file for potential bugs"

# Interactive deep-dive into a specific module
aiwrap -i -w ./src "Let's review the authentication module"
```

**Multi-Provider Comparison:**
```bash
# Test the same prompt across different providers
aiwrap -p kimi "Optimize this SQL query"
aiwrap -p codex "Optimize this SQL query"
aiwrap -p claude "Optimize this SQL query"
```

**Safe Mode (No Auto-Approve):**
```bash
# Interactive session with confirmations enabled
aiwrap -i --no-yolo

# Non-interactive with safety checks
aiwrap --no-yolo "Suggest changes to improve performance"
```

**Using Specific Models:**
```bash
# Use a specific model with Kimi
aiwrap -p kimi -m kimi-k2-0711-preview "Explain quantum computing"

# Use a specific model with Codex
aiwrap -p codex -m gpt-5.3-codex "Write a REST API"

# Interactive with specific model
aiwrap -i -p claude -m claude-sonnet-4
```

---

## Configuration

AIWrap uses a TOML configuration file to set defaults and customize provider behavior.

### Configuration File Locations (searched in order):

1. `./aiwrap.toml` (current directory)
2. Project root (where `.git` is found)
3. `~/.config/aiwrap/aiwrap.toml`
4. `~/.aiwrap/aiwrap.toml`

### General Section

```toml
[general]
# Default provider: "kimi", "gemini", "codex", or "claude"
default_provider = "kimi"

# Enable verbose output for debugging
verbose = false

# Default working directory (optional)
# work_dir = "/path/to/project"
```

### Provider Configuration

Each provider has its own configuration section under `[providers.<name>]`:

#### Kimi

```toml
[providers.kimi]
enabled = true              # Enable/disable this provider
command = "kimi"            # Command to run Kimi CLI
model = "kimi-k2-0711-preview"  # Default model (optional)
yolo_disabled = false       # Set to true to disable auto-approve
thinking = false            # Enable thinking mode
extra_args = []             # Additional CLI arguments
```

#### Gemini

```toml
[providers.gemini]
enabled = true
command = "gemini"
model = "gemini-2.5-pro"    # Default model (optional)
yolo_disabled = false
checkpointing = true        # Enable checkpointing for undo support
extra_args = []
```

#### Codex

```toml
[providers.codex]
enabled = true
command = "codex"
model = "gpt-5.3-codex"     # Default model (optional)
yolo_disabled = false
approval_mode = "auto"      # "auto", "suggest", or "full-auto"
extra_args = []
```

#### Claude

```toml
[providers.claude]
enabled = true
command = "claude"
model = "claude-sonnet-4"   # Default model (optional)
yolo_disabled = false
permission_mode = "default" # "default", "acceptEdits", "bypassPermissions"
extra_args = []
```

### Key Mappings

Map unified commands to provider-specific commands:

```toml
[mappings]
quit = { kimi = "/exit", gemini = "/quit", codex = "/exit", claude = "/exit" }
clear = { kimi = "/clear", gemini = "/clear", codex = "/clear", claude = "/clear" }
help = { kimi = "/help", gemini = "/help", codex = "/help", claude = "/help" }
compact = { kimi = "/compact", gemini = "/compress", codex = "/compact", claude = "/compact" }
model = { kimi = "/model", gemini = "/settings", codex = "/model", claude = "/model" }
status = { kimi = "/debug", gemini = "/stats", codex = "/status", claude = "/status" }
```

---

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
  --no-timer            Disable timing output
  -h, --help            Show help message
```

### Interactive Mode Commands

Once inside any provider's interactive session, you can use these common slash commands:

| Command | Kimi | Gemini | Codex | Claude | Description |
|---------|------|--------|-------|--------|-------------|
| Exit | `/exit` | `/quit` | `/exit` | `/exit` | Exit the session |
| Clear | `/clear` | `/clear` | `/clear` | `/clear` | Clear the conversation |
| Help | `/help` | `/help` | `/help` | `/help` | Show help |
| Compact | `/compact` | `/compress` | `/compact` | `/compact` | Compress conversation context |
| Model | `/model` | `/settings` | `/model` | `/model` | Change model/settings |
| Status | `/debug` | `/stats` | `/status` | `/status` | Show session status |

---

## Environment Variables

AIWrap and the underlying provider CLIs use various environment variables:

### AIWrap Variables

| Variable | Description |
|----------|-------------|
| `AIWRAP_CONFIG` | Path to default configuration file |

### Provider API Keys

| Variable | Provider | Description |
|----------|----------|-------------|
| `KIMI_API_KEY` | Kimi | API key for Moonshot AI |
| `GEMINI_API_KEY` | Gemini | API key for Google Gemini |
| `OPENAI_API_KEY` | Codex | API key for OpenAI |
| `ANTHROPIC_API_KEY` | Claude | API key for Anthropic |

### Provider-Specific Variables

| Variable | Provider | Description |
|----------|----------|-------------|
| `OPENCLAW_GATEWAY_URL` | Codex | Custom gateway URL for OpenAI |

### Setting Environment Variables

**Linux/macOS (add to `~/.bashrc`, `~/.zshrc`, etc.):**
```bash
export KIMI_API_KEY="your-api-key-here"
export OPENAI_API_KEY="your-api-key-here"
export ANTHROPIC_API_KEY="your-api-key-here"
export GEMINI_API_KEY="your-api-key-here"
```

**Windows (PowerShell):**
```powershell
$env:KIMI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set KIMI_API_KEY=your-api-key-here
```

---

## YOLO Mode (Auto-Approve)

By default, **YOLO mode is enabled** for all providers, which means:
- File edits are automatically approved
- Shell commands are automatically executed
- No interruptions for confirmations

### Disabling YOLO Mode

For a single interactive session:
```bash
aiwrap -i --no-yolo
```

In configuration file:
```toml
[providers.kimi]
yolo_disabled = true   # Prompt for approvals (YOLO off)
```

### Safety Recommendations

⚠️ **Warning:** YOLO mode can make destructive changes without confirmation. Consider disabling it when:
- Working on production codebases
- Running commands that could modify important files
- Learning a new AI provider's behavior
- Working with sensitive data

---

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

**macOS, Linux, WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Homebrew:**
```bash
brew install --cask claude-code
```

---

## Provider Documentation

- **Kimi**: https://moonshotai.github.io/kimi-cli/
- **Gemini**: https://github.com/google-gemini/gemini-cli
- **Codex**: https://github.com/openai/codex
- **Claude**: https://docs.anthropic.com/en/docs/claude-code

---

## Tips & Best Practices

1. **Project-specific configuration**: Place an `aiwrap.toml` in your project root to use different defaults per project.

2. **Quick switching**: Use `-p` to temporarily override the default provider without changing config.

3. **Check availability**: Run `aiwrap --list` to see which providers are installed and available.

4. **Model aliases**: Configure your preferred models in the config file and switch easily.

5. **YOLO safety**: Be careful with YOLO mode on production codebases. Use `--no-yolo` for critical work.

6. **Timing feedback**: AIWrap displays execution time after each session. Use `--no-timer` to disable.

7. **Configuration hierarchy**: AIWrap searches for config in multiple locations—use this for global defaults and project overrides.

---

## Troubleshooting

### Command not found

Make sure the provider CLI is installed and in your PATH:
```bash
which kimi
which gemini
which codex
which claude
```

If not found, install the missing provider CLI (see [Installing Provider CLIs](#installing-provider-clis)).

### Permission errors

Ensure the `aiwrap` script is executable:
```bash
chmod +x /path/to/aiwrap/aiwrap
```

### Python version issues

Requires Python 3.7+. Check with:
```bash
python3 --version
```

If your system Python is older, consider using [pyenv](https://github.com/pyenv/pyenv) to install a newer version.

### TOML library missing (Python < 3.11)

If you see an error about `tomllib` or `tomli`:
```bash
pip install tomli
```

### API key errors

If you see authentication errors, ensure your API keys are set correctly:
```bash
# Check if environment variables are set
echo $KIMI_API_KEY
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
echo $GEMINI_API_KEY
```

### Configuration file not found

Verify the configuration file exists in one of the expected locations:
```bash
# Search for config files
find . -name "aiwrap.toml" 2>/dev/null
find ~ -name "aiwrap.toml" 2>/dev/null
```

### Provider-specific errors

Each provider may have its own error messages. Check the provider documentation for specific troubleshooting steps.

### Verbose mode

Enable verbose output for debugging:
```bash
aiwrap -v "your prompt"
```

---

## Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues

If you find a bug or have a suggestion:
1. Check if the issue already exists in the issue tracker
2. Create a new issue with a clear description
3. Include steps to reproduce (for bugs)
4. Specify your environment (OS, Python version, AIWrap version)

### Contributing Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages: `git commit -m "Add feature X"`
6. Push to your fork: `git push origin feature/my-feature`
7. Create a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Add comments for complex logic
- Update documentation for new features
- Keep the code compatible with Python 3.7+

### Areas for Contribution

- Additional provider support
- Enhanced configuration options
- Better error handling
- Shell completion scripts
- Documentation improvements
- Test coverage

---

## License

MIT License - Feel free to use and modify as needed.

See [LICENSE](LICENSE) file for full license text.

---

## Acknowledgments

AIWrap is built on top of excellent AI CLI tools from:
- [Moonshot AI](https://moonshot.ai/) (Kimi)
- [Google](https://ai.google.dev/) (Gemini)
- [OpenAI](https://openai.com/) (Codex)
- [Anthropic](https://www.anthropic.com/) (Claude)
