# test_task_manager.py
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from models import Task, TaskStatus, TaskPriority
from task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    """Simple tests for TaskManager class."""
    
    def setUp(self):
        """Set up a TaskManager with mocked storage."""
        # Create mock storage
        self.mock_storage = MagicMock()
        
        # Create task manager with mocked storage
        self.manager = TaskManager("test.json")
        self.manager.storage = self.mock_storage
        
        # Sample task for testing
        self.sample_task = Task(
            "Test task", 
            priority=TaskPriority.MEDIUM,
            due_date=datetime(2026, 3, 20)
        )
        self.sample_task.id = "test-id-123"
    
    def test_create_task_returns_id(self):
        """Test that create_task returns a task ID."""
        # Arrange
        self.mock_storage.add_task.return_value = "new-task-id-456"
        
        # Act
        task_id = self.manager.create_task(
            title="Buy milk",
            description="2% milk",
            priority_value=3,
            due_date_str="2026-03-20",
            tags=["shopping", "groceries"]
        )
        
        # Assert
        self.assertEqual(task_id, "new-task-id-456")
        self.mock_storage.add_task.assert_called_once()
        
        # Verify task passed to storage has correct attributes
        called_task = self.mock_storage.add_task.call_args[0][0]
        self.assertEqual(called_task.title, "Buy milk")
        self.assertEqual(called_task.description, "2% milk")
        self.assertEqual(called_task.priority, TaskPriority.HIGH)
        self.assertEqual(called_task.tags, ["shopping", "groceries"])
    
    def test_list_tasks_with_filters(self):
        """Test that list_tasks calls correct storage methods."""
        # Act - list all tasks
        self.manager.list_tasks()
        self.mock_storage.get_all_tasks.assert_called_once()
        
        # Act - filter by status
        self.manager.list_tasks(status_filter="todo")
        self.mock_storage.get_tasks_by_status.assert_called_with(TaskStatus.TODO)
        
        # Act - filter by priority
        self.manager.list_tasks(priority_filter=3)
        self.mock_storage.get_tasks_by_priority.assert_called_with(TaskPriority.HIGH)
        
        # Act - show overdue
        self.manager.list_tasks(show_overdue=True)
        self.mock_storage.get_overdue_tasks.assert_called_once()
    
    def test_update_task_status_done(self):
        """Test that marking task as done calls mark_as_done."""
        # Arrange
        self.mock_storage.get_task.return_value = self.sample_task
        
        # Act
        result = self.manager.update_task_status("test-id-123", "done")
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(self.sample_task.status, TaskStatus.DONE)
        self.assertIsNotNone(self.sample_task.completed_at)
        self.mock_storage.save.assert_called_once()
    
    def test_get_statistics_calculates_correctly(self):
        """Test that statistics are calculated correctly."""
        # Arrange - create mock tasks
        today = datetime.now()
        
        task1 = Task("Task 1")
        task1.status = TaskStatus.TODO
        task1.priority = TaskPriority.HIGH
        
        task2 = Task("Task 2")
        task2.status = TaskStatus.DONE
        task2.priority = TaskPriority.MEDIUM
        task2.completed_at = today - timedelta(days=2)  # Within last week
        
        task3 = Task("Task 3")
        task3.status = TaskStatus.TODO
        task3.priority = TaskPriority.URGENT
        task3.due_date = today - timedelta(days=1)  # Overdue
        
        task4 = Task("Task 4")
        task4.status = TaskStatus.DONE
        task4.priority = TaskPriority.LOW
        task4.completed_at = today - timedelta(days=10)  # Older than a week
        
        self.mock_storage.get_all_tasks.return_value = [task1, task2, task3, task4]
        
        # Act
        stats = self.manager.get_statistics()
        
        # Assert
        self.assertEqual(stats["total"], 4)
        self.assertEqual(stats["overdue"], 1)
        self.assertEqual(stats["completed_last_week"], 1)
        self.assertEqual(stats["by_status"]["todo"], 2)
        self.assertEqual(stats["by_status"]["done"], 2)


if __name__ == '__main__':
    unittest.main()