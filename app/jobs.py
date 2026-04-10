import time
import logging

def send_due_date_notification(task_title):
    time.sleep(5) #wait 5 seconds
    logging.warning(f"Reminder: Task '{task_title}' is due soon!")