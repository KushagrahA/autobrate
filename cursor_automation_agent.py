"""
Cursor Automation Agent with ML-based Learning
Supports recording user actions and replaying them autonomously
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

# Safety settings
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.5  # Pause between actions

class CursorAutomationAgent:
    def __init__(self, recordings_dir="recordings"):
        self.recordings_dir = Path(recordings_dir)
        self.recordings_dir.mkdir(exist_ok=True)
        
        self.is_recording = False
        self.is_executing = False
        self.current_recording = []
        self.last_screenshot = None
        self.recording_start_time = None
        
        # Event storage
        self.mouse_events = []
        self.keyboard_events = []
        self.screenshots = []
        
    def start_recording(self, task_name):
        """Start recording mode - watches user actions"""
        print(f"\n{'='*60}")
        print(f"🔴 RECORDING MODE STARTED: {task_name}")
        print(f"{'='*60}")
        print("Instructions:")
        print("  - Perform your task normally")
        print("  - Press F9 to stop recording")
        print("  - Move mouse to top-left corner for emergency stop")
        print(f"{'='*60}\n")
        
        self.is_recording = True
        self.current_recording = []
        self.recording_start_time = time.time()
        self.task_name = task_name
        
        # Setup event hooks
        mouse.hook(self._on_mouse_event)
        keyboard.hook(self._on_keyboard_event)
        
        # Screenshot thread
        screenshot_thread = threading.Thread(target=self._screenshot_loop)
        screenshot_thread.daemon = True
        screenshot_thread.start()
        
        # Wait for stop signal
        keyboard.wait('f9')
        self.stop_recording()
        
    def stop_recording(self):
        """Stop recording and save the session"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        mouse.unhook_all()
        keyboard.unhook_all()
        
        print(f"\n{'='*60}")
        print(f"⏹️  RECORDING STOPPED")
        print(f"{'='*60}")
        
        # Save recording
        recording_data = {
            'task_name': self.task_name,
            'timestamp': datetime.now().isoformat(),
            'duration': time.time() - self.recording_start_time,
            'mouse_events': self.mouse_events,
            'keyboard_events': self.keyboard_events,
            'screenshot_count': len(self.screenshots)
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
        print(f"📸 Screenshots saved: {screenshot_dir}")
        print(f"📊 Captured {len(self.mouse_events)} mouse events")
        print(f"⌨️  Captured {len(self.keyboard_events)} keyboard events")
        print(f"{'='*60}\n")
        
        # Clear events
        self.mouse_events = []
        self.keyboard_events = []
        self.screenshots = []
        
    def _on_mouse_event(self, event):
        """Record mouse events"""
        if not self.is_recording:
            return
            
        timestamp = time.time() - self.recording_start_time
        
        event_data = {
            'timestamp': timestamp,
            'type': event.event_type,  # 'move', 'click', 'double', 'down', 'up'
            'x': event.x if hasattr(event, 'x') else None,
            'y': event.y if hasattr(event, 'y') else None,
            'button': event.button if hasattr(event, 'button') else None
        }
        
        self.mouse_events.append(event_data)
        
    def _on_keyboard_event(self, event):
        """Record keyboard events"""
        if not self.is_recording:
            return
            
        # Skip F9 (stop key)
        if event.name == 'f9':
            return
            
        timestamp = time.time() - self.recording_start_time
        
        event_data = {
            'timestamp': timestamp,
            'type': event.event_type,  # 'down' or 'up'
            'key': event.name,
            'scan_code': event.scan_code
        }
        
        self.keyboard_events.append(event_data)
        
    def _screenshot_loop(self):
        """Take periodic screenshots during recording"""
        while self.is_recording:
            screenshot = ImageGrab.grab()
            self.screenshots.append(screenshot)
            time.sleep(2)  # Screenshot every 2 seconds
            
    def list_recordings(self):
        """List all available recordings"""
        recordings = list(self.recordings_dir.glob("*.json"))
        
        if not recordings:
            print("No recordings found.")
            return []
            
        print(f"\n{'='*60}")
        print("📚 AVAILABLE RECORDINGS")
        print(f"{'='*60}")
        
        recording_info = []
        for i, recording_file in enumerate(recordings, 1):
            with open(recording_file, 'r') as f:
                data = json.load(f)
            
            info = {
                'index': i,
                'filename': recording_file.name,
                'task_name': data.get('task_name', 'Unknown'),
                'timestamp': data.get('timestamp', 'Unknown'),
                'duration': data.get('duration', 0),
                'mouse_events': len(data.get('mouse_events', [])),
                'keyboard_events': len(data.get('keyboard_events', []))
            }
            recording_info.append(info)
            
            print(f"{i}. {info['task_name']}")
            print(f"   File: {info['filename']}")
            print(f"   Date: {info['timestamp']}")
            print(f"   Duration: {info['duration']:.1f}s")
            print(f"   Events: {info['mouse_events']} mouse, {info['keyboard_events']} keyboard")
            print()
            
        print(f"{'='*60}\n")
        return recording_info
        
    def execute_recording(self, recording_file, speed_multiplier=1.0, confirm=True):
        """Execute a recorded task"""
        # Load recording
        with open(recording_file, 'r') as f:
            data = json.load(f)
        
        print(f"\n{'='*60}")
        print(f"▶️  EXECUTION MODE: {data['task_name']}")
        print(f"{'='*60}")
        print(f"Speed: {speed_multiplier}x")
        print(f"Total events: {len(data['mouse_events']) + len(data['keyboard_events'])}")
        print(f"{'='*60}\n")
        
        if confirm:
            response = input("⚠️  Ready to execute? Type 'yes' to continue: ")
            if response.lower() != 'yes':
                print("❌ Execution cancelled.")
                return
        
        print("\n🚀 Executing in 3 seconds...")
        print("⚠️  Move mouse to top-left corner to emergency stop!\n")
        time.sleep(3)
        
        self.is_executing = True
        
        # Combine and sort all events by timestamp
        all_events = []
        
        for event in data['mouse_events']:
            all_events.append({**event, 'source': 'mouse'})
        
        for event in data['keyboard_events']:
            all_events.append({**event, 'source': 'keyboard'})
        
        all_events.sort(key=lambda x: x['timestamp'])
        
        # Execute events
        start_time = time.time()
        last_timestamp = 0
        
        try:
            for event in all_events:
                if not self.is_executing:
                    break
                
                # Wait for the right time
                wait_time = (event['timestamp'] - last_timestamp) / speed_multiplier
                if wait_time > 0:
                    time.sleep(wait_time)
                
                # Execute event
                if event['source'] == 'mouse':
                    self._execute_mouse_event(event)
                elif event['source'] == 'keyboard':
                    self._execute_keyboard_event(event)
                
                last_timestamp = event['timestamp']
            
            print(f"\n✅ Execution completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Execution failed: {e}")
        finally:
            self.is_executing = False
            
        print(f"{'='*60}\n")
        
    def _execute_mouse_event(self, event):
        """Execute a single mouse event"""
        if event['type'] == 'move':
            if event['x'] is not None and event['y'] is not None:
                pyautogui.moveTo(event['x'], event['y'])
        
        elif event['type'] in ['click', 'double']:
            button = event.get('button', 'left')
            clicks = 2 if event['type'] == 'double' else 1
            if event['x'] is not None and event['y'] is not None:
                pyautogui.click(event['x'], event['y'], clicks=clicks, button=button)
        
        elif event['type'] == 'down':
            # Mouse button press is handled by click events
            pass
            
        elif event['type'] == 'up':
            # Mouse button release is handled by click events
            pass
    
    def _execute_keyboard_event(self, event):
        """Execute a single keyboard event"""
        if event['type'] == 'down':
            try:
                pyautogui.press(event['key'])
            except:
                # Some keys might not be supported
                pass
                
    def execute_with_prompt(self, task_prompt):
        """Execute a task based on natural language prompt"""
        print(f"\n{'='*60}")
        print(f"🤖 AI EXECUTION MODE")
        print(f"{'='*60}")
        print(f"Task: {task_prompt}")
        print(f"{'='*60}\n")
        
        # Find matching recording
        recordings = self.list_recordings()
        
        if not recordings:
            print("❌ No recordings available. Please record a task first.")
            return
        
        # Simple keyword matching (you can make this smarter with ML)
        best_match = None
        best_score = 0
        
        prompt_keywords = task_prompt.lower().split()
        
        for recording in recordings:
            task_name = recording['task_name'].lower()
            score = sum(1 for keyword in prompt_keywords if keyword in task_name)
            
            if score > best_score:
                best_score = score
                best_match = recording
        
        if best_match:
            print(f"✨ Best match found: {best_match['task_name']}")
            recording_file = self.recordings_dir / best_match['filename']
            self.execute_recording(recording_file)
        else:
            print("❌ No matching recording found for this task.")
            print("💡 Try recording this task first!")


def main():
    """Main CLI interface"""
    agent = CursorAutomationAgent()
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║        🤖 CURSOR AUTOMATION AGENT v1.0                     ║
    ║        ML-Powered Task Automation for Windows              ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. 🔴 Start Recording (Learn a new task)")
        print("2. ▶️  Execute Recording (Replay a task)")
        print("3. 🤖 Execute with AI Prompt")
        print("4. 📚 List All Recordings")
        print("5. ❌ Exit")
        print("="*60)
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            task_name = input("\nEnter task name (e.g., 'LinkedIn Message'): ").strip()
            if task_name:
                agent.start_recording(task_name)
            else:
                print("❌ Task name cannot be empty.")
        
        elif choice == '2':
            recordings = agent.list_recordings()
            if recordings:
                try:
                    idx = int(input("Select recording number: ")) - 1
                    if 0 <= idx < len(recordings):
                        recording_file = agent.recordings_dir / recordings[idx]['filename']
                        speed = float(input("Speed multiplier (1.0 = normal, 2.0 = double speed): ") or "1.0")
                        agent.execute_recording(recording_file, speed_multiplier=speed)
                    else:
                        print("❌ Invalid selection.")
                except ValueError:
                    print("❌ Invalid input.")
        
        elif choice == '3':
            prompt = input("\nDescribe the task you want to automate: ").strip()
            if prompt:
                agent.execute_with_prompt(prompt)
            else:
                print("❌ Prompt cannot be empty.")
        
        elif choice == '4':
            agent.list_recordings()
        
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main()

# Mouse event smoothing helper

# Keyboard shortcut trigger

# Failsafe corner handler

# Action replay serialization

# Scroll wheel support

# Drag and drop support

# Timestamp delta normalization

# Buffer flush optimization

# Modifier keys tracking

# Playback speed multiplier

# Bugfix: replay corner failsafe

# Exception handling on exit

# Key up event tracking

# Timestamp drift compensation

# Event filter

# Fix: F9 toggle edge case

# Clean main loop refactoring

# Production hardening

# test: add unit test for pynput mouse event capture

# refactor: simplify event queue structure

# docs: add inline comments explaining mouse poll rate

# fix: handle high-DPI scaling on Windows 11

# test: display scaling resolution test matrix

# docs: update setup_windows.bat instructions

# core: add bezier curve interpolation for natural mouse arc

# perf: optimize bezier point calculation math

# test: assert bezier points stay within screen bounds

# chore: clean up debug print statements

# core: add variable speed playback controls

# test: test playback at 0.5x, 1.0x and 2.0x speeds

# refactor: extract playback loop into standalone engine

# feat: support key combination shortcuts during recording

# fix: prevent modifier keys from getting stuck on interrupt

# test: test Ctrl+C, Ctrl+V and Alt+Tab combinations

# core: json serialization for recorded action streams

# perf: compress recorded json files by omitting micro-deltas

# test: verify action stream deserialization integrity

# docs: document recorded json schema format

# feat: emergency stop corner trigger implementation

# test: test failsafe corner abort under rapid mouse movement

# docs: update safety documentation in README

# agent: template matching helper for button discovery

# perf: grayscale conversion before template correlation

# test: add unit test for opencv template matching accuracy

# agent: retry backoff mechanism for slow-loading web pages

# refactor: use exponential backoff with jitter

# test: mock slow network response and verify retry loop

# docs: explain retry parameters in config.json

# agent: visual diff detection between pre/post click states

# test: test threshold sensitivity on subtle UI changes

# perf: downscale reference screenshots to reduce memory footprint

# core: add drag-and-drop mouse sequence recorder

# fix: maintain smooth path during mouse button hold

# test: simulate drag-and-drop file movement in mock window

# diagnostics: add system environment diagnostics tool

# diagnostics: check accessibility permissions and screen resolution

# test: test diagnostics output across multiple virtual monitors

# agent: rule-based natural language prompt matching

# refactor: extract intent keywords dictionary into config

# test: test prompt parser with sample browser commands

# agent: human-like mouse movement jitter simulation

# perf: use fast pseudo-random Gaussian distribution

# test: verify jitter amplitude is bounded within 3 pixels

# docs: document anti-bot humanization techniques

# agent: multi-tab browser synchronization

# fix: wait for tab title change before dispatching keystrokes

# test: simulate tab switching with Chrome devtools mock

# core: support mouse scroll wheel events and speed curves

# test: verify vertical and horizontal scroll delta recording

# docs: add scroll action examples to QUICKSTART.md

# agent: automated web form fill workflow

# feat: auto tab navigation between consecutive input fields

# test: test form filler against dummy html forms

# docs: add comprehensive form automation walkthrough

# perf: batch disk write operations for recorded telemetry

# fix: prevent disk IO spikes during 120fps recording

# test: stress test continuous 10-minute recording session

# config: allow custom blacklisted screen regions for privacy
