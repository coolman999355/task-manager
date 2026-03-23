from datetime import datetime, timedelta
import time
import smtplib
import json
import os

json_file = "schedules.json"

app_password = input("Enter app password: ")
my_email = input("Enter your email: ")


def load_schedules():
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_all_schedules(schedules):
    with open(json_file, "w") as file:
        json.dump(schedules, file, indent=4)


def add_schedule(schedule_name, year, month, day, hour, minute):
    schedules = load_schedules()

    schedule_data = {
        "schedule_name": schedule_name,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "sent": False
    }

    schedules.append(schedule_data)
    save_all_schedules(schedules)
    print(" Schedule saved!")


def view_schedules():
    schedules = load_schedules()

    if not schedules:
        print("No schedules found.")
        return

    print("\n Your schedules:")
    for i, s in enumerate(schedules):
        print(f"{i+1}. {s['schedule_name']} - {s['year']}/{s['month']}/{s['day']} {s['hour']}:{s['minute']} | Sent: {s['sent']}")


def delete_schedule(index):
    schedules = load_schedules()

    if 0 <= index < len(schedules):
        removed = schedules.pop(index)
        save_all_schedules(schedules)
        print(f" Deleted: {removed['schedule_name']}")
    else:
        print(" Invalid index")


def send_email(schedule_name):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=app_password)

            subject = "Reminder!"
            body = f" Your task '{schedule_name}' is coming soon!"

            message = f"Subject:{subject}\n\n{body}"

            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=message
            )

        print(f" Email sent for '{schedule_name}'!")

    except Exception as e:
        print(" Email error:", e)


def mark_as_sent(schedule):
    schedules = load_schedules()

    for s in schedules:
        if s == schedule:
            s["sent"] = True

    save_all_schedules(schedules)


def check_schedules():
    print(" Checking schedules... (CTRL+C to stop)")

    while True:
        schedules = load_schedules()
        now = datetime.now()

        for schedule in schedules:
            task_dt = datetime(
                schedule["year"],
                schedule["month"],
                schedule["day"],
                schedule["hour"],
                schedule["minute"]
            )

            reminder_time = task_dt - timedelta(minutes=10)

            if reminder_time <= now < task_dt and not schedule.get("sent", False):
                send_email(schedule["schedule_name"])
                mark_as_sent(schedule)

        time.sleep(5)


while True:
    print("\n====== SMART SCHEDULER ======")
    print("1. Add schedule")
    print("2. View schedules")
    print("3. Delete schedule")
    print("4. Start reminder system")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        print(" Use 24-hour format (14 = 2PM)")
        name = input("Task name: ")
        year = int(input("Year: "))
        month = int(input("Month: "))
        day = int(input("Day: "))
        hour = int(input("Hour: "))
        minute = int(input("Minute: "))

        add_schedule(name, year, month, day, hour, minute)

    elif choice == "2":
        view_schedules()

    elif choice == "3":
        view_schedules()
        index = int(input("Enter number to delete: ")) - 1
        delete_schedule(index)

    elif choice == "4":
        check_schedules()

    elif choice == "5":
        print(" Bye!")
        break

    else:
        print(" Invalid choice")