import csv
import sys

#
# helpers
#
def safe_int(val, default=None):
    try:
        return int (val)
    except ValueError:
        return default

def safe_float(val, default=None):
    try:
        return float(val)
    except ValueError:
        return default

#
# data types
#
class Track:

    tram = False
    subway = False

    def __init__(self, index, line):
        if line[index['type']] == 'Tram':
            self.tram = True
        else:
            self.subway = True

        self.description = line[index['desc']]
        self.place = line[index['place']]
        self.costs = safe_float(line[index['costs']])
        self.estimated_costs = safe_float(line[index['estCosts']])
        self.length = safe_float(line[index['length']])
        self.station = safe_int(line[index['stations']])
        self.year = safe_int(line[index['year']])

    def any_costs(self):
        if self.costs:
            return self.costs, True
        else:
            return self.estimated_costs, False



#
# api
#

def readCsvFile(filepath):
    data = []

    with open(filepath) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        header = next(csvreader)
        index = { header[i] : i for i in range(len(header)) }

        for row in csvreader:
            data.append(Track(index, row))

    return data

def table_texify(tracks):


    header = " Strecke & geschätze Kosten & tatsächliche Kosten & Streckenlänge & Fertigstellung \\\\\n\\hline"
    row_template = "  %s in %s & %s & %s & %s & %d \\\\\n"

    table_start = "\\begin{tabular}{" + " l"*5 + " }\n"
    table_end = "\\end{tabular}"
    lines = [table_start, header]

    for t in tracks:
        lines.append(row_template %
                     ( t.description,
                       t.place,
                       str(t.costs) + " Mio" if t.costs else "-",
                       str(t.estimated_costs) + " Mio" if t.estimated_costs else "-",
                       str(t.length),
                       t.year ))

    lines.append(table_end)
    return "\n".join(lines)

if __name__=="__main__":
    data = readCsvFile(sys.argv[1])
    print(table_texify(data))
