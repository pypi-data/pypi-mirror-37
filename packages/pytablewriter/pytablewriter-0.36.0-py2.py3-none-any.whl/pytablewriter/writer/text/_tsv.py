# encoding: utf-8

from __future__ import absolute_import, unicode_literals

from ._csv import CsvTableWriter


class TsvTableWriter(CsvTableWriter):
    """
    A table writer class for tab separated values (TSV) format.

    :Example:
        :ref:`example-tsv-table-writer`
    """

    @property
    def format_name(self):
        return "tsv"

    def __init__(self):
        super(TsvTableWriter, self).__init__()

        self.column_delimiter = "\t"
