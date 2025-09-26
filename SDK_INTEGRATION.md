# Claude Code Integration Guide

## Overview

**Important Note**: Claude Code is a terminal-based agentic coding tool, not an API service. This guide explains how to integrate with Claude Code through hooks, automation, and the general Claude API for programmatic access.

## Claude Code vs. Claude API

### Claude Code
- **Terminal-based tool**: `npm install -g @anthropic-ai/claude-code`
- **Agentic coding assistant**: Lives in your terminal, understands codebases
- **Interactive**: Responds to natural language commands in terminal
- **Git integration**: Handles workflows, commit messages, code reviews

### Claude API
- **Programmatic access**: `npm install @anthropic-ai/sdk`
- **General-purpose**: Access Claude models programmatically
- **API endpoints**: RESTful API for messages and completions
- **Application integration**: Build applications powered by Claude

## Installation

### Claude Code (Terminal Tool)
```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Navigate to your project
cd your-project

# Start Claude Code
claude
```

### Claude API (For Programmatic Access)
```bash
# Install Claude API SDK
npm install @anthropic-ai/sdk

# or Python
pip install anthropic
```

## Claude Code Integration Methods

### 1. Git Hooks
Claude Code integrates with Git through hooks and automation:

```bash
# Example: Claude Code can automatically generate commit messages
# This happens automatically when you use Claude Code with git
```

### 2. Terminal Automation
```bash
# Run Claude Code commands programmatically
claude "analyze the performance issues in this codebase"

# Claude Code can be integrated into shell scripts
#!/bin/bash
claude "review this pull request and suggest improvements"
```

### 3. Configuration Files
Claude Code uses configuration files for customization:

```json
// ~/.claude/settings.json
{
  "model": "claude-sonnet-4-20250514",
  "hooks": {
    "pre-commit": "./hooks/validate-commit.js"
  }
}
```

## Claude API Integration (For Session Analysis)

### Basic Claude API Usage
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Analyze session data using Claude API
async function analyzeSessionData(sessionData) {
  const message = await anthropic.messages.create({
    max_tokens: 1024,
    messages: [{
      role: 'user',
      content: `Analyze this Claude Code session data and provide insights:

      Session ID: ${sessionData.session_id}
      Duration: ${sessionData.duration}
      Start Time: ${sessionData.start_time}

      Please provide usage pattern analysis and productivity recommendations.`
    }],
    model: 'claude-sonnet-4-20250514',
  });

  return message.content[0].text;
}
```

### Python Claude API Example
```python
import anthropic
import json
from pathlib import Path

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

class ClaudeAPISessionAnalyzer:
    def __init__(self):
        self.session_file = Path.home() / '.claude' / 'statsig' / 'statsig.session_id.2656274335'

    def read_session_data(self):
        """Read session data from Claude Code's session file"""
        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)

            # Convert timestamps to readable format
            start_time = datetime.datetime.fromtimestamp(data['startTime'] / 1000)
            last_update = datetime.datetime.fromtimestamp(data['lastUpdate'] / 1000)
            duration = last_update - start_time

            return {
                'session_id': data['sessionID'],
                'start_time': start_time,
                'last_update': last_update,
                'duration': duration,
                'duration_seconds': duration.total_seconds()
            }
        except Exception as e:
            print(f"Error reading session data: {e}")
            return None

    async def analyze_with_claude_api(self, session_data):
        """Use Claude API to analyze session data"""
        if not session_data:
            return "No session data available"

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Analyze this Claude Code session data and provide insights:

                    Session ID: {session_data['session_id']}
                    Start Time: {session_data['start_time']}
                    Duration: {session_data['duration']}
                    Duration (seconds): {session_data['duration_seconds']}

                    Provide analysis on:
                    1. Usage patterns and productivity
                    2. Session length optimization
                    3. Recommendations for better workflow
                    """
                }
            ]
        )

        return response.content[0].text
```

## Claude Code Hooks

Claude Code supports hooks for automation and validation:

### Example Hook: Bash Command Validator
```python
#!/usr/bin/env python3
"""Claude Code Hook: Bash Command Validator"""
import json, re, sys

_VALIDATION_RULES = [
    (r"^grep\b(?!.*\|)", "Use 'rg' instead of 'grep'"),
    (r"^find\s+\S+\s+-name\b", "Use 'rg --files | rg pattern'"),
]

def _validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in _VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        sys.exit(0)

    issues = _validate_command(command)
    if issues:
        for message in issues:
            print(f"• {message}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
```

## Session Analysis Integration

### Real-time Session Monitoring
```python
import asyncio
import time
from pathlib import Path

class ClaudeCodeSessionMonitor:
    def __init__(self):
        self.session_file = Path.home() / '.claude' / 'statsig' / 'statsig.session_id.2656274335'
        self.client = anthropic.Anthropic()

    async def monitor_session(self):
        """Monitor Claude Code session in real-time"""
        print("Starting Claude Code session monitoring...")

        last_mtime = 0

        while True:
            try:
                current_mtime = self.session_file.stat().st_mtime

                if current_mtime > last_mtime:
                    print("Session file updated!")

                    # Read new session data
                    session_data = self.read_session_data()
                    if session_data:
                        # Analyze with Claude API
                        analysis = await self.analyze_with_claude_api(session_data)
                        print("Analysis:", analysis)

                    last_mtime = current_mtime

                await asyncio.sleep(5)  # Check every 5 seconds

            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(10)

    def read_session_data(self):
        """Read current session data"""
        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)

            start_time = datetime.datetime.fromtimestamp(data['startTime'] / 1000)
            last_update = datetime.datetime.fromtimestamp(data['lastUpdate'] / 1000)
            duration = last_update - start_time

            return {
                'session_id': data['sessionID'],
                'start_time': start_time,
                'last_update': last_update,
                'duration': duration,
                'duration_seconds': duration.total_seconds()
            }
        except Exception as e:
            print(f"Error reading session data: {e}")
            return None
```

## Configuration

### Claude Code Configuration
```json
// ~/.claude/settings.json
{
  "model": "claude-sonnet-4-20250514",
  "hooks": {
    "pre-commit": "./hooks/validate-commit.js",
    "post-commit": "./hooks/update-stats.js"
  },
  "integrations": {
    "git": true,
    "github": true
  }
}
```

### Environment Variables
```bash
# Required for Claude API
export ANTHROPIC_API_KEY="your-api-key-here"

# Optional: Custom Claude Code settings
export CLAUDE_CODE_MODEL="claude-sonnet-4-20250514"
export CLAUDE_CODE_HOOKS_DIR="./hooks"
```

## Use Cases

### 1. Automated Session Analysis
- Monitor Claude Code usage patterns
- Generate productivity reports
- Track session duration and frequency

### 2. Git Workflow Integration
- Automated commit message generation
- Code review automation
- Pull request analysis

### 3. Development Productivity
- Real-time coding assistance
- Code quality checks
- Performance optimization suggestions

## Limitations

### Claude Code Limitations
- **Terminal-based**: Not designed for API access
- **Interactive**: Requires terminal interaction
- **File-based**: Session data stored in local files
- **No programmatic API**: No direct SDK for Claude Code itself

### Claude API Limitations
- **General-purpose**: Not specifically designed for session analysis
- **No direct session access**: Cannot access Claude Code session data directly
- **Authentication required**: Need API key for access
- **Rate limits**: API usage limits apply

## Best Practices

1. **Use Claude Code for**: Terminal-based coding assistance, Git workflows, interactive code analysis
2. **Use Claude API for**: Programmatic access, custom applications, automated analysis
3. **Combine both**: Use Claude Code for interactive work, Claude API for automation and analysis
4. **Privacy**: Be mindful of data privacy when handling session information

## Official Resources

- **Claude Code**: https://github.com/anthropics/claude-code
- **Claude API Documentation**: https://docs.claude.com/en/api/
- **Claude API SDK (TypeScript)**: https://github.com/anthropics/anthropic-sdk-typescript
- **Claude API SDK (Python)**: https://github.com/anthropics/anthropic-sdk-python
- **Anthropic Documentation**: https://docs.anthropic.com/

---

*This guide documents the actual Claude Code integration patterns as of September 2025. Claude Code is primarily a terminal tool, while the Claude API provides programmatic access to Claude models.*