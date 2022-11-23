#!/usr/bin/env python3

import re
import sys

class ExpiryFile:
    """
    Creates a class with a dictionary of expiration dates, the keys are the
    contracts. Uses a expiry file created with the HEN/HIS web scraper.
    """

    def __init__(self, file_name):

        self.symbol = None
        self.expire_dates = {}      # Dictionary with contracts as keys and dates as values.

        try:

            with open(file_name, 'r') as f:
                self.lines = f.readlines()

            self._create_dictionary()

        except FileNotFoundError:
            print('File {} not found!'.format(file_name))

    def _create_dictionary(self):
        """
        Uses REGEX to find lines that contain a line like Henry Basis Future
        and then lines like Nov22|11/2/2022.
        The method updates 2 class variables self.symbol, self.expire_dates.
        """

        symbol_pattern = re.compile(r'^Henry')
        contract_pattern = re.compile(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{2}\|\d{1,2}/\d{1,2}/\d{4}$')
                
        for line in self.lines:

            if symbol_pattern.match(line):
                self.symbol = self._convert_symbol(line.rstrip())
                continue

            if contract_pattern.match(line):

                (contract, date) = line.strip().split('|')
                self.expire_dates[self._convert_contract(contract)] = self._convert_date(date)

                continue

    def _convert_symbol(self, symbol):
        """
        Helper function to convert a web page name to a valid database symbol.
        """
        if symbol == 'Henry Basis Future':
            s = 'HEN'
        elif symbol == 'Henry Index Future':
            s = 'HIS'
        else:
            s = symbol

        return s 

    def _convert_contract(self, contract):
        """
        Helper function to convert a expiry file contract to a database contract.
        """
        month = contract[0:3]
        year = contract[-2:]
        
        if month == 'Jan':
            mbf_contract = 'F' + year
        elif month == 'Feb':
            mbf_contract = 'G' + year
        elif month == 'Mar':
            mbf_contract = 'H' + year
        elif month == 'Apr':
            mbf_contract = 'J' + year
        elif month == 'May':
            mbf_contract = 'K' + year
        elif month == 'Jun':
            mbf_contract = 'M' + year
        elif month == 'Jul':
            mbf_contract = 'N' + year
        elif month == 'Aug':
            mbf_contract = 'Q' + year
        elif month == 'Sep':
            mbf_contract = 'U' + year
        elif month == 'Oct':
            mbf_contract = 'V' + year
        elif month == 'Nov':
            mbf_contract = 'X' + year
        elif month == 'Dec':
            mbf_contract = 'Z' + year
        else:
            mbf_contract = contract

        return mbf_contract

    def _convert_date(self, date):
        """
        Helper function to convert an expiry date to a database format date.
        """
        (month, day, year) = date.split('/')
        return '{}-{}-{}'.format(year, month, day)

    def is_symbol(self, symbol):
        return self.symbol == symbol

    def find_expire_date(self, contract):
        """
        Returns a date string for a given contract, if the contract
        doesn't exist returns None.
        """
        if contract in self.expire_dates:
            return self.expire_dates[contract]
        else:
            return None

def print_help():
    print('Argument with file name is required!')

def main():

    # The argument should be a file name.
    if len(sys.argv) == 1:
        print_help()
        sys.exit(1)
    else:
        file_name = sys.argv[1]

    # The ExpiryFile class.
    f = ExpiryFile(file_name)

    for c in ('X22', 'X27', 'X28'):
        
        date = None
        if f.is_symbol('HEN'):
            date = f.find_expire_date(c)

        print('{} {}'.format(c, date))

if __name__ == '__main__':
    main()