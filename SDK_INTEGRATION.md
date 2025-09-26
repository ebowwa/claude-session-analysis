# Claude Code SDK Integration Guide

## Overview

The Claude Code SDK provides programmatic access to Claude Code's capabilities through both OpenAI-style and Anthropic-style APIs. This enables developers to build custom tools and integrations that can interact with Claude Code sessions.

## Available SDK Packages

### Official Packages
- **@anthropic-ai/claude-code** - CLI tool (required dependency)
- **claude-code-sdk** - TypeScript wrapper (third-party, widely used)

### Community Packages
- **@instantlyeasy/claude-code-sdk-ts** - Unofficial TypeScript port
- **@lasercat/claude-code-sdk-ts** - Another TypeScript implementation
- **ai-sdk-provider-claude-code** - AI SDK v5 provider

## Installation

### Basic Setup
```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Install SDK wrapper
npm install claude-code-sdk
```

## API Capabilities

### 1. Session Management
```typescript
import { ClaudeCode } from 'claude-code-sdk'

const claude = new ClaudeCode()

// Create and manage sessions
const session = await claude.sessions.create({
  messages: [
    { role: 'user', content: 'Let us analyze some code' }
  ]
})

// Continue sessions
const response = await session.continue({
  messages: [
    { role: 'user', content: 'Now check for security issues' }
  ]
})
```

### 2. Chat Completions (OpenAI-style)
```typescript
const response = await claude.chat.completions.create({
  model: 'claude-code',
  messages: [
    { role: 'user', content: 'Write a Python script to analyze session data' }
  ],
  max_tokens: 1000,
  temperature: 0.7
})
```

### 3. Messages API (Anthropic-style)
```typescript
const response = await claude.messages.create({
  model: 'claude-code',
  messages: [
    {
      role: 'user',
      content: [{
        type: 'text',
        text: 'Analyze my project structure'
      }]
    }
  ],
  max_tokens: 1000
})
```

### 4. Tool Integration
```typescript
// Register custom tools
await claude.tools.create({
  name: 'session-analyzer',
  description: 'Analyze Claude session data',
  input_schema: {
    type: 'object',
    properties: {
      session_id: { type: 'string' },
      time_range: { type: 'string' }
    },
    required: ['session_id']
  }
})

// Use tools in conversations
const response = await claude.chat.completions.create({
  model: 'claude-code',
  messages: [
    { role: 'user', content: 'Analyze my recent sessions' }
  ],
  tools: [{ name: 'session-analyzer' }]
})
```

### 5. Streaming Support
```typescript
const stream = await claude.chat.completions.createStream({
  model: 'claude-code',
  messages: [
    { role: 'user', content: 'Help me debug this issue' }
  ]
})

for await (const chunk of stream) {
  if (chunk.choices[0].delta.content) {
    process.stdout.write(chunk.choices[0].delta.content)
  }
}
```

## Session Analysis Integration Examples

### Enhanced Session Analyzer
```typescript
import { ClaudeCode } from 'claude-code-sdk'

class EnhancedSessionAnalyzer {
  private claude: ClaudeCode

  constructor() {
    this.claude = new ClaudeCode()
  }

  async analyzeWithAI(sessionData: any) {
    const response = await this.claude.messages.create({
      model: 'claude-code',
      messages: [
        {
          role: 'user',
          content: [{
            type: 'text',
            text: `Analyze this Claude session data and provide insights:
            ${JSON.stringify(sessionData, null, 2)}`
          }]
        }
      ],
      max_tokens: 1000
    })

    return response.content[0].text
  }

  async generateReport(sessions: any[]) {
    const session = await this.claude.sessions.create({
      messages: [
        {
          role: 'user',
          content: `Generate a comprehensive report from these session logs:
          ${JSON.stringify(sessions, null, 2)}`
        }
      ]
    })

    return session
  }
}
```

### Real-time Session Monitoring
```typescript
class SessionMonitor {
  private claude: ClaudeCode

  constructor() {
    this.claude = new ClaudeCode()
  }

  async watchSession() {
    // Start a monitoring session
    const session = await this.claude.sessions.create({
      messages: [
        {
          role: 'system',
          content: 'You are a session monitoring assistant. Track usage patterns and provide insights.'
        },
        {
          role: 'user',
          content: 'Start monitoring Claude Code activity and report on patterns.'
        }
      ]
    })

    // Set up interval to check session file
    setInterval(async () => {
      const sessionData = this.readSessionFile()
      if (sessionData.changed) {
        const insights = await session.continue({
          messages: [
            {
              role: 'user',
              content: `Session updated: ${JSON.stringify(sessionData)}`
            }
          ]
        })
        console.log('Session insights:', insights)
      }
    }, 5000)
  }
}
```

## MCP Integration

The SDK supports Model Context Protocol (MCP) servers:

```typescript
// Configure MCP server
const claude = new ClaudeCode()
claude.setMcpServer('http://localhost:3000/mcp')

// Use MCP-provided tools
const response = await claude.chat.completions.create({
  model: 'claude-code',
  messages: [
    { role: 'user', content: 'Use available MCP tools to analyze my project' }
  ]
})
```

## Advanced Features

### 1. Batch Operations
```typescript
// Process multiple requests
const requests = [
  { content: 'Analyze file A' },
  { content: 'Analyze file B' },
  { content: 'Analyze file C' }
]

const results = await Promise.all(
  requests.map(req =>
    claude.chat.completions.create({
      model: 'claude-code',
      messages: [{ role: 'user', content: req.content }]
    })
  )
)
```

### 2. Custom Tool Development
```typescript
interface SessionAnalysisTool {
  name: 'session-analysis'
  description: 'Analyze Claude session patterns'
  input_schema: {
    type: 'object'
    properties: {
      time_range: { type: 'string' }
      include_todos: { type: 'boolean' }
    }
  }
}

// Register session analysis tool
await claude.tools.create({
  name: 'session-analysis',
  description: 'Analyze Claude session patterns and provide insights',
  input_schema: {
    type: 'object',
    properties: {
      time_range: { type: 'string' },
      include_todos: { type: 'boolean', default: true }
    },
    required: ['time_range']
  }
})
```

## Configuration Options

```typescript
const claude = new ClaudeCode({
  apiKey: process.env.ANTHROPIC_API_KEY,
  cliPath: '/custom/path/to/claude',  // Custom CLI path
  timeout: 120000,  // 2 minute timeout
  debug: true  // Enable debug logging
})
```

## Use Cases for Session Analysis

1. **Automated Reporting**: Generate daily/weekly usage reports
2. **Real-time Monitoring**: Track active sessions and provide insights
3. **Pattern Recognition**: Identify usage patterns and trends
4. **Integration with External Tools**: Connect to dashboards and monitoring systems
5. **Custom Analytics**: Build specialized analysis tools

## Limitations

- Requires Claude Code CLI to be installed
- Limited to session-level data (no conversation content access)
- Dependent on local file system for some data
- API rate limits may apply
- Requires valid Anthropic API key

## Security Considerations

- Store API keys securely (use environment variables)
- Be mindful of data privacy when handling session metadata
- Follow Anthropic's usage guidelines and terms
- Implement proper error handling for API failures

---

*This guide documents the discovered Claude Code SDK capabilities as of September 2025. The SDK ecosystem is rapidly evolving, so check the official documentation for the latest updates.*