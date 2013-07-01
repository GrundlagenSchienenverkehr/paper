import csv
import sys

#
# helpers
#
def parse_int(val, default=None):
    try:
        [ cite, val_int ] = val.strip().split(':')
        return int (val_int.strip()), cite
    except ValueError:
        return default, 'none'

def parse_float(val, default=None):
    try:
        [cite, val_float ] = val.strip().split(':')
        return float(val_float.strip()), cite
    except ValueError:
        return default, 'none'

def parse_str(val):
    return val.strip()

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

        self.description = parse_str(line[index['desc']])
        self.place = parse_str(line[index['place']])
        self.costs, self.costs_cite = parse_float(line[index['costs']])
        self.estimated_costs, self.estimated_costs_cite = parse_float(line[index['eCosts']])
        self.length, self.length_cite = parse_float(line[index['length']])
        self.station, self.station_cite = parse_int(line[index['stations']])
        self.year, self.year_cite = parse_int(line[index['year']])

    def any_costs(self):
        if self.costs:
            return self.costs, True
        else:
            return self.estimated_costs, False


    def latex_costs(self):
        if self.costs:
            return str(self.costs) + " Mio \\cite{" + self.costs_cite + "}"
        else:
            return "-"
    def latex_estimated_costs(self):
        if self.estimated_costs:
            return str(self.estimated_costs) + " Mio \\cite{" + self.estimated_costs_cite + "}"
        else:
            return "-"
    def latex_length(self):
        if self.length:
            return str(self.length) + " \\cite{" + self.length_cite + "}"
        else:
            return "-"
    def latex_year(self):
        if self.year:
            return str(self.year) + " \\cite{" + self.year_cite + "}"
        else:
            return "-"


    def latex_with_source(self):
        return "%s in %s & %s & %s & %s & %s \\\\" % (self.description, self.place, self.latex_estimated_costs(), self.latex_costs(), self.latex_length(), self.latex_year())

#
# api
#

def readCsvFile(filepath):
    data = []

    with open(filepath) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        header = next(csvreader)
        index = { header[i].strip() : i for i in range(len(header)) }

        for row in csvreader:
            data.append(Track(index, row))

    return data

def table_texify(tracks):

    header = " Strecke & geschätze Kosten & tatsächliche Kosten & Streckenlänge & Fertigstellung \\\\\n\\hline"

    table_start = "\\begin{tabular}{" + " l"*5 + " }\n"
    table_end = "\\end{tabular}"
    lines = [table_start, header]

    for t in tracks:
        lines.append(t.latex_with_source())

    lines.append(table_end)
    return "\n".join(lines)

if __name__ == "__main__":
    data = readCsvFile(sys.argv[1])
    with open(sys.argv[2],'w') as outfile:
        outfile.write(table_texify(data))
