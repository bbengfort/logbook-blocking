try:
    import unicodecsv as csv
except ImportError:
    import csv

from collections import namedtuple
from datetime import datetime

## Named Tuples for analysis.
Entity = namedtuple('Entity', 'name, email')
Action = namedtuple('Action', 'action, date')
Detail = namedtuple('Detail', 'detail')
Triple = namedtuple('Triple', 'entity, action, detail')

## Date format for date conversion
dtfmt  = "%m/%d/%Y"

class LogReader(object):
    """
    Reads a DDL activity log file and yields SPO triples.
    """

    def __init__(self, path, exclude=None):
        """
        Pass in a list of actions to exclude.
        """
        self.path = path
        self.exclude = frozenset(exclude)

    def parse_row(self, row):
        """
        Yields an SPO from an activity log and parses the various fields.

        Required fieldnames:
        Entity: FullName, Email
        Action: Action, ActionDate (parses mm/dd/yyyy date strings)
        Detail: Detail
        """
        entity = Entity(row['FullName'], row['Email'])
        action = Action(row['Action'], datetime.strptime(row['ActionDate'], dtfmt).date())
        detail = Detail(row['Detail'])
        return Triple(entity, action, detail)

    def __iter__(self):
        with open(self.path, 'rU') as f:
            reader = csv.DictReader(f)

            for row in reader:
                triple = self.parse_row(row)
                if self.exclude and triple.action.action in self.exclude:
                    continue
                yield triple

    def __len__(self):
        return sum(1 for item in self)

if __name__ == '__main__':
    import os
    fixture = os.path.join(os.path.dirname(__file__), "..", "fixtures", "activity.csv")
    for spo in LogReader(fixture):
        print spo
