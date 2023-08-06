import csv


def read_csv(fp, header=None):
    table = []
    with open(fp, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        if not header:
            header = next(csv_reader)
        for row in csv_reader:
            new_row = {}
            for cell, col_name in zip(row, header):
                new_row[col_name] = cell
            table.append(new_row)
    return table
