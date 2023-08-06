import argparse
import sys
import os


def before_scenario(context, scenario):
    print("\n-----------------------------------------------------------------")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    context.parser = parser
    context.sys = sys.argv[:]
    context.mock_sys = []
    context.tmp_files = []


def after_scenario(context, scenario):
    sys.argv = context.sys[:]
    for f in context.tmp_files:
        os.unlink(f)
