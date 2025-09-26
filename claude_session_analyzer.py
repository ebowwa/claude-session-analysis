#!/usr/bin/env python3
"""
Claude Session Analyzer
Analyzes Claude Code session data to track usage patterns and session information.

Author: Claude Code Assistant
Date: September 2025
License: MIT
"""

import json
import datetime
import os
import glob
import sqlite3
from pathlib import Path
import time
import sys

def analyze_session_file(session_file):
    """Analyze a session JSON file and return parsed data."""
    try:
        with open(session_file, 'r') as f:
            data = json.load(f)

        start_time = datetime.datetime.fromtimestamp(data['startTime'] / 1000)
        last_update = datetime.datetime.fromtimestamp(data['lastUpdate'] / 1000)
        duration = last_update - start_time

        return {
            'session_id': data['sessionID'],
            'start_time': start_time,
            'last_update': last_update,
            'duration': duration,
            'file_path': session_file
        }
    except Exception as e:
        print(f"Error reading {session_file}: {e}")
        return None

def find_session_data():
    """Find all session-related files in Claude directories."""
    claude_dir = Path.home() / '.claude'
    session_files = []

    # Look for session files in various locations
    patterns = [
        claude_dir / 'statsig' / 'statsig.session_id.*',
        claude_dir / '**' / '*.json',
    ]

    for pattern in patterns:
        session_files.extend(glob.glob(str(pattern)))

    return session_files

def analyze_recent_activity(days=7):
    """Analyze recent Claude activity."""
    print("=== Claude Session Analysis ===\n")

    session_files = find_session_data()
    current_time = datetime.datetime.now()
    week_ago = current_time - datetime.timedelta(days=days)
    claude_dir = Path.home() / '.claude'

    print(f"Looking for sessions in the last {days} days...\n")

    for file_path in session_files:
        if 'session_id' in file_path:
            session_data = analyze_session_file(file_path)
            if session_data and session_data['start_time'] > week_ago:
                print(f"Session: {session_data['session_id']}")
                print(f"  Start: {session_data['start_time']}")
                print(f"  End: {session_data['last_update']}")
                print(f"  Duration: {session_data['duration']}")
                print(f"  File: {file_path}")
                print()

    # Look for todo activity
    todo_dir = claude_dir / 'todos'
    if todo_dir.exists():
        print("=== Recent Todo Activity ===")
        recent_todos = []

        for todo_file in todo_dir.glob('*.json'):
            mod_time = datetime.datetime.fromtimestamp(todo_file.stat().st_mtime)
            if mod_time > week_ago:
                recent_todos.append((todo_file, mod_time))

        recent_todos.sort(key=lambda x: x[1], reverse=True)

        for todo_file, mod_time in recent_todos[:10]:  # Show last 10
            print(f"{mod_time}: {todo_file.name}")

        print(f"\nFound {len(recent_todos)} todo files modified in the last {days} days")

def monitor_live_session():
    """Monitor the current live session file for changes."""
    session_file = Path.home() / '.claude' / 'statsig' / 'statsig.session_id.2656274335'

    if not session_file.exists():
        print("No active session file found")
        return

    print("=== Live Session Monitor ===")
    print(f"Watching: {session_file}")
    print("Press Ctrl+C to stop\n")

    try:
        last_data = None
        while True:
            current_data = analyze_session_file(session_file)
            if current_data:
                if last_data != current_data:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Session updated:")
                    print(f"  Session ID: {current_data['session_id']}")
                    print(f"  Duration: {current_data['duration']}")
                    print(f"  Last Activity: {current_data['last_update']}")
                    last_data = current_data

            # Check every 5 seconds
            import time
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

def export_session_data(output_file='session_data.json'):
    """Export session data to JSON file."""
    session_files = find_session_data()
    claude_dir = Path.home() / '.claude'

    export_data = {
        'export_time': datetime.datetime.now().isoformat(),
        'sessions': [],
        'todo_activity': []
    }

    # Export session data
    for file_path in session_files:
        if 'session_id' in file_path:
            session_data = analyze_session_file(file_path)
            if session_data:
                export_data['sessions'].append({
                    'session_id': session_data['session_id'],
                    'start_time': session_data['start_time'].isoformat(),
                    'last_update': session_data['last_update'].isoformat(),
                    'duration_seconds': session_data['duration'].total_seconds(),
                    'file_path': session_data['file_path']
                })

    # Export todo activity
    todo_dir = claude_dir / 'todos'
    if todo_dir.exists():
        for todo_file in todo_dir.glob('*.json'):
            mod_time = datetime.datetime.fromtimestamp(todo_file.stat().st_mtime)
            export_data['todo_activity'].append({
                'file_name': todo_file.name,
                'modification_time': mod_time.isoformat(),
                'file_path': str(todo_file)
            })

    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"Session data exported to {output_file}")
    print(f"Found {len(export_data['sessions'])} sessions and {len(export_data['todo_activity'])} todo files")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--monitor":
            monitor_live_session()
        elif sys.argv[1] == "--export":
            output_file = sys.argv[2] if len(sys.argv) > 2 else 'session_data.json'
            export_session_data(output_file)
        elif sys.argv[1] == "--help":
            print("Usage: python3 claude_session_analyzer.py [--monitor] [--export [filename]]")
            print("  --monitor: Monitor live session activity")
            print("  --export [filename]: Export session data to JSON file")
            print("  (default): Analyze recent session activity")
    else:
        analyze_recent_activity()