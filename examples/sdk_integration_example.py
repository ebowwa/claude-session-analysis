#!/usr/bin/env python3
"""
Example of integrating Claude API with Claude Code session analysis
This demonstrates how to use the Claude API for enhanced session monitoring.

Note: This uses the actual Claude API (@anthropic-ai/sdk) to analyze session data,
not a fictional Claude Code SDK. Claude Code is a terminal tool, not an API service.
"""

import json
import datetime
import asyncio
import os
from pathlib import Path

# Install with: pip install anthropic
import anthropic

class ClaudeAPISessionAnalyzer:
    """
    Enhanced session analyzer using Claude API integration.
    This class demonstrates how to use the actual Claude API to analyze session data.
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        # Initialize Claude API client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.session_file = Path.home() / '.claude' / 'statsig' / 'statsig.session_id.2656274335'

    def read_session_data(self):
        """Read current session data from Claude Code's session file."""
        try:
            if not self.session_file.exists():
                print(f"Session file not found: {self.session_file}")
                return None

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
                'duration_seconds': duration.total_seconds(),
                'file_path': str(self.session_file)
            }
        except Exception as e:
            print(f"Error reading session data: {e}")
            return None

    async def analyze_with_claude_api(self, session_data):
        """
        Use Claude API to analyze session data and provide insights.
        This uses the actual Claude API, not a fictional Claude Code SDK.
        """
        if not session_data:
            return "No session data available"

        try:
            # Create prompt for Claude API
            analysis_prompt = f"""
            Analyze this Claude Code session data and provide insights:

            Session ID: {session_data['session_id']}
            Start Time: {session_data['start_time']}
            Last Update: {session_data['last_update']}
            Duration: {session_data['duration']}
            Duration (seconds): {session_data['duration_seconds']}

            Please provide a comprehensive analysis covering:
            1. Usage patterns and productivity insights
            2. Session duration analysis and optimization
            3. Recommendations for better workflow efficiency
            4. Potential productivity improvements
            5. Time management suggestions based on session length

            Format your response as structured insights with actionable recommendations.
            """

            # Make API call to Claude
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ]
            )

            return {
                'insights': response.content[0].text,
                'model_used': response.model,
                'usage': response.usage,
                'timestamp': datetime.datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error analyzing with Claude API: {e}")
            return {
                'insights': "Unable to analyze session data with Claude API",
                'error': str(e),
                'timestamp': datetime.datetime.now().isoformat()
            }

    async def create_enhanced_report(self):
        """Create an enhanced report using Claude API integration."""
        session_data = self.read_session_data()

        if not session_data:
            return {
                'error': 'No active session found',
                'session_file': str(self.session_file),
                'timestamp': datetime.datetime.now().isoformat()
            }

        # Get AI-powered analysis from Claude API
        analysis = await self.analyze_with_claude_api(session_data)

        # Generate comprehensive report
        report = {
            'session_data': session_data,
            'ai_analysis': analysis,
            'generated_at': datetime.datetime.now().isoformat(),
            'analysis_method': 'claude-api-integration',
            'file_analysis': {
                'session_file_exists': self.session_file.exists(),
                'session_file_size': self.session_file.stat().st_size if self.session_file.exists() else 0,
                'last_modified': datetime.datetime.fromtimestamp(self.session_file.stat().st_mtime).isoformat() if self.session_file.exists() else None
            }
        }

        return report

    async def monitor_session_realtime(self, duration_seconds=60):
        """Monitor session in real-time using Claude API for analysis."""
        print(f"Starting real-time session monitoring for {duration_seconds} seconds...")

        if not self.session_file.exists():
            print(f"Session file not found: {self.session_file}")
            return

        start_time = datetime.datetime.now()
        last_mtime = self.session_file.stat().st_mtime
        analysis_count = 0

        while (datetime.datetime.now() - start_time).total_seconds() < duration_seconds:
            try:
                current_mtime = self.session_file.stat().st_mtime

                if current_mtime > last_mtime:
                    print(f"Session file updated at {datetime.datetime.now()}")

                    # Read new session data
                    session_data = self.read_session_data()
                    if session_data:
                        # Get AI insights about the session
                        print("Analyzing session with Claude API...")
                        analysis = await self.analyze_with_claude_api(session_data)

                        print(f"Session ID: {session_data['session_id']}")
                        print(f"Duration: {session_data['duration']}")
                        print("AI Insights:")
                        print(analysis['insights'])
                        print("-" * 50)

                        analysis_count += 1

                    last_mtime = current_mtime

                await asyncio.sleep(2)  # Check every 2 seconds

            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(5)

        print(f"Real-time monitoring completed. Performed {analysis_count} analyses.")

    def check_claude_api_connection(self):
        """Test connection to Claude API."""
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello, please respond with 'API connection successful'"
                    }
                ]
            )
            print("✅ Claude API connection successful")
            print(f"Model: {response.model}")
            print(f"Response: {response.content[0].text}")
            return True
        except Exception as e:
            print(f"❌ Claude API connection failed: {e}")
            return False

async def main():
    """Main example function."""
    try:
        # Initialize analyzer
        analyzer = ClaudeAPISessionAnalyzer()

        # Test API connection
        print("=== Testing Claude API Connection ===")
        if not analyzer.check_claude_api_connection():
            print("Please check your ANTHROPIC_API_KEY environment variable")
            return

        print("\n" + "="*50 + "\n")

        # Example 1: Basic session analysis
        print("=== Basic Session Analysis ===")
        report = await analyzer.create_enhanced_report()
        print(json.dumps(report, indent=2, default=str))

        print("\n" + "="*50 + "\n")

        # Example 2: Real-time monitoring (run for 30 seconds)
        print("=== Real-time Session Monitoring (30 seconds) ===")
        await analyzer.monitor_session_realtime(duration_seconds=30)

    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set the ANTHROPIC_API_KEY environment variable")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Claude Code Session Analyzer with Claude API Integration")
    print("=" * 60)
    print("This example demonstrates:")
    print("1. Reading Claude Code session data from local files")
    print("2. Using Claude API to analyze session patterns")
    print("3. Real-time monitoring with AI-powered insights")
    print("4. Generating comprehensive usage reports")
    print("=" * 60)

    asyncio.run(main())