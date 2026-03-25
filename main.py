from datetime import datetime, timedelta
import time
import smtplib
import json
import os
import threading
import uuid  # For generating unique IDs for each task

# ---------------- CONFIGURATION ----------------

json_file = "schedules.json"  # File to store all schedules

# Ask user for Gmail login info
app_password = input("Enter app password: ")
my_email = input("Enter your email: ")

# ---------------- FILE HANDLING FUNCTIONS ----------------

def load_schedules():
    """
    Load schedules from JSON file.
    Returns a list of schedule dictionaries.
    """
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            try:
                return json.load(file)
            except:
                return []  # Return empty list if file is corrupted
    return []  # Return empty list if file doesn't exist

def save_all_schedules(schedules):
    """
    Save all schedules to JSON file.
    """
    with open(json_file, "w") as file:
        json.dump(schedules, file, indent=4)

# ---------------- CORE FUNCTIONS ----------------

def add_schedule(name, year, month, day, hour, minute, deadline):
    """
    Add a new schedule to the list and save it.
    Each schedule gets a unique ID for tracking.
    """
    schedules = load_schedules()

    schedule = {
        "id": str(uuid.uuid4()),  # Unique ID for this task
        "name": name,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "deadline": deadline,  # description like "homework" or "exam"
        "reminder_sent": False,  # Flag to check if reminder email was sent
        "deadline_sent": False   # Flag to check if deadline email was sent
    }

    schedules.append(schedule)
    save_all_schedules(schedules)
    print(" Schedule added!")

def view_schedules():
    """
    Display all schedules in a readable format.
    """
    schedules = load_schedules()

    if not schedules:
        print(" No schedules.")
        return

    print("\n Your schedules:\n")
    for i, s in enumerate(schedules):
        print(
            f"{i+1}. {s['name']} | "
            f"{s['year']}/{s['month']}/{s['day']} "
            f"{s['hour']}:{s['minute']:02d} | "
            f"Deadline: {s['deadline']} | "
            f"Reminder: {s['reminder_sent']} | "
            f"Done: {s['deadline_sent']}"
        )

def delete_schedule(index):
    """
    Delete a schedule by index (shown in view_schedules).
    """
    schedules = load_schedules()

    if 0 <= index < len(schedules):
        removed = schedules.pop(index)
        save_all_schedules(schedules)
        print(f" Deleted: {removed['name']}")
    else:
        print(" Invalid index")

# ---------------- EMAIL FUNCTIONS ----------------

def send_email(subject, body):
    """
    Send an email with given subject and body to yourself.
    """
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # Secure connection
            connection.login(user=my_email, password=app_password)

            message = f"Subject:{subject}\n\n{body}"

            # Send email to yourself
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=message
            )

        print(f" Sent: {subject}")

    except Exception as e:
        print(" Email error:", e)

# ---------------- MARKING FUNCTIONS ----------------

def mark_sent(schedule_id, key):
    """
    Mark a schedule as reminder_sent or deadline_sent.
    """
    schedules = load_schedules()

    for s in schedules:
        if s["id"] == schedule_id:
            s[key] = True  # Update the correct flag

    save_all_schedules(schedules)

# ---------------- SCHEDULER LOOP ----------------

def check_schedules():
    """
    Background loop that checks all schedules every 5 seconds.
    Sends reminder emails 10 minutes before the task,
    and deadline emails when the task time is reached.
    """
    print(" Reminder system running...")

    while True:
        schedules = load_schedules()
        now = datetime.now()

        for s in schedules:
            # Build datetime object for the scheduled task
            task_dt = datetime(
                s["year"], s["month"], s["day"],
                s["hour"], s["minute"]
            )

            reminder_time = task_dt - timedelta(minutes=10)

            # Skip tasks that are fully completed
            if s["reminder_sent"] and s["deadline_sent"]:
                continue

            # Send reminder email if within 10 minutes
            if reminder_time <= now < task_dt and not s["reminder_sent"]:
                send_email(
                    "Reminder",
                    f"Task '{s['name']}' is in 10 minutes!"
                )
                mark_sent(s["id"], "reminder_sent")
                continue  # Skip deadline check for this loop

            # Send deadline email if task time passed
            if now >= task_dt and not s["deadline_sent"]:
                send_email(
                    "Deadline Reached",
                    f"Time for '{s['name']}'!"
                )
                mark_sent(s["id"], "deadline_sent")

        time.sleep(5)  # Wait 5 seconds before next check

# ---------------- MENU ----------------

def main_menu():
    """
    Main interactive menu for user.
    """
    while True:
        print("\n====== SMART SCHEDULER ======")
        print("1. Add")
        print("2. View")
        print("3. Delete")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            # Add a new task
            try:
                name = input("Task: ")
                year = int(input("Year: "))
                month = int(input("Month: "))
                day = int(input("Day: "))
                hour = int(input("Hour: "))
                minute = int(input("Minute: "))
                deadline = input("Deadline description: ")

                add_schedule(name, year, month, day, hour, minute, deadline)

            except:
                print(" Invalid input")

        elif choice == "2":
            view_schedules()  # Show all tasks

        elif choice == "3":
            view_schedules()
            try:
                i = int(input("Delete number: ")) - 1
                delete_schedule(i)
            except:
                print(" Invalid")

        elif choice == "4":
            print(" Bye!")
            break

        else:
            print(" Invalid")

# ---------------- RUN ----------------

if __name__ == "__main__":
    # Start reminder system in the background thread
    threading.Thread(target=check_schedules, daemon=True).start()

    # Start interactive menu
    main_menu()
