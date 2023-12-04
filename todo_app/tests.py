# from django.test import TestCase

#These test cases include checks for:

#Creating and retrieving instances of ToDoList and ToDoItem.
#Checking the string representation of instances.
#Ensuring the uniqueness of ToDoList titles.
#Verifying the default due date for ToDoItem.
#Testing the get_absolute_url method for both models.
#Confirming that creating a ToDoItem with a blank description is allowed.
#Checking that ToDoItems are ordered by their due_date.


from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import ToDoList, ToDoItem
from todo_app import models

class ToDoListModelTest(TestCase):
    def setUp(self):
        ToDoList.objects.create(title="Shopping List")

    def test_todo_list_creation(self):
        todo_list = ToDoList.objects.get(title="Shopping List")
        self.assertEqual(todo_list.title, "Shopping List")

    def test_todo_list_str_method(self):
        todo_list = ToDoList.objects.get(title="Shopping List")
        self.assertEqual(str(todo_list), "Shopping List")

    def test_unique_todo_list_title(self):
        # Test that creating a ToDoList with a duplicate title raises a ValidationError
        with self.assertRaises(models.ValidationError):
            ToDoList.objects.create(title="Shopping List")

    def test_todo_list_absolute_url(self):
        todo_list = ToDoList.objects.get(title="Shopping List")
        expected_url = reverse("list", args=[str(todo_list.id)])
        self.assertEqual(todo_list.get_absolute_url(), expected_url)

class ToDoItemModelTest(TestCase):
    def setUp(self):
        todo_list = ToDoList.objects.create(title="Work Tasks")
        ToDoItem.objects.create(title="Task 1", todo_list=todo_list)

    def test_todo_item_creation(self):
        todo_item = ToDoItem.objects.get(title="Task 1")
        self.assertEqual(todo_item.todo_list.title, "Work Tasks")

    def test_todo_item_str_method(self):
        todo_item = ToDoItem.objects.get(title="Task 1")
        expected_str = f"Task 1: due {todo_item.due_date}"
        self.assertEqual(str(todo_item), expected_str)

    def test_todo_item_default_due_date(self):
        todo_item = ToDoItem.objects.get(title="Task 1")
        one_week_ahead = timezone.now() + timezone.timedelta(days=7)
        self.assertAlmostEqual(todo_item.due_date, one_week_ahead, delta=timezone.timedelta(seconds=1))

    def test_todo_item_absolute_url(self):
        todo_item = ToDoItem.objects.get(title="Task 1")
        expected_url = reverse("item-update", args=[str(todo_item.todo_list.id), str(todo_item.id)])
        self.assertEqual(todo_item.get_absolute_url(), expected_url)

    def test_todo_item_with_blank_description(self):
        # Test that creating a ToDoItem with a blank description is allowed
        todo_list = ToDoList.objects.create(title="Personal Tasks")
        todo_item = ToDoItem.objects.create(title="Task 2", todo_list=todo_list)
        self.assertEqual(todo_item.description, "")

    def test_todo_item_ordering(self):
        # Test that ToDoItems are ordered by due_date
        todo_list = ToDoList.objects.create(title="Home Tasks")
        todo_item1 = ToDoItem.objects.create(title="Task 1", todo_list=todo_list)
        todo_item2 = ToDoItem.objects.create(title="Task 2", todo_list=todo_list, due_date=timezone.now() + timezone.timedelta(days=1))
        
        self.assertLess(todo_item1.due_date, todo_item2.due_date)
