# TaskMaster Pro 📝

A modern task management desktop application built with Python and Tkinter.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)

## What's This?

A sleek, dark-themed task manager that helps you organize your to-do list. Created as an ITI Python project demonstrating OOP, GUI development, and file handling.

## Features

- **User Authentication** - Secure login/registration with password hashing
- **Task Management** - Create, edit, delete, and track tasks with priorities
- **Search & Filter** - Find tasks quickly by title or status
- **User Profiles** - Edit your personal information
- **Admin Panel** - Manage users and view activity logs (admin only)
- **Reminders** - Get notified about upcoming and overdue tasks
- **JSON Storage** - All data saved locally in human-readable format

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/taskmaster-pro.git
cd taskmaster-pro

# Run the app (no dependencies needed!)
python main.py
```

That's it! Pure Python with built-in Tkinter.

## Project Structure

```
TaskManagementSystem/
├── main.py              # Entry point
├── config/              # App settings & theme
├── models/              # User & Task classes
├── data/                # Storage & validation
├── services/            # Business logic
├── gui/                 # All UI components
├── utils/               # Helper functions
└── storage/             # JSON data files (auto-created)
```

## First Run

1. Register a new account (try both Regular User and Admin roles)
2. Create some tasks with different priorities
3. Test search, filters, and editing
4. Check out the reminders feature

**Sample Login:**
- Email: `admin@test.com`
- Password: `admin123`
- (You'll need to register first!)

## Tech Highlights

- **OOP Design**: Proper classes and separation of concerns
- **Modular Architecture**: Each component in its own file
- **JSON Storage**: Simple, readable data persistence
- **Input Validation**: Egyptian ID/phone numbers, email, dates
- **Password Security**: SHA-256 hashing
- **Modern GUI**: Custom widgets and color schemes

## Screenshots

*Login Screen - Clean and minimal*
```
┌─────────────────────────────┐
│     TaskMaster Pro          │
│   Sign in to your account   │
│                             │
│   Email: _______________    │
│   Password: ___________     │
│                             │
│      [   Sign In   ]        │
└─────────────────────────────┘
```

*Dashboard - At a glance overview*
```
Statistics Cards → [Total: 12] [Completed: 5] [In Progress: 4] [To-Do: 3]
Task List → Color-coded cards with priority bars
```

## Why This Project?

Built to demonstrate:
- ✅ Object-Oriented Programming in Python
- ✅ GUI development with Tkinter
- ✅ File handling and data persistence
- ✅ User authentication and security
- ✅ Clean, maintainable code structure

Perfect for learning or as a portfolio piece!

## Requirements

- Python 3.7 or higher
- Tkinter (included with Python)
- That's it!

---

<div align="center">

**Made with ☕ and Python**

</div>
