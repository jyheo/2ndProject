# -*- coding:utf-8 -*-
import os
import copy
from abc import ABCMeta, abstractmethod


class Check:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    # name => compare
    @abstractmethod
    def process(self, origin, comp):
        pass


class OrderedCheck(Check):

    def process(self, origin, comp):
        dp = [[0 for col in range(len(comp) + 1)] for row in range(len(origin) + 1)]

        for i in range(1, len(dp)):
            for j in range(1, len(dp[0])):
                if origin[i - 1] == comp[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = dp[i - 1][j] if dp[i - 1][j] > dp[i][j - 1] else dp[i][j - 1]

        return float(dp[len(origin)][len(comp)]) / (len(origin) if len(origin) >= len(comp) else len(comp)) * 100


class UnorderedCheck(Check):
    def mapping(self, data):
        dict = {}

        for token in data:
            if dict.get(token, 0) == 0:
                dict[token] = 1
            else:
                dict[token] += 1

        return dict

    def process(self, origin, comp):
        origin = self.mapping(origin)
        comp = self.mapping(comp)

        tokenList = origin.keys()

        sum = 0.0
        originTokenCount = 0
        for token in tokenList:
            originCount = origin.get(token, 0)
            compCount = comp.get(token, 0)
            sum += originCount if compCount > originCount else compCount
            originTokenCount += originCount

        return (sum / originTokenCount) * 100


class Compare:
    originToken = []
    compToken = []
    method = ''

    def __init__(self, method):
        self.method = method

    def setInput(self, originFile, compFile):
        self.originToken = originFile
        self.compToken = compFile

    def process(self):
        dict = {}

        for i in range(len(self.originToken)):
            for j in range(len(self.compToken)):
                per = self.method.process(self.originToken[i], self.compToken[j])
                if per == 100.0:
                    print self.originToken[i], self.compToken[j]
                    dict[i] = dict.get(i, [])
                    dict[i].append([j, 1])
                elif per >= 70.0:
                    dict[i] = dict.get(i, [])
                    dict[i].append([j, 2])

        return dict