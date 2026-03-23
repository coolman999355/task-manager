# task-manager

This Python project allows users to create, manage, and track multiple schedules with automatic email reminders. Users can add schedules with a specific date and time, view all upcoming tasks, delete schedules, and receive email notifications 10 minutes before a scheduled task. All schedules are stored in a JSON file, making the data persistent across sessions.

The program also includes a menu system for easy interaction, supports multiple schedules at once, and ensures that emails are sent only once per schedule.

Key Features:

Add schedules with name, date, and time.
View all scheduled tasks with sent status.
Delete schedules if needed.
Automatic email reminders using SMTP (Gmail).
Persistent storage in schedules.json.
Safe handling of multiple schedules without repeating emails.

How it works:

Users add a schedule through a simple console menu.
Each schedule is saved in a JSON file with a sent flag to track reminders.
A loop continuously checks if it’s time to send a reminder.
When a reminder is triggered, an email is sent, and the schedule is marked as sent.