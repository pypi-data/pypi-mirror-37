
from collections import Counter
from sys import stdout

from .format.read import filtered_records, filtered_tokens
from .format.records import no_bad_values, fix_degrees, append_units, no_unknown_fields, unique_names, join_values, \
    to_hex, no_filter
from .profile.types import Date
from ..command.args import MESSAGES, RECORDS, FIELDS, CSV, \
    TABLES
from ..lib.io import terminal_width
from ..lib.utils import unique


def summarize(log, format, fit_path, all_fields=False, all_messages=False, after=0, limit=-1,
              records=None, warn=False, profile_path=None):
    if format == MESSAGES:
        summarize_messages(log, fit_path,
                           after=after, limit=limit, warn=warn, profile_path=profile_path)
    elif format == FIELDS:
        summarize_fields(log, fit_path,
                         after=after, limit=limit, warn=warn, profile_path=profile_path)
    elif format == RECORDS:
        summarize_records(log, fit_path,
                         all_fields=all_fields, all_messages=all_messages,
                         after=after, limit=limit, records=records, warn=warn, profile_path=profile_path)
    elif format == TABLES:
        summarize_tables(log, fit_path,
                         all_fields=all_fields, all_messages=all_messages,
                         after=after, limit=limit, records=records, warn=warn, profile_path=profile_path)
    elif format == CSV:
        summarize_csv(log, fit_path,
                      after=after, limit=limit, warn=warn, profile_path=profile_path)
    else:
        raise Exception('Bad format: %s' % format)


def summarize_messages(log, fit_path, after=0, limit=-1, warn=False, profile_path=None):
    data, types, messages, tokens = \
        filtered_tokens(log, fit_path, after=after, limit=limit, warn=warn, profile_path=profile_path)
    for index, offset, token in tokens:
        print('%03d %05d %s' % (index, offset, token))


def summarize_fields(log, fit_path, after=0, limit=-1, warn=False, profile_path=None):
    data, types, messages, tokens = \
        filtered_tokens(log, fit_path, after=after, limit=limit, warn=warn, profile_path=profile_path)
    for index, offset, token in tokens:
        print('%03d %05d %s' % (index, offset, token))
        for line in token.describe_fields(types):
            print('  %s' % line)


def summarize_records(log, fit_path, all_fields=False, all_messages=False, after=0, limit=-1, records=None,
                      warn=False, profile_path=None):
    data, types, messages, records = \
        filtered_records(log, fit_path, after=after, limit=limit, records=records, warn=warn,
                         profile_path=profile_path)
    records = list(records)
    width = terminal_width()
    print()
    pprint_as_dicts(records, all_fields, all_messages, width=width)


def summarize_tables(log, fit_path, all_fields=False, all_messages=False, after=0, limit=-1, records=None,
                     warn=False, profile_path=None):
    data, types, messages, records = \
        filtered_records(log, fit_path, after=after, limit=limit, records=records, warn=warn,
                         profile_path=profile_path)
    records = list(records)
    counts = Counter(record.identity for record in records)
    small, large = partition(records, counts)
    width = terminal_width()
    print()
    pprint_as_dicts(small, all_fields, all_messages, width=width)
    pprint_as_tuples(large, all_fields, all_messages, width=width)


def summarize_csv(log, fit_path, after=0, limit=-1 ,profile_path=None, warn=False, out=stdout):
    data, types, messages, tokens = \
        filtered_tokens(log, fit_path, after=after, limit=limit, warn=warn, profile_path=profile_path)
    for index, offset, token in tokens:
        if hasattr(token, 'describe_csv'):
            print(','.join(str(component) for component in token.describe_csv()), file=out)


def partition(records, counts, threshold=3):
    small, large = [], []
    for record in records:
        if counts[record.identity] <= threshold:
            small.append(record)
        else:
            large.append(record)
    return small, large


def pprint_as_dicts(records, all_fields, all_messages, width=80):
    for record in records:
        if all_messages or record.is_known():
            record = record.as_dict(join_values, append_units, to_hex, fix_degrees,
                                    no_filter if all_fields else no_unknown_fields,
                                    no_bad_values)
            print(record.identity)
            pprint_with_tabs(('%s: %s' % (name, value) for name, value in sorted(record.data.items())),
                             width=width)
            print()


def sort_names(data):
    return sorted(list(data), key=lambda x: ' ' if x[0] == 'timestamp' else x[0])


def pprint_as_tuples(records, all_fields, all_messages, width=80):
    records = [record.force(sort_names, unique_names,
                            timestamp=([Date.convert(record.timestamp)], 's'))
               for record in records]
    titles = [record.as_names(no_filter if all_fields else no_unknown_fields)
              for record in unique(records, key=lambda x: x.identity)
              if all_messages or record.is_known()]
    for title in titles:
        pprint_series(title,
                      [record.as_values(join_values, append_units, to_hex, fix_degrees,
                                        no_filter if all_fields else no_unknown_fields)
                       for record in records
                       if record.identity == title.identity],
                      width=width)


def measure_lengths(records, lengths=None, separator=',', keep_bad=False):
    for record in records:
        if lengths is None:
            lengths = [(len(datum) + (len(separator) if i+1 < len(record.data) else 0)) if datum else 0
                       for i, datum in enumerate(record.data)]
        else:
            for i, datum in enumerate(record.data):
                if datum and (lengths[i] or not keep_bad):
                    lengths[i] = max(lengths[i], len(datum) + (len(separator) if i+1 < len(record.data) else 0))
    return lengths


def pad_to_lengths(record, lengths, separator=',', bad='-'):
    for i, datum in enumerate(record.data):
        if lengths[i]:
            if datum:
                yield (datum + (separator if i+1 < len(lengths) else '')).ljust(lengths[i])
            else:
                yield bad.ljust(lengths[i])


def pprint_series(title, records, width=80):
    print(title.identity)
    lengths = measure_lengths([title], keep_bad=True, lengths=measure_lengths(records))
    pprint_with_tabs(pad_to_lengths(title, lengths), first_indent=2, indent=4, separator='', width=width)
    for record in records:
        pprint_with_tabs(pad_to_lengths(record, lengths), first_indent=2, indent=4, separator='', width=width)
    print()


def pprint_with_tabs(data, first_indent=None, indent=2, tab=4, width=80, min_space=2, separator=','):
    if first_indent is None:
        first_indent = indent
    min_space -= 1
    line = ' ' * first_indent
    first = True
    for datum in data:
        if not first:
            line += separator
        l_old = len(line)
        if l_old > indent:
            l_new = (1 + (l_old - indent + min_space) // tab) * tab + indent
            # equality here leaves an attractive space at end of line
            if l_new + len(datum) >= width:
                print(line)
                line = ' ' * indent + datum
            else:
                line += ' ' * (l_new - l_old) + datum
        else:
            line += datum
        first = False
    if len(line) > indent:
        print(line)
