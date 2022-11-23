#!/usr/bin/env python3

import argparse
import sys

from config_db import ConfigDb
from database import Database
from expiry_file import ExpiryFile

def main():

    # Create parser.
    parser = argparse.ArgumentParser()
 
    # Add arguments to the parser.
    parser.add_argument("symbol", choices=['HEN', 'HIS'])
    parser.add_argument("config")
 
    # Parse the arguments.
    args = parser.parse_args()
 
    # Get the arguments value.
    if args.symbol == 'HEN' or args.symbol == 'HIS':
        symbol = args.symbol
        config = args.config
        expiry_file = '{}_expiry.txt'.format(symbol.lower())
    else:
        parser.print_help()
        sys.exit(1)

    try:

        print('Updating expiration dates for symbol {} ...'.format(symbol))

        c = ConfigDb(config)

        with Database(c) as db:

            contracts = []

            print('Connecting to: {} ...'.format(c.host))
            prices = db.query(
                'select symbol, contract, expires from prices where symbol = %s and expires is null', (symbol,))

            if len(prices) > 0:    
                for (symbol, contract, expires) in prices:
                    print('{}|{} -> {}'.format(symbol, contract, expires))
                    contracts.append(contract)
            else:
                print('All {} contracts have expiration dates.'.format(symbol))
                sys.exit(1)

            print('Reading expiration dates from: {} ...'.format(expiry_file))

            # The ExpiryFile class.
            f = ExpiryFile(expiry_file)

            for c in contracts:
                date = None

                if f.is_symbol(symbol):
                    print('Searching {} {} ...'.format(symbol, c))
                    date = f.find_expire_date(c)
                else:
                    print('Symbol {} not found.'.format(symbol))
                
                if date != None: 
                    print('Updating {} {} with {} ...'.format(symbol, c, date))
                    db.execute('update prices set expires = %s where symbol = %s and contract = %s', (date, symbol, contract,))
                else:
                    print('No expiration date found for {} {} ...'.format(symbol, contract))

    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()
    
