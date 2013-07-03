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
        self.tunnel_length, self.tunnel_length_cite = parse_float(line[index['tunnelkm']])
        self.bridge_length, self.bridge_length_cite = parse_float(line[index['bridgekm']])
        self.stations, self.stations_cite = parse_int(line[index['stations']])
        self.year, self.year_cite = parse_int(line[index['year']])
        self.switches, self.switches_cite = parse_int(line[index['switches']])

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

    def latex_tunnel_length(self):
        if self.tunnel_length:
            return str(self.tunnel_length) + " \\cite{" + self.tunnel_length_cite + "}"
        else:
            return "-"

    def latex_bridge_length(self):
        if self.bridge_length:
            return str(self.bridge_length) + " \\cite{" + self.bridge_length_cite + "}"
        else:
            return "-"

    def latex_year(self):
        if self.year:
            return str(self.year) + " \\cite{" + self.year_cite + "}"
        else:
            return "-"

    def latex_stations(self):
        if self.stations:
            return str(self.stations) + " \\cite{" + self.stations_cite + "}"
        else:
            return "-"

    def latex_switches(self):
        if self.switches:
            return str(self.switches) + " \\cite{" + self.switches_cite + "}"
        else:
            return "-"


    def latex_length_costs(self):
        if self.costs and self.length:
            return "%0.2f  Mio" % (self.costs / self.length)
        elif self.estimated_costs and self.length:
            return "%0.2f Mio \\footnotemark[1]" % (self.estimated_costs/ self.length)
        else:
            return "-"

    def latex_stations_costs(self):
        if self.costs and self.stations:
            return "%0.2f Mio" % (self.costs/ self.stations)
        elif self.estimated_costs and self.stations:
            return "%0.2f Mio \\footnotemark[2]" % (self.estimated_costs/ self.stations)
        else:
            return "-"

    def latex_results_track(self):
        return "%s in %s & %s & %s & %s & %s & %s & %s\\\\" % (
            self.description, self.place, self.latex_estimated_costs(),
            self.latex_costs(), self.latex_length(), self.latex_switches(),
            self.latex_stations(), self.latex_year())

    def latex_analysis_track(self):
        return "%s in %s & %s & %s \\\\" % (
            self.description, self.place,
            self.latex_length_costs(), self.latex_stations_costs() )

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


def render_table(tracks, fields, methodname):

    header = " & ".join(fields) + " \\\\\n\\hline"
    table_start = "\\begin{tabular}{" + " l" * len(fields)  + " }\n"
    table_end = "\\end{tabular}"

    lines = [table_start, header]

    for t in tracks:
        handler = getattr(t,"latex_%s_track" % ( methodname ))
        lines.append(handler())

    lines.append(table_end)
    return "\n".join(lines)

def result_table(tracks):
    fields = ["Strecke", "geschätze Kosten", "tatsächliche Kosten", "Streckenlänge in km", "Weichen", "Haltstellen", "Fertigstellung"]
    return render_table(tracks, fields, "results")


def analysis_table(tracks):
    fields = ["Strecke", "Kosten pro km", "Kosten pro Halt"]
    return render_table(tracks, fields, "analysis") + "\\footnotetext[2]{berechnet mit geschätzten Kosten}"


if __name__ == "__main__":
    data = readCsvFile(sys.argv[1])
    with open(sys.argv[2],'w') as outfile:

        if sys.argv[3] == "results":
            outfile.write(result_table(data))
        else:
            outfile.write(analysis_table(data))
