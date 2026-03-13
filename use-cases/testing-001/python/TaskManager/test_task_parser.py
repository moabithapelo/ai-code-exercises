# test_task_parser.py
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from models import TaskPriority
from task_parser import parse_task_from_text


class TestParseTaskFromText(unittest.TestCase):
    """Simple tests for the parse_task_from_text function."""
    
    @patch('task_parser.datetime')
    def test_basic_task_parsing(self, mock_datetime):
        """Test that basic text becomes task title with default values."""
        # Arrange
        mock_datetime.now.return_value = datetime(2026, 3, 13)
        
        # Act
        task = parse_task_from_text("Buy groceries")
        
        # Assert
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertIsNone(task.due_date)
        self.assertEqual(task.tags, [])
    
    def test_priority_number_parsing(self):
        """Test that !1, !2, !3, !4 set correct priorities."""
        # Act
        low_task = parse_task_from_text("Low priority task !1")
        medium_task = parse_task_from_text("Medium priority task !2")
        high_task = parse_task_from_text("High priority task !3")
        urgent_task = parse_task_from_text("Urgent priority task !4")
        
        # Assert
        self.assertEqual(low_task.priority, TaskPriority.LOW)
        self.assertEqual(medium_task.priority, TaskPriority.MEDIUM)
        self.assertEqual(high_task.priority, TaskPriority.HIGH)
        self.assertEqual(urgent_task.priority, TaskPriority.URGENT)
        
        # Check that priority marker removed from title
        self.assertEqual(low_task.title, "Low priority task")
    
    def test_priority_name_parsing(self):
        """Test that !low, !medium, !high, !urgent set correct priorities."""
        # Act
        low_task = parse_task_from_text("Low task !low")
        medium_task = parse_task_from_text("Medium task !medium")
        high_task = parse_task_from_text("High task !high")
        urgent_task = parse_task_from_text("Urgent task !urgent")
        
        # Assert
        self.assertEqual(low_task.priority, TaskPriority.LOW)
        self.assertEqual(medium_task.priority, TaskPriority.MEDIUM)
        self.assertEqual(high_task.priority, TaskPriority.HIGH)
        self.assertEqual(urgent_task.priority, TaskPriority.URGENT)
    
    def test_tag_parsing(self):
        """Test that @tag adds tags."""
        # Act
        task = parse_task_from_text("Work on project @work @important @deadline")
        
        # Assert
        self.assertEqual(task.title, "Work on project")
        self.assertEqual(task.tags, ["work", "important", "deadline"])
    
    def test_date_parsing(self):
        """Test that #date sets due date correctly."""
        # Arrange
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Act
        today_task = parse_task_from_text("Task #today")
        tomorrow_task = parse_task_from_text("Task #tomorrow")
        nextweek_task = parse_task_from_text("Task #next_week")
        friday_task = parse_task_from_text("Task #friday")
        
        # Assert
        self.assertEqual(today_task.due_date, today)
        self.assertEqual(tomorrow_task.due_date, today + timedelta(days=1))
        self.assertEqual(nextweek_task.due_date, today + timedelta(days=7))
        
        # Check that date marker removed from title
        self.assertEqual(today_task.title, "Task")
    
    def test_complete_task_parsing(self):
        """Test parsing a task with all features."""
        # Act
        task = parse_task_from_text(
            "Finish quarterly report !high @work @urgent #friday"
        )
        
        # Assert
        self.assertEqual(task.title, "Finish quarterly report")
        self.assertEqual(task.priority, TaskPriority.HIGH)
        self.assertEqual(set(task.tags), {"work", "urgent"})
        # Due date should be next Friday (we don't test exact date here)


if __name__ == '__main__':
    unittest.main()