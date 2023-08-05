from __future__ import print_function
import pandas as pd
import numpy as np
import os
import time
import sys
from os.path import expanduser, join, exists
from os import remove
from journal_club.sound import *
from journal_club.jc_algorithm import algorithm
from journal_club import where_jc
from journal_club.__version__ import __version__

here = os.path.dirname(__file__)
countdown_mp3 = os.path.join(where_jc, 'countdown.wav')


def _input(x):
    try:
        return raw_input(x)
    except NameError:
        return input(x)


def save(r, record_csv, verbose=False):
    r.to_csv(record_csv)


def get_probs(record, attended=None):
    r = record.copy()
    p = algorithm(r, attended)
    return p


def validate_file(function):
    def inner(args, *a, **k):
        if not exists(args.record_csv):
            raise IOError("Record csv {} does not exist. Run `choose` at least once!".format(args.record_csv))
        
        record = get_record(args)
        cols = ['turn', 'attendence']
        missing = [i for i in cols if i not in record.columns]
        if missing:
            raise IOError("{} is not a valid record_csv file. {} columns are missing".format(args.record_csv, missing))
        return function(args, *a, **k)
    return inner


def create_new(args):
    names = list(set(args.attendences))
    print("Initialising with {}".format(','.join(names)))
    t = pd.DataFrame([[0, ','.join(names), '']], columns=['i', 'attendence', 'turn']).set_index('i')
    if os.path.exists(args.record_csv):
        yn = _input('overwrite previous records? (press enter to continue)')
        save(t, args.record_csv)
        print("overwriting records at {}".format(args.record_csv))
    else:
        save(t, args.record_csv)
        print("Created new record at {}".format(args.record_csv))


def import_legacy(record, args):
    last_picked = record.loc[record['meetings_since_last_turn'] == 0, 'name']
    print("Upgrading database...")
    record = create_new(args)
    record.loc[0] = [','.join(args.attendences), last_picked]
    return record


def get_record(args):
    try:
        record = pd.read_csv(args.record_csv).set_index('i')
        if 'name' in record.columns:
            record = import_legacy(record, args)
    except IOError:
        create_new(args)
        record = get_record(args)
    return record


def pretty_choose(record, attended, duration=5, freq=10):
    probs = get_probs(record, attended).iloc[-1]
    choices = np.random.choice(probs.index.values, p=probs.values, size=duration*freq)
    max_len = max(map(len, probs.index.values))
    times = np.arange(len(choices))**3.
    times /= times.sum()
    times *= duration

    template = '\rchoosing the next leader: {}'
    play_sound(countdown_mp3, 32-duration, block=False)
    previous = 0
    for i, (t, name) in enumerate(zip(times, choices)):
        time.sleep(t)
        if i == len(choices) - 1:
            template = "\r{}... your number's up"
        txt = template.format(name)
        sys.stdout.write(txt)
        gap = (previous - len(txt))
        if gap > 0:
            sys.stdout.write(' ' * gap)
        sys.stdout.flush()
        previous = len(txt)
    print()
    return name


def show_probabilities(probabilities):
    probs = probabilities.iloc[-1].sort_values(ascending=False)
    for i, (name, r) in enumerate(probs.iteritems()):
        print('{}. {} = {:.1%}'.format(i+1, name, r))


def choose(args):
    attend = args.attendences
    record = get_record(args)
    record.loc[len(record)] = [','.join(attend), '']
    probs = get_probs(record, attend)

    show_probabilities(probs)
    choice = pretty_choose(record, attend)

    record.loc[len(record)-1, 'turn'] = choice

    if not args.dry_run:
        save(record, args.record_csv)
    else:
        print("===DRYRUN===")
        show_probabilities(probs)
    play_text("{}, your number's up".format(choice))


@validate_file
def show(args):
    print("Accessing database at {}".format(args.record_csv))
    record = get_record(args)
    probs = get_probs(record)
    included = args.include if args.include else probs.columns
    excluded = args.exclude if args.exclude else []
    names = list(set(included) - set(excluded))
    show_probabilities(probs[names])


@validate_file
def validate(args):
    print("{} is a valid journal_club record_csv file.".format(args.record_csv))


@validate_file
def reset(args):
    input("Warning! Removing database file! Press ENTER to continue/ctrl+c to cancel ")
    remove(args.record_csv)
    print("File removed...")


def test(args):
    play_text('This is a test')
    duration = 3
    play_sound(countdown_mp3, 32-duration, block=False)
    time.sleep(duration)
    print("Test finished")


def main():
    import argparse
    parser = argparse.ArgumentParser('jc')
    subparsers = parser.add_subparsers()

    home = expanduser("~")
    default_location = os.path.join(home, 'jc_record.csv')
    parser.add_argument('--record_csv', default=default_location, help='Record file location default={}'.format(default_location))
    parser.add_argument('--verbose', action='store_true', help='show all messages')
    parser.add_argument('--debug', help='Shows error messages, tracebacks and exceptions. Not normally needed', action="store_true")

    show_parser = subparsers.add_parser('show', help='Shows the current record state')
    show_parser.add_argument('--include', nargs='+', default=[], help='The people to be included')
    show_parser.add_argument('--exclude', nargs='+', default=[], help='The people to be excluded')
    show_parser.set_defaults(func=show)

    version_parser = subparsers.add_parser('version', help='Shows the current version and exits')
    version_parser.set_defaults(func=lambda x: print(__version__))

    choose_parser = subparsers.add_parser('choose', help='Run the choosertron and pick a person from the given list (attendences). '\
                                                          'Creates database if needed')
    choose_parser.add_argument('attendences', nargs='+', help='The people that are in attendence')
    choose_parser.add_argument('--dry-run', action='store_true', help="Don't save the result")
    choose_parser.set_defaults(func=choose)

    subparsers.add_parser('reset', help='Deletes the record file. Runs `rm RECORD_CSV`').set_defaults(func=reset)
    subparsers.add_parser('validate', help='Validates the record file.').set_defaults(func=validate)
    subparsers.add_parser('soundtest', help='tests the sound playback').set_defaults(func=test)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        if args.debug:
            args.func(args)
        else:
            try:
                args.func(args)
            except Exception as e:
                print("Improper usage of `jc'. Look at the help")
                print("Error message reads: {}".format(str(e)))
                parser.print_help()
                raise e
    else:
        parser.print_help()


if __name__ == '__main__':
    main()