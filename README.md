# Claude Session Analysis Tools

A comprehensive toolkit for analyzing Claude Code session data, usage patterns, and activity tracking.

## Overview

This project provides tools to analyze Claude Code's session data, which is stored in JSON format rather than traditional databases. The toolkit helps track usage patterns, session durations, and activity over time.

## What We Discovered

### Session Data Structure
- **Location**: `~/.claude/statsig/statsig.session_id.[user_id]`
- **Format**: JSON (not a traditional database as initially expected)
- **Content**: Session ID, start time, last update timestamps
- **Real-time**: Updates every few seconds during active sessions

### Key Findings
- Claude Code tracks current sessions but doesn't store historical conversation content locally
- Session data includes metadata but not actual conversation text
- Multiple sessions per day with peak activity in evening hours
- Todo files serve as additional activity indicators

### Analysis Results (Sept 2025)
- **Current Session**: f23aeeb7-0862-4aca-a464-cb028ddc6b12 (1h 19m active)
- **Yesterday**: 2 distinct sessions with multiple todo files
- **Recent Activity**: 51 todo files modified in last 7 days

## Tools Included

### claude_session_analyzer.py
Main analysis script with the following capabilities:

```bash
# Analyze recent session activity (default: 7 days)
python3 claude_session_analyzer.py

# Monitor live session activity in real-time
python3 claude_session_analyzer.py --monitor

# Show help
python3 claude_session_analyzer.py --help
```

#### Features:
- **Session Analysis**: Parse session timestamps and calculate durations
- **Activity Tracking**: Monitor todo file modifications as activity indicators
- **Real-time Monitoring**: Watch live session updates
- **Historical Analysis**: Track usage patterns over time

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd claude-session-analysis
```

2. Run the analyzer:
```bash
python3 claude_session_analyzer.py
```

## Usage Examples

### Basic Analysis
```bash
python3 claude_session_analyzer.py
```

### Monitor Current Session
```bash
python3 claude_session_analyzer.py --monitor
```

### Custom Time Range
Modify the `days` parameter in the script to analyze different time periods.

## Session Data Format

```json
{
  "sessionID": "f23aeeb7-0862-4aca-a464-cb028ddc6b12",
  "startTime": 1758853587076,
  "lastUpdate": 1758858226250
}
```

**Note**: Timestamps are in milliseconds since epoch.

## Data Privacy

⚠️ **Important Notes**:
- This tool only analyzes metadata, not conversation content
- No actual conversation text is stored or accessed
- Session IDs and timestamps are the only data collected
- Claude Code does not store conversation history locally

## File Locations

- **Session Data**: `~/.claude/statsig/statsig.session_id.*`
- **Todo Files**: `~/.claude/todos/*.json`
- **Settings**: `~/.claude/settings.json`
- **Claude Config**: `~/.claude.json`

## Technical Details

### Session Tracking
- Claude Code maintains a single session file that updates in real-time
- Session IDs are UUID v4 format
- Timestamps are Unix epoch in milliseconds
- No historical session data is preserved locally

### Activity Indicators
- Todo file modifications indicate active usage
- Multiple todo files per session suggest complex multi-agent workflows
- File timestamps provide rough activity timelines

## Limitations

1. **No Conversation Content**: Only metadata is available
2. **Single Session File**: Only current session data exists
3. **No Historical Sessions**: Past session data is not preserved
4. **Real-time Only**: Analysis depends on currently running processes

## Future Enhancements

- [x] Export session data to CSV/JSON
- [ ] Visualize activity patterns
- [ ] Track multiple user sessions
- [ ] Web dashboard for monitoring
- [ ] CLI interface improvements
- [ ] Session duration analytics

## Contributing

This is a research and analysis tool. Contributions welcome for:
- Additional analysis features
- Visualization capabilities
- Export formats
- Documentation improvements

## License

MIT License - feel free to use and modify for your own Claude Code analysis needs.

## Author

Analysis conducted by Claude Code assistant, September 2025.