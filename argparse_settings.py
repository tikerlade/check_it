"""
Singleton for argparse object.
"""

import argparse

argparse_obj = argparse.ArgumentParser()

argparse_obj.add_argument('--urls',
                          nargs='+',
                          default=[],
                          required=False,
                          help='URL you need to track.')

argparse_obj.add_argument('--request_int',
                          type=int,
                          default=1,
                          required=False,
                          help='How often we need to request data (minutes).')

argparse_obj.add_argument('--symbols_diff',
                          type=int,
                          default=10,
                          required=False,
                          help='How many symbols must change on page that we can say it changed.')