# TODO: Test this
import itertools
from abc import ABCMeta, abstractmethod

from clusterone.business_logic.command import Command
from clusterone.utilities import make_table

class ListCommand(Command):

    __metaclass__ = ABCMeta
    table_header = None
    enumerate = None
    entity_name = None

    @staticmethod
    @abstractmethod
    def _entity_to_row(entity_data):
        raise NotImplementedError()

    @abstractmethod
    def _gather_entity_data(self):
        raise NotImplementedError()

    def __init__(self, client, make_table_fn=make_table):
        if not self.table_header:
            raise TypeError("'table_header' class field must be set on child classes")

        if not self.entity_name:
            raise TypeError("'entity_name' class field must be set on child classes")

        if self.enumerate is None:
            raise TypeError("'enumerate' class field must be set on child classes")

        self.client = client

        self._warnings = set()
        self._data = {}
        self._table_header = self.table_header

        # dependencies
        self.make_table_fn = make_table_fn

    def execute(self):
        self._data = self._gather_entity_data()

        if self._data:
            output = self._build_table(self._data)
        else:  # empty notebooks array
            output = "You don't seem to have any {entity_name}s yet. Try 'just create {entity_name}' to make one.".format(entity_name=self.entity_name)

        return {
            "warnings": self._warnings,
            "data": self._data,
            "output": output,
        }

    def _build_table(self, entities_data):
        raw_table_data = map(self._entity_to_row, entities_data)
        processed_table_data = self._process_table_data(raw_table_data)
        return self.make_table_fn(processed_table_data, header=self._table_header)

    def _process_table_data(self, table_data):
        if self.enumerate:
            self._table_header = ("#",) + self._table_header
            processed_table_data = self._enumerate_table_data(table_data)
        else:
            processed_table_data = table_data

        return processed_table_data

    @staticmethod
    def _enumerate_table_data(table_data):
        return ((str(i),) + tuple(row_element) for i, row_element in zip(itertools.count(start=1), table_data))

