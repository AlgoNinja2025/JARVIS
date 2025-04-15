import os

def alarm(query):
    try:
        # Ensure the query contains a valid time format (HH:MM:SS)
        with open("Alarmtext.txt", "a") as timehere:
            timehere.write(query.strip() + "\n")  # Strip any extra spaces

        # Check if alarm.py exists before attempting to start it
        if os.path.exists("alarm.py"):
            os.startfile("alarm.py")
        else:
            print("Error: alarm.py not found. Please make sure it exists in the same directory.")

    except FileNotFoundError:
        print("Error: Alarmtext.txt file not found.")
    except Exception as e:
        print(f"An unexpected error occurred while setting the alarm: {e}")

