# -*- coding:utf-8 -*-
import requests
from flask import json

import preprocessor
import compare
import time

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# pair 수 만큼 호출
def compareOnePair(originFile, compFile, pairNum, compareMethod, commentList
                   , tokenizerList, originLineNumber):
    global output
    opath = originFile.rsplit('/')[0]
    cpath = compFile.rsplit('/')[0]

    #start_time = time.time()

    originFile = open(originFile)
    compFile = open(compFile)

    originCode = originFile.read()
    compCode = compFile.read()

    preprocess_filter = [preprocessor.RemoveBlank(), tokenizerList]

    inputs = [originCode, compCode]
    outputs = []

    for i in range(len(inputs)):
        lineNumInfo = []
        for j in range(len(inputs[i].split('\n'))):
            lineNumInfo.append(j)

        if len(commentList) > 0:
            for comment in commentList[i]:
                preprocess_filter.insert(0, comment)

        for task in preprocess_filter:
            if isinstance(task, list):
                task = task[i]
            task.setInput(inputs[i])
            task.setLineNumInfo(lineNumInfo)
            output, lineNumInfo = task.process()
            inputs[i] = output

        outputs.append([output, lineNumInfo])

        if len(commentList) > 0:
            for j in range(len(commentList[i])):
                preprocess_filter.pop(0)

    # ori, comp = preprocessor.numberMapping(outputs[0][0], outputs[1][0])

    checkFunction = ''
    if compareMethod == 1:
        checkFunction = compare.OrderedCheck()
    elif compareMethod == 2:
        checkFunction = compare.UnorderedCheck()
    elif compareMethod == 3:
        checkFunction = compare.EditDistance()

    compa = compare.Compare(checkFunction)
    compa.setInput(outputs[0][0], outputs[1][0])
    ret = compa.process()

    #mid_time = time.time()

    similLine = 0.0
    entireLine = originLineNumber
    similLine += len(ret.keys())

    similarity = similLine / entireLine * 100

    result = [[pairNum, similarity]]
    for key in ret.keys():
        # key : 원본 라인 번호 -1
        result.append({'pairID': pairNum, 'originLine': outputs[0][1][key] + 1, 'compareLine': outputs[1][1][ret[key][0]] + 1, 'rType': ret[key][1]})

    return result
