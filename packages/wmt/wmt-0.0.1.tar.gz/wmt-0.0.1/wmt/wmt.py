#!/usr/bin/python3

import argparse
import configparser
import datetime
import csv
import os
import pprint
import time

COLUMNS_NAMES = ['name', 'start', 'end', 'duration']
DATETIME_FMT = '%d/%m/%y %H:%M.%S'

def getUserDir():
	if os.name == 'nt':
		return os.getenv('USERPROFILE')
	elif os.name == 'nt':
		return os.getenv('HOME')
	else:
		raise Exception('Not supported platform - ' + os.name)

class Wmt:
        def __init__(self, debug = False):
                self.debug_prints = debug
                self.debug('initiating wmt')
                # search and parse dotfile:
                wmt_path = os.path.join(getUserDir(), '.wmt')
                if not os.path.exists(wmt_path):
                        os.mkdir(wmt_path)
                config_path = os.path.join(wmt_path, 'config')
                if os.path.exists(config_path):
                        config = configparser.ConfigParser()
                        config.read(config_path)
                        self.db_path = config['Paths']['DataBaseFile']
                else:
                        self.db_path = os.path.join(wmt_path, 'db.csv')
                if not os.path.exists(self.db_path):
                        self.create_db()
                else:
                        self.debug('db already exist in ' + self.db_path)

        def start(self, name, offset):
                start = datetime.datetime.now()
                start += datetime.timedelta(minutes = offset)
                with open(self.db_path, 'a') as f:
                        writer = csv.DictWriter(f, fieldnames = COLUMNS_NAMES)
                        writer.writerow({'name': name, 'start': start.strftime(DATETIME_FMT)})

                print(name + ' ' + start.strftime(DATETIME_FMT))

        def end(self, offset):
                end = datetime.datetime.now()
                end += datetime.timedelta(minutes = offset)
                with open(self.db_path, 'r+') as f:
                        reader = csv.DictReader(f, fieldnames = COLUMNS_NAMES)
                        for row in reader:
                                pass
                        if row['end'] != '':
                                raise Exception('No session is running')
                        name = row['name']
                        start = datetime.datetime.strptime(row['start'], DATETIME_FMT)
                        print('total sec is ' + str((end - start).total_seconds()))
                        print('total sec/60 is ' + str((end - start).total_seconds() / 60))
                        duration = int(round((end - start).total_seconds() / 60))

                        # removing last line:
                        f.seek(0, os.SEEK_END)
                        pos = f.tell() - 2
                        while pos > 0 and f.read(1) != "\n":
                                pos -= 1
                                f.seek(pos, os.SEEK_SET)
                        pos += 1
                        if pos > 0:
                                f.seek(pos, os.SEEK_SET)
                                f.truncate()

                        writer = csv.DictWriter(f, fieldnames = COLUMNS_NAMES)
                        writer.writerow({'name': name,
                                'start': start.strftime(DATETIME_FMT), 'end': end.strftime(DATETIME_FMT),
                                'duration': duration})
                print(name + ' ' + start.strftime(DATETIME_FMT) + ' ended (' + str(duration) +' minutes)')

        def status(self):
                with open(self.db_path, 'r') as f:
                        reader = csv.DictReader(f, fieldnames = COLUMNS_NAMES,)
                        for row in reader:
                                pass
                        pprint.pprint(row)

        def create_db(self):
                self.debug('Creates new DB file in ' + self.db_path)
                with open(self.db_path, 'x') as f:
                        writer = csv.DictWriter(f, fieldnames = COLUMNS_NAMES)
                        writer.writeheader()

        def debug(self, f):
                if self.debug_prints:
                        print(f)

def printprogressbar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s        ' % (prefix, bar, percent, suffix), end='\r')

def main():
        parser = argparse.ArgumentParser(description='Find out where your time goes. Simple time-tracer CLI')
        parser.add_argument('action', choices=['start', 'end', 'status'], help='action of upstream nodes, one of add, modify, delete')
        parser.add_argument('-n', '--name', type=str, required=False, help='Name of the session')
        parser.add_argument('-t', '--time', type=int, default=0, required=False, help='Relative time in minutes to start/end the session in')
        parser.add_argument('-d', '--duration', type=int, required=False, help='Duration of the session in minutes')
        parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='store_true')
        parser.add_argument('-i', '--interactive', help='Interctive wait for session to end', action='store_true')
        parser.add_argument('-c', '--config', type=str, help='Interctive wait for session to end')
        args = parser.parse_args()
        wmt = Wmt(args.verbose)

        if args.action == "start":
                if args.name is None:
                        raise Exception('error: the following arguments are required: -n/--name')
                wmt.start(args.name, args.time)
                if args.interactive:
                        t0 = time.time()
                        elapsed = 0
                        print('Hit Ctrl+\'C\' to end this session')
                        try:
                                while args.duration is None or elapsed < (args.duration * 60):
                                        elapsed = time.time() - t0
                                        time.sleep(0.2)
                                        if args.duration is None:
                                                print('\rElapsed %s:%s     '%(int(elapsed / 60), round(elapsed % 60)), end='\r')
                                        else:
                                                printprogressbar(elapsed, args.duration * 60, prefix='', suffix='Elapsed %s:%s'%(int(elapsed / 60), round(elapsed % 60)))
                        except KeyboardInterrupt:
                                pass
                        print()
                        wmt.end(0)
                else:
                        if not args.duration is None:
                                wmt.end(args.duration)
        elif args.action == "end":
                wmt.end(args.time)
        elif args.action == "status":
                wmt.status()

if __name__ == "__main__":
        main()
