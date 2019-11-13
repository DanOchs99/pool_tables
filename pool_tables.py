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

from os import system, path
from time import sleep
import datetime
import math
import smtplib, ssl
import json
from table import Table

def set_filename():
    ### set the filename to today
    today = datetime.datetime.now()
    filename = f"{today.month:02d}-{today.day:02d}-{today.year}"
    return filename

def email_report():
    # function to email report

    # test that a log_file exists (a table was closed today)
    if path.exists(log_file):
    # read the file contents into msg
        with open(log_file) as file_obj:
            contents = file_obj.read()
        # add an email header
        msg = f"From: {email_report_from}\nTo: {email_report_to}\nSubject: {log_file}\n\n{contents}"
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

def write_state(tables):
    out_state = []
    for table in tables:
        out_state.append(table.__dict__())
    with open(state_file, 'w') as file_obj:
        json.dump(out_state,file_obj)

def read_state():
    tables = []
    with open(state_file) as file_obj:
        in_state = json.load(file_obj)
    for d in in_state:
        table = Table.create_from_json(d)
        tables.append(table)
    return tables

### set the log file and state file names
log_file = f"{set_filename()}.txt"
state_file = f"{set_filename()}.json"

### restart code - FIX THIS WHEN WRITE STATE WORKING!
if path.exists(state_file):
    # i've already been running today - create tables from the JSON file
    with open(state_file) as file_obj:
        d = json.load(file_obj)
    tables = read_state()
else:
    # we're good to start with all tables open - will create state file for today on first table opening
    tables = []
    for i in range(12):
        table = Table(i+1)
        tables.append(table)

### email settings
smtp_server = 'localhost'
port = 1025
email_report_from = 'pool_hall@somewhere.org'
email_report_to = 'boss@somewhere.org'

### main UI loop
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
        # email the log file
        email_report()
        continue
    elif choice in ['1','2','3','4','5','6','7','8','9','10','11','12']:
        # user wants to open or close out a table
        table = tables[int(choice)-1]
        if table.status:
            # table is occupied so close it out
            msg = table.close(log_file)
            write_state(tables)
            print()
            print(f"{msg}")
            print(f"Added to file: {log_file}")
            sleep(2)
        else:
            # table is not occupied so start game
            table.open()
            write_state(tables)
        continue
    else:
        # don't understand - message user, wait 2 seconds, refresh
        print("Invalid selection.")
        sleep(2)
        continue
        
