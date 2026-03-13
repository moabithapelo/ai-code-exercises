# test_task_score.py
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from models import Task, TaskStatus, TaskPriority
from task_score import calculate_task_score


class TestCalculateTaskScore(unittest.TestCase):
    """Simple tests for the calculate_task_score function."""
    
    def setUp(self):
        """Set up fixed time for predictable tests."""
        self.fixed_now = datetime(2026, 3, 13, 12, 0, 0)  # Friday, March 13, 2026
        
    @patch('task_score.datetime')
    def test_priority_only_score(self, mock_datetime):
        """Test that different priorities produce correct base scores."""
        # Arrange
        mock_datetime.now.return_value = self.fixed_now
        
        # Create tasks with different priorities (all other fields default)
        low_task = Task("Low task", priority=TaskPriority.LOW)
        medium_task = Task("Medium task", priority=TaskPriority.MEDIUM)
        high_task = Task("High task", priority=TaskPriority.HIGH)
        urgent_task = Task("Urgent task", priority=TaskPriority.URGENT)
        
        # Act
        low_score = calculate_task_score(low_task)
        medium_score = calculate_task_score(medium_task)
        high_score = calculate_task_score(high_task)
        urgent_score = calculate_task_score(urgent_task)
        
        # Assert
        self.assertEqual(low_score, 10, "LOW priority should score 10")
        self.assertEqual(medium_score, 20, "MEDIUM priority should score 20")
        self.assertEqual(high_score, 40, "HIGH priority should score 40")
        self.assertEqual(urgent_score, 60, "URGENT priority should score 60")
    
    @patch('task_score.datetime')
    def test_due_date_bonuses(self, mock_datetime):
        """Test that due dates add correct bonuses."""
        # Arrange
        mock_datetime.now.return_value = self.fixed_now
        
        # Create tasks with different due dates (LOW priority = base 10)
        overdue_task = Task("Overdue", priority=TaskPriority.LOW, 
                           due_date=self.fixed_now - timedelta(days=1))
        due_today_task = Task("Today", priority=TaskPriority.LOW, 
                             due_date=self.fixed_now)
        due_tomorrow_task = Task("Tomorrow", priority=TaskPriority.LOW, 
                                due_date=self.fixed_now + timedelta(days=1))
        due_in_5_days_task = Task("In 5 days", priority=TaskPriority.LOW, 
                                  due_date=self.fixed_now + timedelta(days=5))
        due_in_10_days_task = Task("In 10 days", priority=TaskPriority.LOW, 
                                   due_date=self.fixed_now + timedelta(days=10))
        no_due_task = Task("No due", priority=TaskPriority.LOW)
        
        # Act
        overdue_score = calculate_task_score(overdue_task)
        today_score = calculate_task_score(due_today_task)
        tomorrow_score = calculate_task_score(due_tomorrow_task)
        five_days_score = calculate_task_score(due_in_5_days_task)
        ten_days_score = calculate_task_score(due_in_10_days_task)
        no_due_score = calculate_task_score(no_due_task)
        
        # Assert
        self.assertEqual(overdue_score, 10 + 35, "Overdue should add +35")
        self.assertEqual(today_score, 10 + 20, "Due today should add +20")
        self.assertEqual(tomorrow_score, 10 + 15, "Due in 1 day should add +15")
        self.assertEqual(five_days_score, 10 + 10, "Due in 5 days should add +10")
        self.assertEqual(ten_days_score, 10, "Due in 10 days should add +0")
        self.assertEqual(no_due_score, 10, "No due date should add +0")
    
    @patch('task_score.datetime')
    def test_status_penalties_and_tag_bonus(self, mock_datetime):
        """Test status penalties and tag bonuses."""
        # Arrange
        mock_datetime.now.return_value = self.fixed_now
        
        # Test status penalties
        done_task = Task("Done", priority=TaskPriority.LOW, status=TaskStatus.DONE)
        review_task = Task("Review", priority=TaskPriority.LOW, status=TaskStatus.REVIEW)
        
        # Test tag bonuses
        blocker_tag_task = Task("Blocker", priority=TaskPriority.LOW, tags=["blocker"])
        critical_tag_task = Task("Critical", priority=TaskPriority.LOW, tags=["critical"])
        urgent_tag_task = Task("Urgent tag", priority=TaskPriority.LOW, tags=["urgent"])
        multiple_tags_task = Task("Multiple", priority=TaskPriority.LOW, 
                                  tags=["blocker", "critical", "work"])
        no_tag_task = Task("No tag", priority=TaskPriority.LOW, tags=[])
        
        # Act
        done_score = calculate_task_score(done_task)
        review_score = calculate_task_score(review_task)
        
        blocker_score = calculate_task_score(blocker_tag_task)
        critical_score = calculate_task_score(critical_tag_task)
        urgent_tag_score = calculate_task_score(urgent_tag_task)
        multiple_score = calculate_task_score(multiple_tags_task)
        no_tag_score = calculate_task_score(no_tag_task)
        
        # Assert
        self.assertEqual(done_score, 10 - 50, "DONE status should subtract 50")
        self.assertEqual(review_score, 10 - 15, "REVIEW status should subtract 15")
        
        self.assertEqual(blocker_score, 10 + 8, "Blocker tag should add +8")
        self.assertEqual(critical_score, 10 + 8, "Critical tag should add +8")
        self.assertEqual(urgent_tag_score, 10 + 8, "Urgent tag should add +8")
        self.assertEqual(multiple_score, 10 + 8, "Multiple matching tags add +8 only once")
        self.assertEqual(no_tag_score, 10, "No tags should add +0")


if __name__ == '__main__':
    unittest.main()