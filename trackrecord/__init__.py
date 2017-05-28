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
        self._data_frame = pd.read_csv(path)

    def coauthor_count(self):
        author_lists = self._data_frame.get('Authors')
        author_surnames = []
        for author_list in author_lists:
            author_surnames.extend(author_list.split(',')[::2])
        author_surnames = [x.strip() for x in author_surnames]
        return Counter(author_surnames).most_common()[1:]

    def journal_count(self):
        journal_names = self._data_frame.get('Source title')
        return Counter(journal_names).most_common()

    def h_index(self):
        citations = self._data_frame.get('Cited by').values
        citation_numbers = np.array(sorted([x for x in citations if not pd.isnull(x)], reverse=True))
        print(citation_numbers)
        h_index = 0
        while h_index + 1 <= sum(citation_numbers > h_index):
            h_index = h_index + 1
        return h_index

    def plot_differential_publication_histogram(self):
        years = np.sort(self._data_frame.get('Year').values)
        labels, values = zip(*Counter(years).items())
        plt.bar(labels, values)
        plt.show()

    def plot_cumulative_publication_histogram(self):
        years = np.sort(self._data_frame.get('Year').values)
        plt.bar(years, np.arange(years.size))
        plt.show()