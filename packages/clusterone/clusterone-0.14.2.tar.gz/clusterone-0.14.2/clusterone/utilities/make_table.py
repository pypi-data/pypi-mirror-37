from clusterone.utils import render_table as render_table


def make_table(table_data, header, max_length=70, render_table_func=render_table):
    """Merge table_data and header and prepare to print"""

    table_data = list(table_data)
    for row in table_data:
        assert len(header) == len(row)

    header_and_rows = [header] + table_data
    table = render_table_func(header_and_rows, max_length).table
    return table
