import csv
import json 

class CsvToJson:
    def __init__(self, csv_filename):
        self.csvFile = open(csv_filename, 'r')
        self.jsonFile = open('output.json', 'w')
        self.jsonFile.write("[")

    def showCsv(self):
        for line in self.csvFile:
            print(line)

    def show(self):
        for line in open('converted.json', 'r'):
            print(line)

    def convert(self):
        fieldnames = ("id", "language", "link","text","keywords","sentiment","website","date")
        writeComma = False
        reader = csv.DictReader(self.csvFile, fieldnames)
        for row in reader:
            if (writeComma):
                self.jsonFile.write(",")
            writeComma = True
            json.dump(row, self.jsonFile)
            self.jsonFile.write("\n")
        self.jsonFile.write("]")
        self.jsonFile.close()

CsvToJson("output.csv").convert()
