#!/usr/bin/env python

import re
import json
import sys
import requests
import collections
from tqdm import tqdm
from ascii_graph import Pyasciigraph
from ascii_graph.colors import Gre, Yel, Red
from ascii_graph.colordata import vcolor

class CheckPwnd(object):
    '''
    '''
    def __init__(self, email):
        '''
        '''
        self.email = email
        self.base_url = "https://haveibeenpwned.com/api/v2/{}/{}"
        self.dump_dict = {}
        self.user_agent = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
        }
        self.pwned_check = self.base_url.format("pasteaccount", self.email)
        self.breached_check = self.base_url.format("breachedaccount", self.email)
        self.pastebin_dump = "https://www.pastebin.com/raw/{}"
        self.detected_breaches = collections.Counter()

    def account_check(self):
        '''
        check if there is an account
        return None if there isn't.
        TODO:
            None is fine for now may need to make this return something else
        '''

        return requests.get(self.pwned_check, headers=self.user_agent)

    def print_stats(self, title, dataset):
        '''
        inpsired by:
            https://github.com/x0rz/tweets_analyzer/blob/master/tweets_analyzer.py#L286-L291
        '''
        keys = dataset.items()

        pattern = [Red, Yel, Gre]
        data = vcolor(keys, pattern)

        graph = Pyasciigraph()
        for line in graph.graph(title, data):
            print(line)

    def account_stats(self):
        '''
        '''
        account_stats = {}
        breach_stats = {}
        breached_accounts = requests.get(self.breached_check, headers=self.user_agent)
        breach_num = [breaches['Name'] for breaches in
                      tqdm(breached_accounts.json())]

        account_stats['breach_num'] = len(breach_num)

        top_breaches = [(breaches['PwnCount'], breaches['Name']) for breaches
                        in breached_accounts.json()]

        for k, v in sorted(top_breaches[:5], reverse=True):
            breach_stats[v] = k
        self.print_stats("account: {} pwn stats".format(self.email),breach_stats)
        self.print_stats("account: {} breach stats".format(self.email), account_stats)

    def account_dump(self, account_check):
        '''
        Dump the accounts into a dict with 2 lists.
        Might make this function receive email in future.
        '''
        #account_check = self.account_check("pasteaccount")
        if account_check:
            pastebin = [self.pastebin_dump.format(data["Id"]) for data in
                        account_check.json() if data["Source"] ==
                        "Pastebin" ]

            adhoc = [ data["Id"] for data in
                     account_check.json() if data["Source"] ==
                     "AdHocUrl"]

            self.dump_dict["pastebin"] = pastebin
            self.dump_dict["adhoc"] = adhoc

            return self.dump_dict
        else:
            return account_check

    def account_fetch(self):
        '''
        Dump the found creds to stdout or (possibly) in future to file
        This regex does not find *everything that returns will need to find a
        better way.
        This was the simplest regex I could muster because I suck
        the lines may need to be split
        out and searched that way.
        '''

        urls = self.account_dump()
        for website, url in urls.items():
            for dumps in url:
                data = requests.get(dumps)
                if data:
                    password = re.search('{}:(\w+)'.format(self.email), data.text)
                    if password:
                        print(password.group())
