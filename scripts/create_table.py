# -*- coding: utf-8 -*-
import csv
import sys
import locale
from locale import str, format_string
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

def dev(avarage, val):
    diff = val - avarage
    dev = diff / avarage
    if dev > 0:
        sign = "+"
    elif dev < 0:
        sign = "\\textminus"
    else:
       sign = "\\textpm"
    return format_string("%s %d \\%%", (sign, int(abs(dev)*100)))

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
            if self.costs > 1000:
                return str(self.costs/1000) + " Mrd \\cite{" + self.costs_cite + "}"
            else:
                return str(self.costs) + " Mio \\cite{" + self.costs_cite + "}"
        else:
            return "-"

    def latex_estimated_costs(self):
        if self.estimated_costs:
            if self.estimated_costs > 1000:
                return str(self.estimated_costs/1000) + " Mrd \\cite{" + self.estimated_costs_cite + "}"
            else:
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


    def latex_length_costs(self, avarage):
        if self.costs and self.length:
            return format_string("%0.2f  Mio & %s", (self.costs / self.length, dev(avarage.length_costs,self.costs/ self.length) ))
        elif self.estimated_costs and self.length:
            return format_string("%0.2f Mio \\footnotemark[2] & %s", (self.estimated_costs/ self.length, dev(avarage.length_costs,self.estimated_costs/ self.length) ))
        else:
            return "-"

    def latex_stations_costs(self, avarage):
        if self.costs and self.stations:
            return format_string("%0.2f Mio & %s ", (self.costs/ self.stations, dev(avarage.stations_costs,self.costs/ self.stations)))
        elif self.estimated_costs and self.stations:
            return format_string("%0.2f Mio \\footnotemark[2] & %s", (self.estimated_costs/ self.stations,  dev(avarage.stations_costs,self.estimated_costs/ self.stations)))
        else:
            return "-"

    def latex_results_track(self, last_place):
        template = "%s: %s & %s & %s & %s & %s & %s & %s & %s & %s\\\\"
        if last_place == self.place:
            template = "{\color{white}%s: }%s & %s & %s & %s & %s & %s & %s & %s & %s\\\\"

        return template % (
            self.place, self.description, self.latex_estimated_costs(),
            self.latex_costs(), self.latex_length(), self.latex_tunnel_length(), self.latex_bridge_length(),
            self.latex_switches(), self.latex_stations(), self.latex_year())

    def latex_analysis_track(self, avarage):
        return "%s: %s & %s & %s \\\\" % (
            self.place, self.description,
            self.latex_length_costs(avarage), self.latex_stations_costs(avarage) )


    def get_costs_length(self) :
        return ( self.costs or self.estimated_costs ) / self.length


    def get_length_vector(self) :
        if self.length:
            tl = 0
            bl = 0

            if self.tunnel_length:
                tl = self.tunnel_length

            if self.bridge_length:
                bl = self.bridge_length

            l =  self.length - (tl)

            return [ tl, self.length - (bl +  tl)]


    def get_costs(self):
        if self.costs:
            return self.costs
        if self.estimated_costs:
            return self.estimated_costs

class Avarage:

    def __init__(self, tracks):

        stations = 0
        stations_costs = 0

        length = 0
        length_costs = 0

        for t in tracks:


            if ( t.costs or t.estimated_costs ) and t.length:
                length_costs += t.costs or t.estimated_costs
                length += t.length

            if ( t.costs or t.estimated_costs) and t.stations:
                stations_costs += t.costs or t.estimated_costs
                stations += t.stations


        self.length_costs = length_costs / length
        self.stations_costs = stations_costs / stations


    def latex_analysis_track(self, _):
        return format_string("\\textit{Durchschnitt} & %0.2f Mio & \\textpm 0 & %0.2f Mio & \\textpm 0 \\\\", (self.length_costs, self.stations_costs))


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


def analysis_table(tracks):

    fields = ["Strecke", "\multicolumn{2}{c}{Kosten pro km}", "\multicolumn{2}{c}{Kosten pro Halt}"]
    av = Avarage(tracks)

    header = " & ".join(fields) + " \\\\\n"
    subheader = " & absolut & relativ & absolut & relativ \\\\\n\\hline"
    table_start = "\\begin{tabular}{p{15em}" + " l" * (len(fields) +1  )  + " }\n"
    table_end = "\\end{tabular}"

    lines = [table_start, header, subheader ]

    tracks.insert(0, av)

    for t in tracks:
        lines.append(t.latex_analysis_track(av))

    lines.append(table_end)
    lines.append("\\footnotetext[2]{berechnet mit geschätzten Kosten}")
    return "\n".join(lines)

def result_table(tracks):
    fields = ["Strecke", "\multicolumn{2}{c}{Kosten in \euro}", " \multicolumn{3}{c}{Streckenlänge in km}", "Weichen", "Haltstellen", "Fertigst."]
    header = " & ".join(fields) + " \\\\\n" + "& geschätzt & tatsächlich & gesamt & Tunnel & Brücken & & & \\\\\n\hline\n"
    table_start = "\\begin{tabular}{" + " l" * 4 + "l" * 2 + "l" * 3  + " }\n"
    table_end = "\\end{tabular}"

    lines = [table_start, header]

    subway = False
    last_place = None
    for t in tracks:
        if t.subway and not subway:
            subway = True
            lines.append("[.2em] \\hline \\\\[-.8em]")

        lines.append(t.latex_results_track(last_place))
        # hide multiple cities:
        #last_place = t.place

    lines.append(table_end)
    return "\n".join(lines)





if __name__ == "__main__":
    data = readCsvFile(sys.argv[1])

    locale.setlocale(locale.LC_NUMERIC, 'de_DE.utf8')

    files = sys.argv[2:]

    with open(files[0],'w') as outfile:
        outfile.write(result_table(data))

    with open(files[1],'w') as outfile:
        trams = list(filter(lambda x: x.tram, data))
        outfile.write(analysis_table(trams))

    with open(files[2],'w') as outfile:
        subs = list(filter(lambda x: x.subway, data))
        outfile.write(analysis_table(subs))
