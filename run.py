from trading import check_program_status
import schedule
import time

def check_program_status_wrapper():
    print("Checking program status...")
    check_program_status()

# Schedule the check_program_status_wrapper function to run every minute
schedule.every(1).minutes.do(check_program_status_wrapper)

while True:
    # Run pending scheduled jobs
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
