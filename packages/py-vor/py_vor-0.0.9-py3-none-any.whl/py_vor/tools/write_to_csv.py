# -*- coding: utf-8 -*-

"""write_to_csv
Writes a nested list to a CSV file.
Author: ksco92
"""

import csv

##########################################
##########################################
##########################################
##########################################


def write_to_csv(destination_file, content, delim=','):

    """Writes a nested list to a CSV file."""

    with open(destination_file, 'w', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f, delimiter=delim)
        writer.writerows(content)
        f.close()
