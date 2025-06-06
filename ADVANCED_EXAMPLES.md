# 💡 Advanced Examples & Customizations

## Table of Contents
1. [Looping Executions](#looping-executions)
2. [Conditional Automation](#conditional-automation)
3. [Multi-Step Workflows](#multi-step-workflows)
4. [Computer Vision Integration](#computer-vision-integration)
5. [Error Handling](#error-handling)
6. [Notifications & Logging](#notifications--logging)

---

## Looping Executions

### Example 1: Send 50 LinkedIn Messages

Add this method to `CursorAutomationAgent` class:

```python
def execute_loop(self, recording_file, iterations, speed=1.0, delay_between=2.0):
    """Execute a recording multiple times"""
    print(f"\n{'='*60}")
    print(f"🔁 LOOP EXECUTION: {iterations} iterations")
    print(f"{'='*60}\n")
    
    confirm = input(f"Execute {iterations} times? Type 'yes': ")
    if confirm.lower() != 'yes':
        print("❌ Cancelled")
        return
    
    success_count = 0
    
    for i in range(iterations):
        print(f"\n--- Iteration {i+1}/{iterations} ---")
        
        try:
            self.execute_recording(recording_file, speed, confirm=False)
            success_count += 1
            print(f"✅ Iteration {i+1} completed")
        except Exception as e:
            print(f"❌ Iteration {i+1} failed: {e}")
            retry = input("Continue with next iteration? (yes/no): ")
            if retry.lower() != 'yes':
                break
        
        if i < iterations - 1:  # Don't wait after last iteration
            print(f"⏳ Waiting {delay_between}s before next iteration...")
            time.sleep(delay_between)
    
    print(f"\n{'='*60}")
    print(f"📊 LOOP COMPLETED")
    print(f"{'='*60}")
    print(f"✅ Successful: {success_count}/{iterations}")
    print(f"❌ Failed: {iterations - success_count}/{iterations}")
    print(f"{'='*60}\n")
```

**Usage:**
```python
agent = CursorAutomationAgent()
recording = "recordings/LinkedIn_Message_20240115_143022.json"
agent.execute_loop(recording, iterations=50, speed=1.5, delay_between=3)
```

---

## Conditional Automation

### Example 2: Only Execute if Button Exists

```python
import cv2
import numpy as np
from PIL import ImageGrab

def find_button_on_screen(template_image_path, threshold=0.8):
    """
    Find a button on screen using template matching
    
    Args:
        template_image_path: Path to button template image
        threshold: Match confidence (0.0-1.0)
    
    Returns:
        (x, y) position if found, None otherwise
    """
    # Capture screen
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
    
    # Load template
    template = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)
    
    # Template matching
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= threshold:
        # Found! Return center position
        h, w = template.shape
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y)
    
    return None

def execute_if_button_exists(agent, recording_file, button_template):
    """Execute only if specific button is visible"""
    print("🔍 Checking if button exists...")
    
    button_pos = find_button_on_screen(button_template)
    
    if button_pos:
        print(f"✅ Button found at {button_pos}")
        print("▶️  Executing task...")
        agent.execute_recording(recording_file, confirm=False)
    else:
        print("❌ Button not found. Skipping execution.")
        print("💡 Make sure the correct window is open.")
```

**Usage:**
```python
# First, save a screenshot of the button you want to detect
# Then use it as a template
agent = CursorAutomationAgent()
execute_if_button_exists(
    agent,
    "recordings/LinkedIn_Message.json",
    "templates/send_button.png"
)
```

---

## Multi-Step Workflows

### Example 3: Complex Job Application Workflow

```python
class WorkflowAutomation:
    def __init__(self, agent):
        self.agent = agent
        self.recordings_dir = agent.recordings_dir
    
    def execute_workflow(self, workflow_name):
        """Execute a multi-step workflow"""
        workflows = {
            'job_application': [
                ('fill_basic_info', 1.0),
                ('upload_resume', 1.5),
                ('fill_experience', 1.0),
                ('answer_questions', 1.2),
                ('submit_application', 1.0)
            ],
            'course_completion': [
                ('watch_video', 0.5),  # Can skip faster
                ('answer_mcq', 1.5),
                ('submit_quiz', 1.0)
            ]
        }
        
        if workflow_name not in workflows:
            print(f"❌ Unknown workflow: {workflow_name}")
            return
        
        steps = workflows[workflow_name]
        
        print(f"\n{'='*60}")
        print(f"🎯 WORKFLOW: {workflow_name}")
        print(f"{'='*60}")
        print(f"Steps: {len(steps)}")
        for i, (step_name, speed) in enumerate(steps, 1):
            print(f"  {i}. {step_name} (speed: {speed}x)")
        print(f"{'='*60}\n")
        
        confirm = input("Execute workflow? Type 'yes': ")
        if confirm.lower() != 'yes':
            return
        
        for i, (step_name, speed) in enumerate(steps, 1):
            print(f"\n--- Step {i}/{len(steps)}: {step_name} ---")
            
            # Find recording file
            recording_file = self.find_recording(step_name)
            
            if not recording_file:
                print(f"❌ Recording not found for: {step_name}")
                skip = input("Skip this step? (yes/no): ")
                if skip.lower() != 'yes':
                    break
                continue
            
            # Execute
            try:
                self.agent.execute_recording(recording_file, speed, confirm=False)
                print(f"✅ Step {i} completed")
            except Exception as e:
                print(f"❌ Step {i} failed: {e}")
                retry = input("Retry? (yes/no): ")
                if retry.lower() == 'yes':
                    self.agent.execute_recording(recording_file, speed, confirm=False)
                else:
                    break
            
            # Pause between steps
            if i < len(steps):
                time.sleep(2)
        
        print(f"\n✅ Workflow '{workflow_name}' completed!\n")
    
    def find_recording(self, task_name):
        """Find recording file by task name"""
        for file in self.recordings_dir.glob("*.json"):
            with open(file, 'r') as f:
                data = json.load(f)
                if task_name.lower() in data.get('task_name', '').lower():
                    return file
        return None
```

**Usage:**
```python
agent = CursorAutomationAgent()
workflow = WorkflowAutomation(agent)

# First, record each step:
# 1. Record: "fill_basic_info"
# 2. Record: "upload_resume"
# etc.

# Then run the full workflow:
workflow.execute_workflow('job_application')
```

---

## Computer Vision Integration

### Example 4: Wait Until Element Appears

```python
def wait_for_element(template_path, timeout=30, check_interval=1):
    """
    Wait until an element appears on screen
    
    Args:
        template_path: Path to template image
        timeout: Maximum wait time in seconds
        check_interval: How often to check (seconds)
    
    Returns:
        True if found, False if timeout
    """
    start_time = time.time()
    
    print(f"⏳ Waiting for element (timeout: {timeout}s)...")
    
    while time.time() - start_time < timeout:
        pos = find_button_on_screen(template_path)
        if pos:
            print(f"✅ Element found at {pos}")
            return True
        
        time.sleep(check_interval)
        print(".", end="", flush=True)
    
    print("\n❌ Timeout: Element not found")
    return False

def smart_execute(agent, recording_file, wait_for_template=None):
    """Execute recording, optionally waiting for an element first"""
    
    if wait_for_template:
        if not wait_for_element(wait_for_template):
            print("❌ Cannot execute: Required element not found")
            return False
    
    agent.execute_recording(recording_file, confirm=False)
    return True
```

**Usage:**
```python
# Wait for "Next" button to appear, then execute
smart_execute(
    agent,
    "recordings/Submit_Form.json",
    wait_for_template="templates/next_button.png"
)
```

---

## Error Handling

### Example 5: Robust Execution with Retry

```python
def execute_with_retry(agent, recording_file, max_retries=3, retry_delay=5):
    """Execute with automatic retry on failure"""
    
    for attempt in range(max_retries):
        try:
            print(f"\n{'='*60}")
            print(f"🔄 Attempt {attempt + 1}/{max_retries}")
            print(f"{'='*60}")
            
            agent.execute_recording(recording_file, confirm=False)
            
            # Verify success (you can add custom verification)
            print("✅ Execution successful!")
            return True
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print(f"❌ All {max_retries} attempts failed")
                return False
    
    return False

def execute_with_fallback(agent, primary_recording, fallback_recording):
    """Try primary method, fall back to alternative if it fails"""
    
    print("▶️  Trying primary method...")
    if execute_with_retry(agent, primary_recording, max_retries=2):
        return True
    
    print("\n⚠️  Primary method failed. Trying fallback...")
    return execute_with_retry(agent, fallback_recording, max_retries=2)
```

---

## Notifications & Logging

### Example 6: Add Sound & Desktop Notifications

```python
import winsound
from datetime import datetime

def play_success_sound():
    """Play success sound"""
    winsound.Beep(1000, 200)  # Frequency, duration
    winsound.Beep(1500, 200)

def play_error_sound():
    """Play error sound"""
    winsound.Beep(500, 300)
    winsound.Beep(400, 300)

class LoggedAgent(CursorAutomationAgent):
    """Agent with detailed logging"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_file = "automation_log.txt"
    
    def log(self, message, level="INFO"):
        """Log message to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(log_entry.strip())
    
    def execute_recording(self, recording_file, *args, **kwargs):
        """Execute with logging and notifications"""
        
        self.log(f"Starting execution: {recording_file.name}")
        
        try:
            super().execute_recording(recording_file, *args, **kwargs)
            self.log("Execution completed successfully", "SUCCESS")
            play_success_sound()
            return True
            
        except Exception as e:
            self.log(f"Execution failed: {e}", "ERROR")
            play_error_sound()
            return False
```

**Usage:**
```python
agent = LoggedAgent()
agent.execute_recording(Path("recordings/task.json"))

# Check log file for detailed history
with open("automation_log.txt", 'r') as f:
    print(f.read())
```

---

## Bonus: Schedule Automation

### Example 7: Run Tasks at Specific Times

```python
import schedule
import threading

def schedule_task(agent, recording_file, time_str):
    """
    Schedule a task to run at specific time
    
    Args:
        agent: CursorAutomationAgent instance
        recording_file: Path to recording
        time_str: Time in "HH:MM" format (e.g., "14:30")
    """
    
    def job():
        print(f"\n⏰ Scheduled task triggered at {time_str}")
        agent.execute_recording(recording_file, confirm=False)
    
    schedule.every().day.at(time_str).do(job)
    print(f"✅ Task scheduled for {time_str} daily")

def run_scheduler():
    """Run the scheduler in background"""
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

# Usage:
agent = CursorAutomationAgent()

# Schedule LinkedIn messages at 9 AM daily
schedule_task(agent, Path("recordings/LinkedIn_Message.json"), "09:00")

# Schedule course quiz at 2 PM daily
schedule_task(agent, Path("recordings/Course_Quiz.json"), "14:00")

# Run scheduler in background thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

print("📅 Scheduler running. Press Ctrl+C to stop.")
```

---

## 🎓 Next Level: Build Your Own Features

### Ideas to Implement:

1. **Mouse Movement Smoothing**: Make movements look more human
2. **Random Delays**: Add randomness to avoid detection
3. **OCR Integration**: Read text from screen
4. **Database Integration**: Store data from automated tasks
5. **Web Scraping**: Extract data during automation
6. **Email Notifications**: Send completion reports
7. **Cloud Sync**: Sync recordings across devices
8. **Mobile Control**: Trigger automation from phone

### Example: Human-like Mouse Movement

```python
import random

def human_like_move(x, y):
    """Move mouse with human-like curve"""
    current_x, current_y = pyautogui.position()
    
    # Calculate control point for bezier curve
    control_x = (current_x + x) / 2 + random.randint(-50, 50)
    control_y = (current_y + y) / 2 + random.randint(-50, 50)
    
    # Move in steps
    steps = 20
    for i in range(steps + 1):
        t = i / steps
        # Quadratic Bezier curve
        new_x = (1-t)**2 * current_x + 2*(1-t)*t * control_x + t**2 * x
        new_y = (1-t)**2 * current_y + 2*(1-t)*t * control_y + t**2 * y
        
        pyautogui.moveTo(int(new_x), int(new_y))
        time.sleep(random.uniform(0.001, 0.003))
```

---

## 📚 Resources for Learning More

- **PyAutoGUI Docs**: https://pyautogui.readthedocs.io/
- **OpenCV Tutorials**: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- **Mouse & Keyboard**: https://github.com/boppreh/keyboard
- **Claude API**: https://docs.anthropic.com/

---

## ⚠️ Important Reminders

1. **Always test on dummy data first**
2. **Use appropriate delays between actions**
3. **Implement error handling for production use**
4. **Respect website Terms of Service**
5. **Don't automate anything illegal or unethical**

Happy coding! 🚀

<!-- Web form filling workflow -->
