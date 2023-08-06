import csv, sys
from qualifyr.quality_file import QualityFile
from qualifyr.utility import string_to_num, get_logger

class FastqcFile(QualityFile):
    logger = get_logger(__file__)
    file_type = 'fastqc'

    def validate(self):
        # method to check file looks like what it says it is
        '''Returns valid rows from file. An empty list if invalid'''
        with open(self.file_path) as fh:
            reader = csv.reader(fh, delimiter="\t", quotechar='"')
            rows = list(reader)
            first_row = rows[0]
            last_row = rows[-1]
            if first_row[1] == 'Basic Statistics' and last_row[1] == 'Adapter Content':
                return rows
            else:
                return []
    

    def parse(self):
        # read in file and make a dict:
        valid_rows = self.validate()
        if len(valid_rows) == 0:
            self.logger.error('quast file invalid')
            sys.exit(1)
        else:
            for row in valid_rows:
                self.metrics[row[1]] = row[0]