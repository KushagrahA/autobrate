# 🚀 Quick Start Guide

## Choose Your Version

### 🔵 Basic Version (No API needed)
**File**: `cursor_automation_agent.py`
- Simple recording and playback
- Keyword-based task matching
- Perfect for getting started
- **No API key required**

### 🟣 Advanced Version (AI-powered)
**File**: `advanced_cursor_agent.py`
- AI understands your recordings
- Smart task matching
- Natural language prompts
- **Requires Claude API key**

---

## 🎯 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Basic Version (Recommended First)
```bash
python cursor_automation_agent.py
```

### 3. Test with Simple Task
1. Choose option `1` (Start Recording)
2. Name it: `Test Task`
3. Open Notepad, type "Hello World", press F9
4. Choose option `2` (Execute Recording)
5. Watch it replay!

---

## 💼 Real-World Example: LinkedIn Referrals

### Step-by-Step:

**1. Recording Phase**
```
python cursor_automation_agent.py
> Select: 1 (Start Recording)
> Task name: LinkedIn Software Engineer Referral
```

**2. Perform Your Task**
- Open LinkedIn
- Go to a connection's profile
- Click "Message"
- Type: "Hi [Name], I saw an opening for Software Engineer at [Company]. Would you be open to referring me? I have 3 years of experience in Python/React. Here's my resume: [link]. Thanks!"
- Click "Send"
- Press F9

**3. Execution Phase**
```
> Select: 2 (Execute Recording)
> Choose: 1 (LinkedIn Software Engineer Referral)
> Speed: 1.0
> Type: yes
```

**4. Repeat for Each Person**
- Position LinkedIn on the next person's profile
- Run the execution
- It will send the exact same message!

**Pro Tip**: Create a spreadsheet with names and modify the message template for each batch.

---

## 📚 Example: Course Completion Bot

### The Scenario
You have a mandatory training with 50 MCQ questions. You know the pattern.

### Solution:

**1. Record One Question**
```
> Task: Course MCQ Pattern
```
- Click the correct answer (say it's always option C)
- Click "Next"
- Press F9

**2. Loop Execution**
For now, manually run it 50 times, OR modify the code to loop:

```python
# In the main() function, add a loop option
for i in range(50):
    agent.execute_recording(recording_file, speed_multiplier=2.0, confirm=False)
    time.sleep(1)  # Pause between questions
```

**Result**: 50 questions answered in 5 minutes instead of 30!

---

## 🔐 Advanced: Adding Claude API

### Get API Key
1. Go to: https://console.anthropic.com/
2. Create an account
3. Generate API key
4. Copy the key

### Set Environment Variable

**Windows (PowerShell)**:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

**Windows (Command Prompt)**:
```cmd
set ANTHROPIC_API_KEY=sk-ant-api03-...
```

**Permanent (System Properties)**:
1. Search "Environment Variables" in Windows
2. Add new system variable
3. Name: `ANTHROPIC_API_KEY`
4. Value: your key

### Run Advanced Version
```bash
python advanced_cursor_agent.py
```

### Benefits
- Just describe: "send linkedin message"
- AI finds the right recording
- Better task matching
- Learns from your descriptions

---

## 🛡️ Safety Checklist

Before executing any task:

- [ ] Test on dummy data first
- [ ] Know the emergency stop (mouse to top-left)
- [ ] Start with 1.0x speed
- [ ] Check what windows are open
- [ ] Make sure you can undo actions
- [ ] Don't use for anything illegal/unethical

---

## 🎨 Customization Ideas

### Add Looping
```python
def execute_loop(self, recording_file, times, speed=1.0):
    for i in range(times):
        print(f"Iteration {i+1}/{times}")
        self.execute_recording(recording_file, speed, confirm=False)
        time.sleep(2)
```

### Add Conditional Logic
```python
# Use computer vision to check if button is present
if self.find_button_on_screen("Submit"):
    self.execute_recording(...)
```

### Add Notifications
```python
import winsound
# After execution
winsound.MessageBeep()
print("✅ Task completed!")
```

---

## 📊 Usage Statistics

After using for a week, you might see:
- **Time saved**: ~10 hours
- **Tasks automated**: 200+
- **Repetitive stress avoided**: Priceless 😄

---

## 🐛 Common Issues

### "Module not found"
```bash
pip install [module_name] --user
```

### "Permission denied"
Run as Administrator:
- Right-click Command Prompt
- "Run as Administrator"
- Navigate to folder
- Run script

### "Recording doesn't work"
- Make sure script has focus
- Check F9 isn't bound elsewhere
- Try F8 as alternative (modify code)

### "Execution clicks wrong place"
- Screen resolution changed?
- Window moved?
- Try re-recording

---

## 🎓 Learning Path

### Week 1: Basics
- ✅ Install and run
- ✅ Record simple task (notepad typing)
- ✅ Execute and verify
- ✅ Test emergency stop

### Week 2: Real Tasks
- ✅ Record LinkedIn message
- ✅ Execute on 5 people
- ✅ Experiment with speed
- ✅ Try course MCQs

### Week 3: Advanced
- ✅ Get Claude API key
- ✅ Use AI-powered version
- ✅ Customize with loops
- ✅ Add your own features

### Week 4: Master
- ✅ Build task library
- ✅ Automate daily workflows
- ✅ Help friends set it up
- ✅ Share your success stories!

---

## 🌟 Success Stories (Your Future)

**Before**: "I spent 3 hours sending referral requests on LinkedIn"  
**After**: "I recorded it once, executed 100 times in 20 minutes"

**Before**: "I click through 200 training questions manually"  
**After**: "My bot does it at 2x speed while I browse Reddit"

**Before**: "I copy-paste data for hours"  
**After**: "I automated it, now I actually do my real work"

---

## 🚀 You're Ready!

Start with the basic version, test on harmless tasks, and gradually build up to your real use cases.

Remember: **With great automation comes great responsibility!** 🕷️

Questions? Check the README.md for detailed docs!

Happy automating! 🎉
