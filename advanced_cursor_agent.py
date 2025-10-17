"""
Advanced Cursor Automation Agent with Claude AI Integration
Uses Claude API for intelligent task understanding and matching
"""

import pyautogui
import cv2
import numpy as np
import json
import time
import keyboard
import mouse
from PIL import ImageGrab
import threading
from datetime import datetime
import os
from pathlib import Path
import anthropic
import base64
from io import BytesIO

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

class AdvancedCursorAgent:
    def __init__(self, recordings_dir="recordings", claude_api_key=None):
        self.recordings_dir = Path(recordings_dir)
        self.recordings_dir.mkdir(exist_ok=True)
        
        # Initialize Claude client if API key provided
        self.claude_client = None
        if claude_api_key:
            self.claude_client = anthropic.Anthropic(api_key=claude_api_key)
        
        self.is_recording = False
        self.is_executing = False
        self.recording_start_time = None
        self.mouse_events = []
        self.keyboard_events = []
        self.screenshots = []
        self.task_name = ""
        
    def start_recording_with_context(self, task_name, task_description=""):
        """Enhanced recording with task context"""
        print(f"\n{'='*60}")
        print(f"🔴 SMART RECORDING MODE: {task_name}")
        print(f"{'='*60}")
        if task_description:
            print(f"Description: {task_description}")
            print(f"{'='*60}")
        print("Instructions:")
        print("  - Perform your task naturally")
        print("  - The AI is watching and learning patterns")
        print("  - Press F9 to stop recording")
        print("  - Move mouse to top-left corner for emergency stop")
        print(f"{'='*60}\n")
        
        self.is_recording = True
        self.task_name = task_name
        self.task_description = task_description
        self.recording_start_time = time.time()
        self.mouse_events = []
        self.keyboard_events = []
        self.screenshots = []
        
        # Setup hooks
        mouse.hook(self._on_mouse_event)
        keyboard.hook(self._on_keyboard_event)
        
        # Screenshot thread
        screenshot_thread = threading.Thread(target=self._screenshot_loop)
        screenshot_thread.daemon = True
        screenshot_thread.start()
        
        # Wait for stop
        keyboard.wait('f9')
        self.stop_recording_with_analysis()
        
    def stop_recording_with_analysis(self):
        """Stop recording and analyze with Claude"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        mouse.unhook_all()
        keyboard.unhook_all()
        
        print(f"\n{'='*60}")
        print(f"⏹️  RECORDING STOPPED - Analyzing...")
        print(f"{'='*60}")
        
        # Analyze recording with Claude (if available)
        analysis = self._analyze_recording_with_claude()
        
        # Save recording with analysis
        recording_data = {
            'task_name': self.task_name,
            'task_description': self.task_description,
            'timestamp': datetime.now().isoformat(),
            'duration': time.time() - self.recording_start_time,
            'mouse_events': self.mouse_events,
            'keyboard_events': self.keyboard_events,
            'screenshot_count': len(self.screenshots),
            'ai_analysis': analysis
        }
        
        # Save to file
        filename = f"{self.task_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.recordings_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(recording_data, f, indent=2)
        
        # Save screenshots
        screenshot_dir = self.recordings_dir / f"{filename[:-5]}_screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        for i, screenshot in enumerate(self.screenshots):
            screenshot.save(screenshot_dir / f"screenshot_{i:04d}.png")
        
        print(f"✅ Recording saved: {filepath}")
        print(f"📸 {len(self.screenshots)} screenshots saved")
        print(f"📊 {len(self.mouse_events)} mouse events, {len(self.keyboard_events)} keyboard events")
        
        if analysis:
            print(f"\n🤖 AI Analysis:")
            print(f"   {analysis.get('summary', 'No summary available')}")
            print(f"   Key Actions: {', '.join(analysis.get('key_actions', []))}")
        
        print(f"{'='*60}\n")
        
    def _analyze_recording_with_claude(self):
        """Use Claude to analyze the recording and extract patterns"""
        if not self.claude_client or not self.screenshots:
            return None
        
        try:
            # Take first, middle, and last screenshot for analysis
            sample_screenshots = [
                self.screenshots[0],
                self.screenshots[len(self.screenshots)//2] if len(self.screenshots) > 2 else self.screenshots[0],
                self.screenshots[-1]
            ]
            
            # Convert screenshots to base64
            screenshot_data = []
            for img in sample_screenshots:
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_b64 = base64.b64encode(buffered.getvalue()).decode()
                screenshot_data.append(img_b64)
            
            # Analyze with Claude
            message = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": screenshot_data[0]
                            }
                        },
                        {
                            "type": "text",
                            "text": f"""Analyze this task recording:

Task Name: {self.task_name}
Description: {self.task_description}
Duration: {time.time() - self.recording_start_time:.1f}s
Mouse Events: {len(self.mouse_events)}
Keyboard Events: {len(self.keyboard_events)}

Based on the screenshot and data, provide:
1. A brief summary of what task was performed (1-2 sentences)
2. Key actions identified (list 3-5 main steps)
3. Any patterns or repetitive elements
4. Keywords that would help match this recording to future prompts

Respond in JSON format:
{{
  "summary": "...",
  "key_actions": ["action1", "action2", ...],
  "patterns": ["pattern1", ...],
  "keywords": ["keyword1", "keyword2", ...]
}}"""
                        }
                    ]
                }]
            )
            
            # Parse response
            response_text = message.content[0].text
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                return analysis
            
        except Exception as e:
            print(f"⚠️  AI analysis failed: {e}")
        
        return None
    
    def _on_mouse_event(self, event):
        """Record mouse events"""
        if not self.is_recording:
            return
        
        timestamp = time.time() - self.recording_start_time
        event_data = {
            'timestamp': timestamp,
            'type': event.event_type,
            'x': event.x if hasattr(event, 'x') else None,
            'y': event.y if hasattr(event, 'y') else None,
            'button': event.button if hasattr(event, 'button') else None
        }
        self.mouse_events.append(event_data)
    
    def _on_keyboard_event(self, event):
        """Record keyboard events"""
        if not self.is_recording or event.name == 'f9':
            return
        
        timestamp = time.time() - self.recording_start_time
        event_data = {
            'timestamp': timestamp,
            'type': event.event_type,
            'key': event.name,
            'scan_code': event.scan_code
        }
        self.keyboard_events.append(event_data)
    
    def _screenshot_loop(self):
        """Capture screenshots periodically"""
        while self.is_recording:
            screenshot = ImageGrab.grab()
            self.screenshots.append(screenshot)
            time.sleep(2)
    
    def execute_with_ai_prompt(self, prompt):
        """Use Claude to understand the prompt and find the best recording"""
        print(f"\n{'='*60}")
        print(f"🤖 AI-POWERED EXECUTION")
        print(f"{'='*60}")
        print(f"Your Request: {prompt}")
        print(f"{'='*60}\n")
        
        # Load all recordings
        recordings = list(self.recordings_dir.glob("*.json"))
        
        if not recordings:
            print("❌ No recordings available. Please record a task first.")
            return
        
        print(f"🔍 Analyzing {len(recordings)} recordings...")
        
        # Load recording data
        recording_data = []
        for recording_file in recordings:
            with open(recording_file, 'r') as f:
                data = json.load(f)
                recording_data.append({
                    'file': recording_file,
                    'task_name': data.get('task_name', ''),
                    'description': data.get('task_description', ''),
                    'analysis': data.get('ai_analysis', {}),
                    'keywords': data.get('ai_analysis', {}).get('keywords', [])
                })
        
        # Use Claude to match
        if self.claude_client:
            best_match = self._ai_match_recording(prompt, recording_data)
        else:
            # Fallback to keyword matching
            best_match = self._keyword_match_recording(prompt, recording_data)
        
        if best_match:
            print(f"\n✨ Best Match: {best_match['task_name']}")
            if best_match.get('description'):
                print(f"   Description: {best_match['description']}")
            
            confidence = best_match.get('confidence', 'unknown')
            print(f"   Confidence: {confidence}")
            
            response = input("\n▶️  Execute this task? (yes/no): ")
            if response.lower() == 'yes':
                from cursor_automation_agent import CursorAutomationAgent
                basic_agent = CursorAutomationAgent(self.recordings_dir)
                basic_agent.execute_recording(best_match['file'])
        else:
            print("❌ No suitable recording found for this task.")
            print("💡 Try recording this task first!")
    
    def _ai_match_recording(self, prompt, recording_data):
        """Use Claude to intelligently match prompt to recordings"""
        try:
            # Prepare recording info for Claude
            recordings_info = "\n".join([
                f"{i+1}. {rec['task_name']}"
                f" - {rec['description']}"
                f" - Keywords: {', '.join(rec['keywords'])}"
                for i, rec in enumerate(recording_data)
            ])
            
            message = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{
                    "role": "user",
                    "content": f"""Match this user request to the best recording:

User Request: "{prompt}"

Available Recordings:
{recordings_info}

Analyze the request and select the best matching recording. Consider:
- Keywords and terminology
- Task similarity
- Likely user intent

Respond in JSON:
{{
  "best_match_index": <index 1-{len(recording_data)}>,
  "confidence": "<high/medium/low>",
  "reasoning": "why this is the best match"
}}

If no good match exists, set best_match_index to 0."""
                }]
            )
            
            # Parse response
            response_text = message.content[0].text
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                match_idx = result.get('best_match_index', 0) - 1
                
                if match_idx >= 0 and match_idx < len(recording_data):
                    recording_data[match_idx]['confidence'] = result.get('confidence', 'unknown')
                    recording_data[match_idx]['reasoning'] = result.get('reasoning', '')
                    return recording_data[match_idx]
            
        except Exception as e:
            print(f"⚠️  AI matching failed: {e}")
            print("Falling back to keyword matching...")
        
        return self._keyword_match_recording(prompt, recording_data)
    
    def _keyword_match_recording(self, prompt, recording_data):
        """Fallback keyword-based matching"""
        prompt_words = prompt.lower().split()
        best_score = 0
        best_match = None
        
        for rec in recording_data:
            score = 0
            searchable_text = f"{rec['task_name']} {rec['description']} {' '.join(rec['keywords'])}".lower()
            
            for word in prompt_words:
                if word in searchable_text:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = rec
        
        if best_match:
            best_match['confidence'] = 'medium' if best_score > 2 else 'low'
        
        return best_match


def advanced_main():
    """Advanced CLI with Claude integration"""
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║     🤖 ADVANCED CURSOR AUTOMATION AGENT v2.0               ║
    ║     AI-Powered Task Understanding & Execution              ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Check for Claude API key
    claude_api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not claude_api_key:
        print("⚠️  No Claude API key found.")
        print("   Set ANTHROPIC_API_KEY environment variable for AI features.")
        print("   Basic functionality will still work!\n")
    else:
        print("✅ Claude AI integration enabled!\n")
    
    agent = AdvancedCursorAgent(claude_api_key=claude_api_key)
    
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. 🔴 Smart Recording (with AI analysis)")
        print("2. 🤖 AI-Powered Execution (describe what you want)")
        print("3. ▶️  Manual Execution (choose recording)")
        print("4. 📚 List All Recordings")
        print("5. ❌ Exit")
        print("="*60)
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            task_name = input("\nEnter task name: ").strip()
            task_desc = input("Describe what you'll do (optional): ").strip()
            if task_name:
                agent.start_recording_with_context(task_name, task_desc)
            else:
                print("❌ Task name cannot be empty.")
        
        elif choice == '2':
            prompt = input("\n🤖 What do you want to automate?\n   (e.g., 'send LinkedIn message', 'complete course quiz'): ").strip()
            if prompt:
                agent.execute_with_ai_prompt(prompt)
            else:
                print("❌ Please describe the task.")
        
        elif choice == '3':
            from cursor_automation_agent import CursorAutomationAgent
            basic_agent = CursorAutomationAgent(agent.recordings_dir)
            recordings = basic_agent.list_recordings()
            if recordings:
                try:
                    idx = int(input("Select recording number: ")) - 1
                    if 0 <= idx < len(recordings):
                        speed = float(input("Speed (1.0 = normal): ") or "1.0")
                        recording_file = agent.recordings_dir / recordings[idx]['filename']
                        basic_agent.execute_recording(recording_file, speed_multiplier=speed)
                    else:
                        print("❌ Invalid selection.")
                except ValueError:
                    print("❌ Invalid input.")
        
        elif choice == '4':
            from cursor_automation_agent import CursorAutomationAgent
            basic_agent = CursorAutomationAgent(agent.recordings_dir)
            basic_agent.list_recordings()
        
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    advanced_main()

# Retry on element not found

# Screenshot capture hook

# Visual verification

# Natural jitter

# Prompt intent parser

# Action plan execution

# Click verification check

# Double click handling

# Text input typing simulation

# Clipboard paste fallback

# Window focus assertion

# Auto bring window to front

# Element bounding box caching

# Smooth deceleration near target

# Overshoot correction

# Dynamic sleep calculation

# Headless execution mode

# OCR helper hook
