import datetime
import pytz
import os
import sys
from O365 import Account, FileSystemTokenBackend

class OutlookMeetingScheduler:
    def __init__(self, client_id, client_secret=None):
        self.credentials = (client_id, client_secret) if client_secret else (client_id,)
        self.token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')
        self.account = Account(self.credentials, token_backend=self.token_backend)
        self.schedule = None

    def authenticate(self):
        """Authenticates the user using O365 library."""
        print("Authenticating...")
        # basic and calendar_all scopes are needed to read/write calendar
        if not self.account.is_authenticated:
            # This will print a URL to the console for the user to visit
            # and paste the result back if using console flow.
            self.account.authenticate(scopes=['basic', 'calendar_all'])
        else:
            print("Already authenticated!")
        
        self.schedule = self.account.schedule()
        print("Authentication successful.")

    def get_ist_time(self):
        """Returns the current time and the target meeting time in IST."""
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.datetime.now(ist)
        
        # Target: Today at 9:00 AM IST
        meeting_start = now_ist.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # If 9 AM has already passed today, maybe schedule for tomorrow? 
        # The prompt says "scheduled for today", so we stick to today even if it's in the past 
        # (Outlook allows creating past events), or we can warn.
        # Let's stick to the prompt: "scheduled for today at 9 am IST".
        
        meeting_end = meeting_start + datetime.timedelta(hours=1) # 1 hour duration
        
        return meeting_start, meeting_end

    def check_availability(self, start_time, end_time):
        """Checks if the time slot is free."""
        print(f"Checking availability for {start_time} to {end_time}...")
        
        # Get events for the specific time range
        q = self.schedule.new_query('start').greater_equal(start_time)
        q.chain('and').on_attribute('end').less_equal(end_time)
        
        events = self.schedule.get_events(query=q, include_recurring=True)
        
        busy = False
        for event in events:
            print(f"Found conflicting event: {event.subject} at {event.start}")
            busy = True
            
        if busy:
            print("Warning: There are conflicting events in this time slot.")
            return False
        else:
            print("Time slot is clear.")
            return True

    def create_meeting(self, subject, start_time, end_time):
        """Creates the meeting event."""
        print(f"Creating meeting '{subject}'...")
        
        new_event = self.schedule.new_event()
        new_event.subject = subject
        new_event.start = start_time
        new_event.end = end_time
        new_event.location = "Online"
        
        # Save the event to the calendar
        success = new_event.save()
        
        if success:
            print(f"Successfully created event: {subject}")
            print(f"Time: {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')} - {end_time.strftime('%H:%M:%S %Z')}")
            return True
        else:
            print("Failed to create event.")
            return False

    def run(self):
        self.authenticate()
        
        start_time, end_time = self.get_ist_time()
        
        # Check availability
        is_free = self.check_availability(start_time, end_time)
        
        if not is_free:
            user_input = input("Slot is not free. Do you want to proceed anyway? (y/n): ")
            if user_input.lower() != 'y':
                print("Aborting.")
                return

        # Create the meeting
        self.create_meeting("Test", start_time, end_time)

if __name__ == "__main__":
    # You can hardcode credentials here or load from env vars
    # For security, we recommend env vars.
    CLIENT_ID = os.environ.get('OUTLOOK_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('OUTLOOK_CLIENT_SECRET')
    
    if not CLIENT_ID:
        print("Error: OUTLOOK_CLIENT_ID environment variable not set.")
        print("Please set it or edit the script to include your Client ID.")
        sys.exit(1)

    agent = OutlookMeetingScheduler(CLIENT_ID, CLIENT_SECRET)
    agent.run()
