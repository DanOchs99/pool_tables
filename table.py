# definition of Table class
#
# Dan Ochs
# 11/12/19

import datetime
import math

class Table:
    def __init__(self,num):
        self.num = num   # table number
        self.status = False   # True = Occupied, False = Not Occupied
        self.start = None   # time play started
    
    def __dict__(self):
        # override default to handle possible datetime in a table
        d = {}
        d['num'] = self.num
        d['status'] = self.status
        if self.start is None:
            d['start'] = None
        else:
            d['start'] = [self.start.year, self.start.month, self.start.day,
                          self.start.hour, self.start.minute, self.start.second,
                          self.start.microsecond]            
        return d

    @staticmethod
    def create_from_json(d):
        table = Table(d['num'])
        table.status = d['status']
        if d['start'] is None:
            table.start = None
        else:
            table.start = datetime.datetime(year = d['start'][0], month = d['start'][1], day = d['start'][2],
                                   hour = d['start'][3], minute = d['start'][4], second = d['start'][5], microsecond = d['start'][6])
        return table

    def open(self):
        self.status = True
        self.start = datetime.datetime.now()

    def close(self, log_file):
        # calc time played, cost
        price = 30.0     # cost in $/hour
        end = datetime.datetime.now()
        time_played = end - self.start
        # charge based on whole minutes played
        cost = math.floor(time_played.total_seconds() / 60.0) * (price / 60.0)    
        # append an entry to log file
        log_out = self._write_log_entry(end, time_played, cost, log_file)
        # fix table status
        self.status = False
        self.start = None
        return log_out    # pass back the log entry so can show user

    def _write_log_entry(self, end, time_played, cost, log_file):
        # format start and end times
        start_str = self.start.strftime("%I:%M:%S %p")
        end_str = end.strftime("%I:%M:%S %p")
        # format duration
        hours_played = math.floor(time_played.total_seconds() / (60.0 * 60.0))
        min_played = math.floor((time_played.total_seconds()-hours_played * 60 * 60) / 60.0)
        duration_str = f"{hours_played:02d}:{min_played:02d}"
        # create log entry
        log_out = f"Table: {self.num} Start: {start_str} End: {end_str} Duration: {duration_str} Cost: ${cost:.2f}"
        # append an entry to today's log file
        with open(log_file,'a') as log_file_handle:
            log_file_handle.write(f"{log_out}\n")
        return log_out    # pass back the log entry