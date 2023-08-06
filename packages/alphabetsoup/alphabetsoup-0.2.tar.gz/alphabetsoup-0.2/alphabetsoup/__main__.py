# -*- coding: utf-8 -*-
'''
alphabetsoup -- fix problems in protein FASTA files
'''

# This file makes it easier for developers to test in-place via the command
# python3 -m alphabetsoup
# from the directory above this one.

from .__init__ import cli
if __name__ == '__main__':
    cli(auto_envvar_prefix='ALPHABETSOUP')
