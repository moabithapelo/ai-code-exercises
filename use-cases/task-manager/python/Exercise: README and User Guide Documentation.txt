Project Selected: Task Manager CLI

The Task Manager is a command-line task management application written in Python 
that allows users to create, organize, prioritize, and track tasks with features 
like due dates, priorities, tags, and status tracking.

Prompt 1 - Comprehensive README Generation:

Please create a comprehensive README.md file for my project based on the following information:

Project name: Task Manager CLI
Description: A command-line task management application that helps users organize, prioritize, and track their tasks with features like due dates, priority levels, tags, and status tracking. Tasks are persisted in a JSON file for data durability between sessions.

Key features:
- Create tasks with titles, descriptions, due dates, priority levels (LOW/MEDIUM/HIGH/URGENT), and tags
- List tasks with filtering by status, priority, or overdue status
- Update task status (TODO → IN_PROGRESS → REVIEW → DONE)
- Update task priority and due dates
- Add and remove tags from tasks
- View detailed task information
- Delete tasks
- View task statistics (counts by status/priority, overdue tasks, recently completed)
- Automatic priority scoring algorithm to identify most important tasks

Technologies used:
- Python 3.8+
- Standard library only (no external dependencies)
  - argparse for CLI interface
  - datetime for date handling
  - json for data persistence
  - enum for status/priority types
  - uuid for unique task IDs

Installation requirements:
- Python 3.8 or higher installed on your system
- No additional packages required

The README should include:
1. Clear project title and description
2. Installation instructions
3. Basic usage examples
4. Features overview
5. Configuration options
6. Troubleshooting section
7. Contributing guidelines
8. License information

Code structure overview:
task_manager/
├── app.py          # Core application logic (TaskManager class)
├── cli.py          # Command-line interface (argument parsing)
├── models.py       # Domain models (Task, TaskPriority, TaskStatus)
└── storage.py      # Data persistence (JSON file storage with custom encoders)

AI-Generated README.md:

# Task Manager CLI

A lightweight, feature-rich command-line task management application written in pure Python. Organize your tasks with priorities, due dates, tags, and status tracking—all stored locally in a JSON file.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
  - [Creating Tasks](#creating-tasks)
  - [Listing Tasks](#listing-tasks)
  - [Updating Tasks](#updating-tasks)
  - [Managing Tags](#managing-tags)
  - [Task Statistics](#task-statistics)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Task Creation** – Add tasks with titles, descriptions, due dates, priority levels (LOW/MEDIUM/HIGH/URGENT), and tags
- **Smart Filtering** – List tasks filtered by status, priority, or overdue status
- **Status Tracking** – Move tasks through workflow: TODO → IN_PROGRESS → REVIEW → DONE
- **Priority Management** – Update task priority and due dates anytime
- **Tag System** – Add and remove tags for better organization
- **Detailed Views** – Inspect full task details including timestamps
- **Statistics Dashboard** – View task counts by status/priority, overdue tasks, and weekly completion rates
- **Priority Scoring** – Built-in algorithm to identify your most important tasks
- **Persistent Storage** – All data saved to a JSON file (no database required)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher installed on your system

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/task-manager-cli.git
   cd task-manager-cli

Quick Start:

# Create your first task
python -m task_manager.cli create "Buy groceries" -d "Milk, eggs, bread" -p 3 -u 2026-03-20 -t "shopping,personal"

# List all tasks
python -m task_manager.cli list

# Mark a task as in progress
python -m task_manager.cli status <task-id> in_progress

# Mark a task as complete
python -m task_manager.cli status <task-id> done

# View task statistics
python -m task_manager.cli stats

# Get help
python -m task_manager.cli --help

 Usage Guide:

 Creating Tasks:

 # Basic task (title only)
python -m task_manager.cli create "Write documentation"

# Task with description and priority
python -m task_manager.cli create "Prepare presentation" -d "Slides for Monday meeting" -p 4

# Task with due date and tags
python -m task_manager.cli create "Submit report" -u 2026-03-25 -t "work,deadline"

# Full example
python -m task_manager.cli create "Review pull request" -d "Check code changes" -p 3 -u 2026-03-18 -t "github,code-review"


Project Structure:

task_manager/
├── __init__.py          # Package initialization
├── app.py               # Core application logic (TaskManager class)
│   └── TaskManager      # Main service class orchestrating all operations
├── cli.py               # Command-line interface with argparse
│   └── main()           # Entry point for CLI commands
├── models.py            # Domain models and business logic
│   ├── Task             # Main task entity with business methods
│   ├── TaskPriority     # Enum: LOW(1), MEDIUM(2), HIGH(4), URGENT(6)
│   └── TaskStatus       # Enum: TODO, IN_PROGRESS, REVIEW, DONE
└── storage.py           # Data persistence layer
    ├── TaskStorage      # Repository for task data
    ├── TaskEncoder      # Custom JSON encoder for Task objects
    └── TaskDecoder      # Custom JSON decoder for Task objects


Troubleshooting:


"No module named task_manager"

Make sure you're running the command from the parent directory of task_manager, or add the parent directory to your PYTHONPATH.
Tasks not saving

    Check write permissions in the current directory

    Verify the tasks.json file isn't corrupted (try deleting it to start fresh)

Invalid date format error

Always use YYYY-MM-DD format for dates (e.g., 2026-03-20)
Task not found

Task IDs are UUIDs. Use the full ID shown in list commands, or copy-paste to avoid typos.
Priority values not working

Priority must be 1 (LOW), 2 (MEDIUM), 3 (HIGH), or 4 (URGENT)


Apply Prompt 2 - Step-by-Step Guide Creation:


---

## AI-Generated Step-by-Step Guide

```markdown
# How to Prioritize and Focus on Your Most Important Tasks in Task Manager

This guide will help you identify which tasks deserve your attention first using Task Manager's built-in priority scoring system.

## 🎯 What You'll Learn
- Understanding how tasks are prioritized
- Viewing tasks in priority order
- Filtering to find the right focus
- Getting your top priorities quickly

## 📋 Prerequisites
- Task Manager installed and working
- At least a few tasks created in the system
- Basic familiarity with command-line operations

---

## Step-by-Step Instructions

### Step 1: Understand How Priority Scoring Works

Task Manager automatically calculates a priority score for each task based on multiple factors. Higher scores = higher priority.

**Priority factors and their weights:**
- **Base priority**: LOW=10, MEDIUM=20, HIGH=40, URGENT=60 points
- **Due date**: Overdue (+35), Due today (+20), Due in 2 days (+15), Due in a week (+10)
- **Status**: DONE (-50 penalty), REVIEW (-15 penalty)
- **Critical tags**: +8 for "blocker", "critical", or "urgent" tags
- **Recent activity**: +5 if updated in last 24 hours

```python
# Example scores:
# URGENT + Overdue + Critical tag = ~103 (highest priority)
# LOW + No due date = 10 (lowest priority)
# DONE task = -50 (effectively removed from priority lists)


Apply Prompt 3 - FAQ Document Generation:


---

## AI-Generated FAQ Document

```markdown
# Task Manager CLI - Frequently Asked Questions

## 📋 General Questions

### What is Task Manager CLI?
Task Manager CLI is a command-line application that helps you organize and track tasks. It stores everything in a JSON file and uses only Python's standard library—no external dependencies required.

### Do I need to install anything besides Python?
No! Task Manager uses only Python's built-in modules. If you have Python 3.8 or higher, you're ready to go.

### How do I get help while using the app?
```bash
# General help
python -m task_manager.cli --help

# Help for a specific command
python -m task_manager.cli create --help
python -m task_manager.cli list --help

Compare and Reflect:


---

## Step 4: Compare and Reflect

### Comparison Checklist

| Document Type | Purpose | Target Audience | Key Strengths |
|---------------|---------|-----------------|---------------|
| **README.md** | Project overview, installation, quick start | New users, potential contributors | Comprehensive, well-structured, includes badges and table of contents |
| **Priority Guide** | Step-by-step tutorial for specific feature | Beginners learning the workflow | Action-oriented, common mistakes, troubleshooting, daily routine |
| **FAQ** | Quick answers to common questions | All users, especially those stuck | Searchable, covers edge cases, practical solutions |

### Insights from Each Prompt Approach

**Prompt 1 (README Generation)** was most valuable for creating a **complete project overview** that serves as the entry point for anyone discovering the project. The structured format with badges, table of contents, and clear sections makes it professional and approachable.

**Prompt 2 (Step-by-Step Guide)** excelled at creating a **learning pathway** for a specific feature. The "Daily Priority Routine" section transforms abstract features into practical habits.

**Prompt 3 (FAQ)** was best for **covering edge cases and common pain points** that wouldn't fit in the main documentation but are essential for user success.

### What I'd Improve

1. **Add actual screenshots** where placeholders are indicated
2. **Include a "Quick Reference Card"** with all commands
3. **Add more examples** for complex scenarios (e.g., bulk operations)
4. **Create video tutorial links** for visual learners

### How These Documents Work Together

- **README** = Front door ("What is this?")
- **Priority Guide** = Living room ("How do I use it day-to-day?")
- **FAQ** = Toolbox ("How do I fix this specific problem?")

---

## Final Submission Summary

  Item               | Description 
 --------------------|-------------
| **README.md**      | Complete project documentation with installation, features, usage, and contribution guidelines |
| **Priority Guide** | Step-by-step tutorial for prioritizing tasks using the scoring algorithm |
| **FAQ**            | Comprehensive Q&A covering getting started, features, troubleshooting, and data management |

