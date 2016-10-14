__author__ = 'Glenn Abastillas'

import re, time

class Spreadsheet(object):

    def __init__(self, f = None):
        self.spreadsheet_file = f
        self.spreadsheet = []
        self.loaded = False
        self.transposed = False

    def get(self):
        return self.spreadsheet_file

    def load(self, f = None):
        """
            Opens file specified in "f" variable. Stores the text in self.spreadsheet. Closes file opened in "f".
        """
        if f is None:
            f = self.spreadsheet_file

        opened_file = open(f)
        self.spreadsheet = [line.split(",") for line in opened_file.read().split("\r")]
        opened_file.close()

        self.loaded = True
        #print self.spreadsheet[0]

    def add_data(self, data = None):
        if data is None:
            pass
        else:
            if self.transposed == True:
                self.transpose()
            
            if len(data) == 1:
                self.spreadsheet += [data] + [""] * (len(self.spreadsheet[0])-1)
            else:
                self.spreadsheet += [data]

    def get_column(self, col = 0, header = "author", unique = False):
        """
            Returns column as specified by the header
        """

        columns = []

        for row in self.spreadsheet:
            if row[col].lower() == header:
                pass
            else:
                if row[col][0] == "":
                    columns.append(row[col][1:])
                else:
                    columns.append(row[col])

        if unique == True:
            return list(set(columns))
        else:
            return columns

    def create_masked_values(self, col = 0, new_term = "U"):
        values = self.get_column(col = col, unique = True)
        v_len  = len(str(len(values)))
        new_values = [new_term + str(values.index(value)).zfill(v_len) for value in values]
        return new_values

    def mask_values(self, col = 0, new_term = "U", unique = True):
        old_values = self.get_column(col = col, unique = unique)
        new_values = self.create_masked_values(col = col, new_term = new_term)

        for row in self.spreadsheet[1:]:
            index = old_values.index(row[col])
            row[col] = new_values[index]

    def set_spreadsheet_from_list(self, f = None):
        self.spreadsheet = f

    def save_spreadsheet(self, name = "new_data", file_type = "csv"):
        name = time.strftime("%Y%m%d_%H%M%S") + "_" + name + "." + file_type
        spreadsheet_to_save = []

        for row in self.spreadsheet:
            spreadsheet_to_save.append(",".join(row))

        spreadsheet_to_save = "\r".join(spreadsheet_to_save)

        open_file = open(name, "w")
        open_file.write(spreadsheet_to_save)
        open_file.close()

    def count_tokens(self, token = "@", index = 2):
        if not self.transposed:
            self.transpose()
            
        self.spreadsheet[0].append(token)

        token = r"" + token + "\w+"

        for row in self.spreadsheet[1:]:
            tokens = re.findall(token, row[2])
            length = str(len(tokens))
            row.append(length)

    def transpose(self, spreadsheet = None):

        if self.loaded:

            if spreadsheet is None:
                s = self.spreadsheet
            else:
                s = spreadsheet

            new_sheet = [[] for x in "|".join(s[0]).split("|")]
            #print new_sheet

            col_count = len(s[0])
            row_count = len(s)
            #print col_count, row_count

            for i in range(row_count):#[:10000]:
                #print self.spreadsheet[i][:3]
                for j in range(col_count):
                    #print i, j
                    #print "\t", self.spreadsheet[i][j]
                    new_sheet[j].append(s[i][j])



            if spreadsheet is None:
                self.spreadsheet = new_sheet
                self.transposed = not self.transposed
                #print self.spreadsheet[:4]
            else:
                self.transposed = not self.transposed
                return new_sheet
        else:
            print "No file loaded."

        #print "TEST", self.transposed


if __name__ == "__main__":
    s = Spreadsheet("data/cs_data_masked_lite.csv")
    s.load()
    #s.create_masked_values(3)
    #s.mask_values(3)
    #s.count_tokens("http://")
    #s.save_spreadsheet()
    s.transpose()

