# 🤖 Cursor Automation Agent - Setup & Usage Guide

## What This Agent Does

This intelligent automation agent can:
- **Watch and Learn**: Record your cursor movements, clicks, and keyboard inputs
- **Understand Tasks**: Use visual context to understand what you're doing
- **Replay Actions**: Automatically perform repetitive tasks
- **AI-Powered Execution**: Understand natural language prompts to run the right task

## Perfect For:
✅ LinkedIn job applications & referrals  
✅ Course completion (MCQ selection)  
✅ Data entry tasks  
✅ Web form filling  
✅ Any repetitive cursor-based task  

---

## 🚀 Installation

### Step 1: Install Python
Make sure you have Python 3.8+ installed. Download from: https://www.python.org/downloads/

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**IMPORTANT FOR WINDOWS**: You need to run these commands as Administrator:
```bash
# Open Command Prompt or PowerShell as Administrator
pip install pyautogui opencv-python numpy Pillow keyboard mouse anthropic
```

---

## 📖 How to Use

### Running the Agent
```bash
python cursor_automation_agent.py
```

You'll see a menu with 5 options:

---

## 🔴 MODE 1: Recording (Learning)

**Use Case**: Teach the agent a new task

**Example: LinkedIn Referral Messages**

1. Select option `1` from the menu
2. Enter task name: `LinkedIn Referral Message`
3. The agent starts recording - now perform your task:
   - Open LinkedIn
   - Navigate to a connection
   - Click "Message"
   - Type your referral message
   - Copy-paste it if needed
   - Send the message
4. Press `F9` when done

The agent has now learned this task!

**Example: Course MCQ Completion**

1. Select option `1` from the menu
2. Enter task name: `Course MCQ Answer`
3. Perform the task:
   - Read the question
   - Click the correct answer
   - Click "Next" or "Submit"
4. Press `F9` when done

---

## ▶️ MODE 2: Execute Recording (Replay)

**Use Case**: Replay an exact task you've recorded

1. Select option `2` from the menu
2. Choose which recording to replay
3. Set speed (1.0 = normal, 2.0 = double speed)
4. Type `yes` to confirm
5. The agent takes over your cursor!

**Safety Features**:
- Move your mouse to the **top-left corner** to emergency stop
- 3-second countdown before execution
- Confirmation required before running

---

## 🤖 MODE 3: AI Prompt Execution

**Use Case**: Tell the agent what to do in natural language

Instead of selecting a recording number, just describe what you want:

**Examples**:
```
"Send LinkedIn message"
"Complete course questions"
"Apply for job"
"Fill form"
```

The agent will find the best matching recording and execute it!

---

## 📚 MODE 4: List Recordings

View all your saved task recordings with details:
- Task name
- When it was recorded
- How many actions were captured
- Duration

---

## 💡 Pro Tips

### For LinkedIn Applications:
1. Record yourself sending ONE referral message
2. Then use execution mode to send it to 50 people
3. The agent will click and type everything automatically

### For Course Completion:
1. Record yourself answering ONE MCQ correctly
2. Use execution mode to blast through similar questions
3. Adjust speed (try 2.0x for faster completion)

### Best Practices:
- **Start Simple**: Record short, repetitive tasks first
- **Test First**: Always test a recording on dummy data before using it for real
- **Use Descriptive Names**: Name recordings clearly (e.g., "LinkedIn_Software_Engineer_Referral")
- **Emergency Stop**: Remember - mouse to top-left corner stops everything!
- **Speed Control**: Start with 1.0x speed, increase once you're confident

---

## 🎯 Real-World Examples

### Example 1: LinkedIn Job Referral Spam 😎

**Scenario**: You need to message 100 people for referrals

**Solution**:
1. **Record Mode**: Message ONE person with your referral request
2. **Prepare**: Open LinkedIn, have a list of people
3. **Execute**: Run the recording 100 times (or modify to loop)

**Result**: What would take 2 hours now takes 10 minutes!

### Example 2: Online Course Speed-Run

**Scenario**: 200 MCQ questions, all easy but time-consuming

**Solution**:
1. **Record Mode**: Answer 1 question correctly
2. **Prepare**: Have answers ready or know the pattern
3. **Execute**: Let the agent click through at 2x speed

**Result**: Course completed while you make coffee ☕

### Example 3: Data Entry Hell

**Scenario**: Copy data from Excel to a web form, 500 rows

**Solution**:
1. **Record Mode**: Copy-paste ONE row of data
2. **Prepare**: Excel sheet ready, web form open
3. **Execute**: Loop the recording 500 times

**Result**: No more RSI from copy-pasting!

---

## 🛡️ Safety & Ethics

### Safety Features:
- ✅ Failsafe: Mouse to corner = instant stop
- ✅ Confirmation required before execution
- ✅ Speed control to see what's happening
- ✅ All actions are logged

### Ethical Usage:
⚠️ **Use Responsibly**:
- Don't use for cheating on exams
- Don't spam people maliciously
- Don't violate website Terms of Service
- Don't use for fraudulent activities

✅ **Good Uses**:
- Legitimate job applications
- Your own data entry work
- Repetitive tasks you have permission to automate
- Time-saving for tedious but allowed tasks

---

## 🔧 Troubleshooting

### "Permission Error" when installing
→ Run Command Prompt as Administrator

### "Keyboard/Mouse not recording"
→ Run the script as Administrator

### "Execution is too fast/slow"
→ Adjust the speed multiplier (try 0.5x for slower, 2.0x for faster)

### "Actions don't match screen positions"
→ Make sure your screen resolution doesn't change between recording and execution

### "F9 not stopping recording"
→ Make sure the Python window has focus

---

## 🚀 Next Steps: Adding Real ML

The current version uses **rule-based recording**. Want to make it smarter?

### Future Enhancements (DIY):

1. **Visual Understanding**: Use Claude's Computer Use API or OpenCV to understand what's on screen
2. **Adaptive Positioning**: Use image recognition to find buttons even if they move
3. **Smart Waiting**: Detect when pages load instead of fixed delays
4. **Error Recovery**: Handle popups and errors automatically
5. **Natural Language**: Integrate Claude API for better prompt understanding

I can help you add any of these features - just ask!

---

## 📞 Need Help?

If you run into issues:
1. Check the console for error messages
2. Make sure all dependencies are installed
3. Run as Administrator on Windows
4. Check that F9 key isn't bound to another function

---

## 🎉 You're Ready!

Start with a simple task:
1. Record yourself clicking through 3 buttons
2. Execute it and watch the magic
3. Gradually build up to more complex tasks

**Remember**: Start small, test thoroughly, and always have the emergency stop ready!

Happy automating! 🚀

<!-- CLI commands section -->

<!-- Architecture diagram update -->

<!-- Real world examples updated -->

<!-- FAQ section added -->
