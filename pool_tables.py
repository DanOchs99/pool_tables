# Pool Table Management Application
#
# Dan Ochs
# 11/12/19
#
# user is the UofH Games Room administrator
# you should be able to see all the tables (12)
# each table should show OCCUPIED or NOT OCCUPIED
# if OCCUPIED show start time & number of minutes played (if > 60 show hours too)
# can only give out tables NOT OCCUPIED. i.e. if Table 8 is occupied and you
#     try to give it out the app will print a message saying "Table 8 is currently occupied"
# whenever close a table write an entry to log (text or json) file. File should be named
#     11-22-2017.txt or 11-22-2017.json. Entry should consist of the following information:
#     pool table number, start date time, end date time, total time played, cost
#
# hard mode - associate dollar amount for time played on the pool table - ($30 / hour)
# harder mode - write unit tests for your application
# extremely hard mode - add the ability to email the final report (file) to an email address

from os import system
from time import sleep
import datetime
import math
import smtplib, ssl

log_file = ''
### email settings
smtp_server = 'localhost'
port = 1025
email_report_from = 'pool_hall@somewhere.org'
email_report_to = 'boss@somewhere.org'

class Table:
    def __init__(self,num):
        self.num = num   # table number
        self.status = False   # True = Occupied, False = Not Occupied
        self.start = None   # time play started    
    def open(self):
        self.status = True
        self.start = datetime.datetime.now()
    def close(self):
        # calc time played, cost
        price = 30.0     # cost in $/hour
        end = datetime.datetime.now()
        time_played = end - self.start
        # charge based on whole minutes played
        cost = math.floor(time_played.total_seconds() / 60.0) * (price / 60.0)    
        # append an entry to log file
        self._write_log_entry(end, time_played, cost)
        # fix table status
        self.status = False
        self.start = None

    def _write_log_entry(self, end, time_played, cost):
        global log_file
        
        # set filename and build log entry
        log_file = f"{end.month:02d}-{end.day:02d}-{end.year}.txt"

        # format start and end times
        start_str = self.start.strftime("%I:%M:%S %p")
        end_str = end.strftime("%I:%M:%S %p")

        # format duration
        hours_played = math.floor(time_played.total_seconds() / (60.0 * 60.0))
        min_played = math.floor((time_played.total_seconds()-hours_played * 60 * 60) / 60.0)
        duration_str = f"{hours_played:02d}:{min_played:02d}"

        log_out = f"Table: {self.num} Start: {start_str} End: {end_str} Duration: {duration_str} Cost: ${cost:.2f}"
        
        print()
        print(f"{log_out}")
        print(f"Added to file: {log_file}")
        sleep(2)

        # append an entry to today's log file
        with open(log_file,'a') as log_file_handle:
            log_file_handle.write(f"{log_out}\n")

def email_report():
    # function to email report
    # test that log_file got initilized (a table was closed)
    if len(log_file) > 0:
        # log_file exists, read in the log file
        with open(log_file) as log_file_handle:
            log_file_content = log_file_handle.readlines()
        msg = ""
        for line in log_file_content:
            msg = msg + line
        msg = msg + '\n'
        # add an email header
        msg = f"From: {email_report_from}\nTo: {email_report_to}\nSubject: {log_file}\n\n" + msg
        # connect to local server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.sendmail(email_report_from, email_report_to, msg)
        except Exception as e:
            # print any error messages to stdout
            print(e)
        finally:
            try:
                server.quit()
            except UnboundLocalError:
                # never got connected so no need to shut it down
                pass

        print(f"Emailed today's report to {email_report_to}")
        sleep(2)
    else:
        print("No log file. Please close a table first.")
        sleep(2)

# list of tables to manage
tables = []
for i in range(12):
    table = Table(i+1)
    tables.append(table)

# main UI loop
while True:
    system('clear')
    print ("Pool Table Management")
    print()
    # display tables status
    current_time = datetime.datetime.today()
    current_time_str = current_time.strftime("%A, %d. %B %Y %I:%M:%S %p")
    print(f"Status as of {current_time_str} - ")
    for table in tables:
        if table.status:
            ### --- start of test code section
            ### test code section for hours vs. minutes duration display
            ### force start time to be 2:20 before current time; test assumes current minutes > 20 !!
            #curr_time = datetime.datetime.now()
            #table.start = datetime.datetime(2019, 11, 12, hour = curr_time.hour - 2, minute = curr_time.minute - 20, second = 0)
            ### --- end of test code section ---
            start_time_str = table.start.strftime("%I:%M:%S %p")
            time_played = datetime.datetime.now() - table.start
            min_played = math.floor(time_played.total_seconds() / 60.0)
            if min_played > 60:
                hours_played = math.floor(time_played.total_seconds() / (60.0 * 60.0))
                min_played = math.floor((time_played.total_seconds()-hours_played * 60 * 60) / 60.0)
                print(f"Pool table {table.num:2d}: OCCUPIED   (Started - {start_time_str})   (Time on table - {hours_played}:{min_played})")
            else:
                print(f"Pool table {table.num:2d}: OCCUPIED   (Started - {start_time_str})   (Time on table - {min_played} min)")
        else:
            print(f"Pool table {table.num:2d}: NOT OCCUPIED")    
    # display menu
    print()
    print("Enter table number (1-12) to open or close out a table.")
    choice = input("Enter 'r' to refresh list/menu; 'e' to email today's report; 'q' to quit: ")
    if choice == 'q':
        # quit application
        is_all_empty = True
        for table in tables:
            if table.status:
                is_all_empty = False
        if is_all_empty:
            # all the tables are closed out so quit immediately
            break
        else:
            safety_choice = input("There are open tables! Are you *sure* you want to quit? ('Q' to quit, anything else to continue): ")
            if safety_choice == 'Q':
                break
            else:
                continue
    elif choice == 'r':
        # refresh list
        continue
    elif choice == 'e':
        # email report
        email_report()
        continue
    elif choice in ['1','2','3','4','5','6','7','8','9','10','11','12']:
        # user wants to open or close out a table
        table = tables[int(choice)-1]
        if table.status:
            # table is open so close it out
            table.close()
        else:
            # table is not occupied so start game
            table.open()
        continue
    else:
        # don't understand - message user, wait 2 seconds, refresh
        print("Invalid selection.")
        sleep(2)
        continue
        
