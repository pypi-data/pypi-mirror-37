from bs4 import BeautifulSoup
import bs4
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import re


class ATNF:
    head_char = '-'
    empty_symbol = '*'

    def __init__(self, url, *, content_file=None, result_file=None,  refresh=False):
        self.url = url
        self.__response_content = None
        self.__content_file = content_file
        self.result_file = result_file
        self.__soup = None
        self.refresh = refresh
        self.column_names = None
        self.units = []
        self.df = None
        self.__csv_alread_read = False
        if self.__content_file is None:
            self.__content_file = os.path.join(os.getcwd(), 'ATNF.txt')
        if self.result_file is None:
            self.result_file = os.path.join(os.getcwd(), 'ATNF_table.txt')

    def get_from_url(self, filename=None):
        if filename:
            self.__content_file = filename
        if os.path.isfile(self.__content_file) and not self.refresh:
            with open(self.__content_file, 'rb') as f:
                self.__response_content = f.read()
        else:
            response = requests.get(self.url)
            self.__response_content = response.content
            with open(self.__content_file, 'wb') as f:
                f.write(self.__response_content)
                print('write file to {}'.format(self.__content_file))
        self.__soup = BeautifulSoup(self.__response_content, 'lxml')

    def to_csv(self, filename=None):
        if filename:
            self.result_file = filename

        self.get_from_url()
        table = self.__soup.find('pre').getText().strip() \
            .strip(ATNF.head_char).strip('\n').split('\n')
        self.column_names = table[0].strip('#').split()
        result = ' '.join(self.column_names) + '\n'

        print('column names: ', result)
        for row in table:
            processed = self.__parse_each_row(row)
            if processed == '':
                continue
            result += processed + '\n'
        with open(self.result_file, 'w') as f:
            f.write(result)
        self.__csv_alread_read = True

    def __parse_each_row(self, row):
        row_elements = row.split()
        res = ''
        p_starName = re.compile(r'(J|B)\d{,4}[+-]')
        p_reference = re.compile(r'([A-Z].*)|([a-z].*)')

        def pure_interger(x):
            try:
                int(x)
            except:
                return False
            else:
                return True

        for i, e in enumerate(row_elements[1:]):
            if e == ATNF.empty_symbol:
                return ''
            if p_starName.match(e) or (not p_reference.match(e) and not pure_interger(e)):
                if e.strip().startswith('('):
                    self.units.append({self.column_names[i]: e})
                    continue
                res += str(e).strip() + ' '
        return res

    def get_table(self):
        if not self.__csv_alread_read:
            self.to_csv()
        self.df = pd.read_csv(self.result_file, index_col=False, delimiter=' ')

    def plot(self, xlabel, ylabel, *args, **kwargs):
        if self.df is None:
            self.get_table()
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        try:
            plt.scatter(self.df[xlabel], self.df[ylabel], *args, **kwargs)
            return plt
        except Exception as e:
            print(e)

    def clean(self):
        try:
            os.remove(self.__content_file)
            os.remove(self.result_file)
        except Exception as e:
            print(e)
