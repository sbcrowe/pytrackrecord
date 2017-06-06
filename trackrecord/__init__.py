# -*- coding: utf-8 -*-
""" This module provides tools for visualisation of track record."""

# authorship information
__author__ = 'Scott Crowe'
__email__ = 'sb.crowe@gmail.com'
__license__ = "GPL3"

# import required code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


class ScopusAnalysis:
    """Performs analysis of Scopus track record export."""

    def __init__(self, path):
        # instantiate
        self._path = path
        self._data_frame = pd.read_csv(self._path)

    def annual_output(self, years = None):
        annual_output = Counter(self._data_frame.get('Year')).most_common()
        if years is None:
            return annual_output
        else:
            dao = dict(annual_output)
            return list({year:dao[year] for year in years if year in dao}.items())

    def total_output(self, start_year = 2012, number_years = 5):
        years = range(start_year, start_year + number_years, 1)
        tally = 0
        for output in self.annual_output():
            if output[0] in years:
                tally += output[1]
        return tally

    def coauthor_count(self, limit = None):
        author_lists = self._data_frame.get('Authors')
        author_surnames = []
        for author_list in author_lists:
            author_surnames.extend(author_list.split(',')[::2])
        author_surnames = [x.strip() for x in author_surnames]
        if limit is None:
            return Counter(author_surnames).most_common()[1:]
        else:
            return Counter(author_surnames).most_common(limit + 1)[1:]

    def journal_count(self):
        journal_names = self._data_frame.get('Source title')
        return Counter(journal_names).most_common()

    def h_index(self):
        citations = self._data_frame.get('Cited by').values
        citation_numbers = np.array(sorted([x for x in citations if not pd.isnull(x)], reverse=True))
        h_index = 0
        while h_index + 1 <= sum(citation_numbers > h_index):
            h_index = h_index + 1
        return h_index

    def plot_differential_publication_histogram(self, moving_average = True):
        years = np.sort(self._data_frame.get('Year').values)
        labels, values = zip(*Counter(years).items())
        plt.title('Histogram of annual publications')
        plt.xlabel('Year')
        plt.ylabel('# of publications')
        plt.bar(labels, values)
        if moving_average:
            def moving_average(labels, values):
                dictionary = dict(zip(labels, values))
                results = []
                for year in range(min(labels), max(labels)+1):
                    five_year_tally = 0
                    for sum_year in range(year-4,year+1):
                        if sum_year in dictionary:
                            five_year_tally += dictionary[sum_year]
                    results.append(five_year_tally / 5)
                return results
            # note: removal of labels and use of 'valid' mode is intended to avoid edge effects
            sorted_years = np.sort(labels)
            average, = plt.plot(sorted_years, moving_average(labels, values), 'r-', label='Moving average (past 5 years)')
            plt.legend(handles=[average])
        plt.show()

    def plot_cumulative_publication_histogram(self):
        years = np.sort(self._data_frame.get('Year').values)
        plt.bar(years, np.arange(years.size))
        plt.show()


class ePrintAnalysis:
    """Performs analysis of ePrint track record export."""

    def __init__(self, path):
        # instantiate
        self._path = path
        self._data_frame = pd.read_csv(self._path)

    def annual_output(self, years = None):
        annual_output = Counter(self._data_frame.get('Date Published')).most_common()
        if years is None:
            return annual_output
        else:
            dao = dict(annual_output)
            return list({year:dao[year] for year in years if year in dao}.items())

    def coauthor_count(self):
        author_lists = self._data_frame.get('Authors/Creators')
        author_surnames = []
        for author_list in author_lists:
            author_names = author_list.split('and')
            for author_name in author_names:
                author_surnames.append(author_name.split(',')[0])
        author_surnames = [x.strip() for x in author_surnames]
        return Counter(author_surnames).most_common()[1:]