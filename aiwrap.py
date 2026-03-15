#!/usr/bin/env python3
"""
AIWrap - A unified CLI wrapper for Kimi, Gemini, Codex, and Claude Code.

This tool provides a single interface to interact with multiple AI coding assistants.
Switch between providers using a configuration file without changing your workflow.

Supported providers:
  - kimi:     Kimi Code CLI (https://moonshotai.github.io/kimi-cli/)
  - gemini:   Google Gemini CLI (https://github.com/google-gemini/gemini-cli)
  - codex:    OpenAI Codex CLI (https://github.com/openai/codex)
  - claude:   Anthropic Claude Code (https://docs.anthropic.com/en/docs/claude-code)
"""

import argparse
import os
import subprocess
import sys
import shutil
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

# Try to import tomllib (Python 3.11+) or fall back to tomli
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("Error: tomllib or tomli is required. Install with: pip install tomli")
        sys.exit(1)


class Provider(Enum):
    """Supported AI CLI providers."""
    KIMI = "kimi"
    GEMINI = "gemini"
    CODEX = "codex"
    CLAUDE = "claude"


@dataclass
class ProviderConfig:
    """Configuration for a single provider."""
    enabled: bool = True
    command: str = ""
    model: Optional[str] = None
    yolo_disabled: bool = False
    thinking: bool = False
    checkpointing: bool = True
    approval_mode: str = "auto"
    permission_mode: str = "default"
    extra_args: List[str] = field(default_factory=list)


@dataclass
class AIWrapConfig:
    """Complete AIWrap configuration."""
    default_provider: Provider = Provider.KIMI
    verbose: bool = False
    work_dir: Optional[str] = None
    providers: Dict[Provider, ProviderConfig] = field(default_factory=dict)
    mappings: Dict[str, Dict[str, str]] = field(default_factory=dict)


def find_config_file() -> Optional[Path]:
    """Find the aiwrap.toml configuration file.
    
    Search order:
    1. Current directory
    2. Project root (looking for .git)
    3. ~/.config/aiwrap/
    4. ~/.aiwrap/
    """
    # Check current directory
    local_config = Path.cwd() / "aiwrap.toml"
    if local_config.exists():
        return local_config

    # Check project root (traverse up looking for .git)
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists():
            project_config = parent / "aiwrap.toml"
            if project_config.exists():
                return project_config

    # Check user config directories
    user_configs = [
        Path.home() / ".config" / "aiwrap" / "aiwrap.toml",
        Path.home() / ".aiwrap" / "aiwrap.toml",
    ]
    for config_path in user_configs:
        if config_path.exists():
            return config_path

    return None


def load_config(config_path: Optional[Path] = None) -> AIWrapConfig:
    """Load configuration from TOML file."""
    if config_path is None:
        config_path = find_config_file()

    config = AIWrapConfig()
    
    if config_path is None or not config_path.exists():
        # Return default configuration
        config.providers = {
            Provider.KIMI: ProviderConfig(command="kimi"),
            Provider.GEMINI: ProviderConfig(command="gemini"),
            Provider.CODEX: ProviderConfig(command="codex"),
            Provider.CLAUDE: ProviderConfig(command="claude"),
        }
        return config

    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        sys.exit(1)

    # Parse general section
    general = data.get("general", {})
    default_provider_str = general.get("default_provider", "kimi").lower()
    try:
        config.default_provider = Provider(default_provider_str)
    except ValueError:
        print(f"Error: Unknown provider '{default_provider_str}' in config")
        sys.exit(1)
    
    config.verbose = general.get("verbose", False)
    work_dir = general.get("work_dir")
    config.work_dir = work_dir if work_dir else None

    # Parse providers
    providers_data = data.get("providers", {})
    for provider in Provider:
        provider_data = providers_data.get(provider.value, {})
        config.providers[provider] = ProviderConfig(
            enabled=provider_data.get("enabled", True),
            command=provider_data.get("command", provider.value),
            model=provider_data.get("model") or None,
            yolo_disabled=provider_data.get("yolo_disabled") or False,
            thinking=provider_data.get("thinking") or False,
            checkpointing=provider_data.get("checkpointing") if provider_data.get("checkpointing") is not None else True,
            approval_mode=provider_data.get("approval_mode", "auto"),
            permission_mode=provider_data.get("permission_mode", "default"),
            extra_args=provider_data.get("extra_args", []),
        )

    # Parse mappings
    config.mappings = data.get("mappings", {})

    return config


def check_command_installed(command: str) -> bool:
    """Check if a command is installed and available in PATH."""
    return shutil.which(command) is not None


def build_kimi_command(config: ProviderConfig, prompt: Optional[str] = None, 
                       args: argparse.Namespace = None) -> List[str]:
    """Build command arguments for Kimi CLI."""
    cmd = [config.command]

    # Add model if specified
    if args and args.model:
        cmd.extend(["--model", args.model])
    elif config.model:
        cmd.extend(["--model", config.model])

    # Add work directory
    if args and args.work_dir:
        cmd.extend(["--work-dir", args.work_dir])

    # Add YOLO mode (enabled by default in config, use --no-yolo to disable)
    yolo_enabled = not config.yolo_disabled if not (args and args.no_yolo) else False
    if yolo_enabled:
        cmd.append("--yolo")

    # Add thinking mode
    if config.thinking:
        cmd.append("--thinking")

    # Add extra args
    cmd.extend(config.extra_args)

    # Handle interactive vs non-interactive mode
    if args and args.interactive:
        # Interactive mode: no --prompt flag, just run kimi
        pass
    elif prompt:
        # Non-interactive mode: use --prompt
        cmd.extend(["--prompt", prompt])
        # Also add --print for proper non-interactive mode unless explicitly disabled
        if not args or not args.print:
            cmd.append("--print")

    return cmd


def build_gemini_command(config: ProviderConfig, prompt: Optional[str] = None,
                         args: argparse.Namespace = None) -> List[str]:
    """Build command arguments for Gemini CLI."""
    cmd = [config.command]

    # Add model if specified
    if args and args.model:
        cmd.extend(["--model", args.model])
    elif config.model:
        cmd.extend(["--model", config.model])

    # Add YOLO mode (enabled by default in config, use --no-yolo to disable)
    yolo_enabled = not config.yolo_disabled if not (args and args.no_yolo) else False
    if yolo_enabled:
        cmd.append("--yolo")

    # Add extra args
    cmd.extend(config.extra_args)

    # Gemini accepts an initial prompt as argument for interactive mode
    if prompt:
        cmd.append(prompt)

    return cmd


def build_codex_command(config: ProviderConfig, prompt: Optional[str] = None,
                        args: argparse.Namespace = None) -> List[str]:
    """Build command arguments for Codex CLI."""
    cmd = [config.command]

    # Add model if specified
    if args and args.model:
        cmd.extend(["--model", args.model])
    elif config.model:
        cmd.extend(["--model", config.model])

    # Add YOLO mode (enabled by default in config, use --no-yolo to disable)
    yolo_enabled = not config.yolo_disabled if not (args and args.no_yolo) else False
    if yolo_enabled:
        cmd.append("--full-auto")
    elif config.approval_mode and config.approval_mode != "auto":
        cmd.append(f"--{config.approval_mode}")

    # Add extra args
    cmd.extend(config.extra_args)

    # Add prompt if provided (opens interactive with initial prompt)
    if prompt:
        cmd.append(prompt)

    return cmd


def build_claude_command(config: ProviderConfig, prompt: Optional[str] = None,
                         args: argparse.Namespace = None) -> List[str]:
    """Build command arguments for Claude Code CLI."""
    cmd = [config.command]

    # Claude uses -p for SDK mode (non-interactive), plain for interactive
    # We want interactive mode, so we don't use -p

    # Add extra args
    cmd.extend(config.extra_args)

    # Add prompt if provided
    if prompt:
        cmd.append(prompt)

    return cmd


def build_command(provider: Provider, config: ProviderConfig, 
                  prompt: Optional[str] = None,
                  args: argparse.Namespace = None) -> List[str]:
    """Build the command based on the provider."""
    builders = {
        Provider.KIMI: build_kimi_command,
        Provider.GEMINI: build_gemini_command,
        Provider.CODEX: build_codex_command,
        Provider.CLAUDE: build_claude_command,
    }
    
    builder = builders.get(provider)
    if not builder:
        raise ValueError(f"Unknown provider: {provider}")
    
    return builder(config, prompt, args)


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format.
    
    Examples:
        2.34s -> "2.34s"
        83.45s -> "1m 23s"
        3661s -> "1h 1m"
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        if secs >= 1:
            return f"{minutes}m {int(secs)}s"
        else:
            return f"{minutes}m"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def run_provider(provider: Provider, config: AIWrapConfig, 
                 prompt: Optional[str] = None,
                 args: argparse.Namespace = None) -> int:
    """Run the selected provider CLI."""
    provider_config = config.providers.get(provider)
    if not provider_config:
        print(f"Error: No configuration found for provider '{provider.value}'")
        return 1

    if not provider_config.enabled:
        print(f"Error: Provider '{provider.value}' is disabled in configuration")
        return 1

    if not check_command_installed(provider_config.command):
        print(f"Error: Command '{provider_config.command}' not found.")
        print(f"Please install the {provider.value} CLI first.")
        
        install_hints = {
            Provider.KIMI: "pip install kimi-cli",
            Provider.GEMINI: "npm install -g @google/gemini-cli",
            Provider.CODEX: "npm install -g @openai/codex",
            Provider.CLAUDE: "curl -fsSL https://claude.ai/install.sh | bash",
        }
        
        if provider in install_hints:
            print(f"Install with: {install_hints[provider]}")
        return 1

    cmd = build_command(provider, provider_config, prompt, args)
    
    if config.verbose or (args and args.verbose):
        print(f"Running: {' '.join(cmd)}")

    # Check if timer is disabled
    timer_disabled = args and args.no_timer

    try:
        start_time = time.time()
        result = subprocess.run(cmd, check=False)
        end_time = time.time()
        
        # Display timing if not disabled
        if not timer_disabled:
            elapsed = end_time - start_time
            print(f"\n⏱  Total time: {format_duration(elapsed)}")
        
        return result.returncode
    except KeyboardInterrupt:
        end_time = time.time()
        if not timer_disabled:
            elapsed = end_time - start_time
            print(f"\n\n⏱  Total time: {format_duration(elapsed)}")
        print("\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"Error running command: {e}")
        return 1


def list_providers(config: AIWrapConfig) -> None:
    """List all available providers and their status."""
    print("Available AI Providers:")
    print("-" * 50)
    
    for provider in Provider:
        provider_config = config.providers.get(provider, ProviderConfig())
        
        if not provider_config.enabled:
            status = "⚫ disabled"
        elif check_command_installed(provider_config.command):
            status = "🟢 available"
        else:
            status = "🔴 not installed"
        
        default_marker = " (default)" if provider == config.default_provider else ""
        print(f"  {provider.value:<10} {status}{default_marker}")
        
        if provider_config.model:
            print(f"             model: {provider_config.model}")


def show_config(config: AIWrapConfig, config_path: Optional[Path] = None) -> None:
    """Show current configuration."""
    print("AIWrap Configuration:")
    print("-" * 50)
    
    if config_path:
        print(f"Config file: {config_path}")
    else:
        found_config = find_config_file()
        if found_config:
            print(f"Config file: {found_config}")
        else:
            print("Config file: (using defaults)")
    
    print(f"Default provider: {config.default_provider.value}")
    print(f"Verbose mode: {config.verbose}")
    print()
    
    list_providers(config)


def create_config_template() -> None:
    """Create a sample configuration file in the current directory."""
    config_path = Path.cwd() / "aiwrap.toml"
    
    if config_path.exists():
        response = input(f"Config file already exists at {config_path}. Overwrite? [y/N] ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    template = '''# AIWrap Configuration File
[general]
default_provider = "kimi"
verbose = false

[providers.kimi]
enabled = true
command = "kimi"
yolo_disabled = false

[providers.gemini]
enabled = true
command = "gemini"
yolo_disabled = false

[providers.codex]
enabled = true
command = "codex"
yolo_disabled = false

[providers.claude]
enabled = true
command = "claude"
yolo_disabled = false
'''

    config_path.write_text(template)
    print(f"Created configuration file: {config_path}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="aiwrap",
        description="A unified CLI wrapper for Kimi, Gemini, Codex, and Claude Code.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aiwrap -i                 Start interactive session (REPL mode)
  aiwrap -i -p codex        Start interactive session with Codex
  aiwrap "fix this bug"     Run with prompt (non-interactive mode)
  aiwrap -m gpt-5.3 "task"  Use specific model with prompt
  aiwrap --no-yolo -i       Interactive mode with confirmations
  aiwrap --list             List all providers
  aiwrap --config           Show current configuration

Note: Either --interactive or a PROMPT is required. Running 'aiwrap' alone will fail.
      YOLO mode (auto-approve all actions) is enabled by default.

Configuration:
  AIWrap looks for aiwrap.toml in this order:
    1. Current directory
    2. Project root (where .git is found)
    3. ~/.config/aiwrap/aiwrap.toml
    4. ~/.aiwrap/aiwrap.toml

Provider Documentation:
  - Kimi:   https://moonshotai.github.io/kimi-cli/
  - Gemini: https://github.com/google-gemini/gemini-cli
  - Codex:  https://github.com/openai/codex
  - Claude: https://docs.anthropic.com/en/docs/claude-code
        """
    )

    parser.add_argument(
        "prompt",
        nargs="?",
        help="Initial prompt to send to the AI (starts interactive mode)"
    )

    parser.add_argument(
        "-p", "--provider",
        choices=[p.value for p in Provider],
        help="AI provider to use (overrides default)"
    )

    parser.add_argument(
        "-m", "--model",
        help="Model to use (provider-specific)"
    )

    parser.add_argument(
        "-w", "--work-dir",
        help="Working directory for the session"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode (REPL). Without this, a PROMPT is required."
    )

    parser.add_argument(
        "--no-yolo",
        action="store_true",
        help="Disable YOLO mode (prompt for approvals instead of auto-approving)"
    )

    parser.add_argument(
        "--print",
        action="store_true",
        help="Run in print mode (non-interactive) - Kimi only"
    )

    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all available providers"
    )

    parser.add_argument(
        "-c", "--config",
        action="store_true",
        help="Show current configuration"
    )

    parser.add_argument(
        "--init",
        action="store_true",
        help="Create a sample configuration file in current directory"
    )

    parser.add_argument(
        "--config-file",
        type=Path,
        help="Path to custom configuration file"
    )

    parser.add_argument(
        "--no-timer",
        action="store_true",
        help="Disable timing output"
    )

    args = parser.parse_args()

    # Handle special commands
    if args.init:
        create_config_template()
        return 0

    # Load configuration
    config = load_config(args.config_file)

    if args.list:
        list_providers(config)
        return 0

    if args.config:
        show_config(config, args.config_file)
        return 0

    # Validate: either --interactive or a prompt must be provided
    if not args.interactive and not args.prompt:
        parser.error("Either --interactive/-i or a PROMPT is required. Use -h for help.")

    # Determine provider to use
    provider_str = args.provider or config.default_provider.value
    try:
        provider = Provider(provider_str)
    except ValueError:
        print(f"Error: Unknown provider '{provider_str}'")
        return 1

    # Run the provider
    return run_provider(provider, config, args.prompt, args)


if __name__ == "__main__":
    sys.exit(main())
