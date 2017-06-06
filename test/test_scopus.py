# -*- coding: utf-8 -*-
""" This module tests Scopus track record analysis record with nose."""

# authorship information
__author__ = 'Scott Crowe'
__email__ = 'sb.crowe@gmail.com'
__license__ = "GPL3"

# import required code
import trackrecord as tr

# define default parameters
_scopus_file_path = '../data/scopus.csv'
sa = tr.ScopusAnalysis(_scopus_file_path)

def test_annual_output():
    assert len(sa.annual_output()) == 9

def test_total_output():
    assert sa.total_output(2012, 5) == 43

def test_coauthor_count():
    assert len(sa.coauthor_count()) == 54

def test_h_index():
    assert sa.h_index() == 8

def test_journal_count():
    assert len(sa.journal_count()) == 11