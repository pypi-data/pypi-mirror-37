#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
import os
import yaml
import getopt

__author__ = "handa"
__version__ = '0.2.0'


class BaseObject(object):
    """
    基类,主要是model转str
    """

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())

    def gatherAttrs(self):
        return ", ".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


class PodObject(BaseObject):
    """
    git 信息
    """

    def __init__(self):
        self.name = ""
        self.currentVersion = ""
        self.specifiedVersion = ""
        self.subSpecList = []  # subSpec 列表
        self.dependenceList = []  # 依赖列表
        self.citedList = []  # 被依赖列表


def writeToFile(string, filePath):
    """
    把字符串写进文件
    :param string:
    :param filePath:
    :return:
    """
    with open(filePath, "w+") as fileWriter:
        fileWriter.write(string)


def appendToFile(string, filePath):
    with open(filePath, "a+") as fileWriter:
        fileWriter.write(string)


def formatPrint(printString, separate=""):
    if separate:
        print separate * 30 + '\n'
    print str(printString)


def printTips():
    formatPrint("""
    需要提供三个参数：

    --appName                   app 的名字
    --lockPath                  pod install/update 之后生成的Podfile.lock 文件
    --resultPath                导出的结果文件，不存在会自动创建。是 marddown 文件。

    """, "**")


def fileExist(path):
    """
    检测模块是否已经安装
    Arguments:
        path {str} -- 模块路径
    Returns:
        Bool -- 是否已经安装
    """
    if os.path.isdir(path) or os.path.isfile(path):
        return True
    return False


def parse_name_version(str=""):
    """
    字符串分割出名字和版本
    :param str:
    :return:
    """
    name = version = None
    if not str:
        return name, version
    tmpStr = str.replace("(", "").replace(")", "")
    tmpList = tmpStr.split(" ")
    name = tmpList[0]
    if len(tmpList) >= 2:
        version = tmpStr.replace(name + " ", "")
    return name, version


def parse_subSpec(str=""):
    """
    根据字符串，解析出subspec
    :param str:
    :return:
    """
    podName = subspec = None
    tmplist = str.split("/")
    podName = tmplist[0]
    if len(tmplist) >= 2:
        subspec = str.replace(podName + "/", "")
    return podName, subspec


# noinspection PyInterpreter
def lockfile_pods_dict(podDict, AppName, pods, dependency_list):
    """
    lockfile 的podDict 属性
    :param AppName 项目
    :param pods: lockfile 的PODS
    :param dependencies :lockfile 的DEPENDENCIED
    :return: 以库名为key，值为PodObject 的字典
    """
    for object in pods:

        if isinstance(object, dict):
            # 解析依赖关系
            keyStr = object.keys().pop()
            key_tmp_name, key_version = parse_name_version(keyStr)
            key_pod_name, key_subspec_name = parse_subSpec(key_tmp_name)
            if key_subspec_name:
                # 前面已经有了，这里解析的是subspec的dependency
                podDict = lockfile_pods_dict(podDict, key_pod_name, object[keyStr], dependency_list)
            else:
                # 可能是新的库
                podObject = None
                if key_pod_name in podDict.keys():
                    podObject = podDict[key_pod_name]
                else:
                    # 不存在，创建一个
                    podObject = PodObject()
                    podDict[key_pod_name] = podObject
                podObject.name = key_pod_name
                podObject.currentVersion = key_version
                dependencie_list = object[keyStr]
                for dependencie in dependencie_list:
                    value_tmp_name, value_version = parse_name_version(dependencie)
                    value_pod_name, value_subspec_name = parse_subSpec(value_tmp_name)
                    if value_subspec_name:
                        # subspec
                        if value_pod_name not in podObject.subSpecList:
                            podObject.subSpecList.append(value_subspec_name)
                    else:
                        # 不是subspec，而是依赖
                        dependencyObject = None
                        if value_pod_name in podDict.keys():
                            dependencyObject = podDict[value_pod_name]
                        else:
                            dependencyObject = PodObject()
                            dependencyObject.name = value_pod_name
                            dependencyObject.currentVersion = value_version
                            # 被依赖
                        if dependencyObject not in podObject.dependenceList:
                            podObject.dependenceList.append(dependencyObject.name)
                        dependencyObject.citedList.append(podObject.name)
        elif isinstance(object, str):
            # 字符串，解析名字，版本
            tmp_name, version = parse_name_version(object)
            pod_name, subspec_name = parse_subSpec(tmp_name)
            if subspec_name:
                # 是 subspec，不要
                continue
            podObject = PodObject()
            if pod_name in podDict.keys():
                podObject = podDict[pod_name]
            else:
                podObject = PodObject()
                podDict[pod_name] = podObject
            podObject.citedList.append(AppName)
            if AppName not in object and AppName in podDict.keys():
                podDict[AppName].dependenceList.append(pod_name)
            podObject.name = pod_name
            podObject.currentVersion = version
    for dependencyString in dependency_list:
        tmp_name, version = parse_name_version(dependencyString)
        pod_name, subspec_name = parse_subSpec(tmp_name)
        podObject = None
        if pod_name in podDict.keys():
            podObject = podDict[pod_name]
            podObject.specifiedVersion = version
    return podDict


def getarguments():
    """
    获得参数
    :param type: 哪个命令的参数
    :return:
    """
    if type == "":
        return
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:l:r:",
                                   ["help", "appName=", "lockPath=", "resultPath="])
    except getopt.GetoptError:
        printTips()
        exit(1)
    if not args and not opts:
        printTips()
        exit(1)
    appName = ""
    lockPath = ""
    resultPath = ""
    for cmd, arg in opts:
        print cmd
        # 使用一个循环，每次从opts中取出一个两元组，赋给两个变量。cmd保存选项参数，arg为附加参数。接着对取出的选项参数进行处理。
        if cmd == "--appName":
            appName = str(arg)
        elif cmd == "--lockPath":
            lockPath = arg
        elif cmd == "--resultPath":
            resultPath = arg
        else:
            printTips()
    if not appName or not lockPath or not resultPath:
        formatPrint("缺少必要的参数。")
        exit(1)
    return appName, lockPath, resultPath


def note(name):
    if not name:
        return
    return name + "(" + name + ")"


def rootNote(name):
    return name + "((" + name + "))"


def branch(start, end):
    return start + "-->" + end + "\n"


def isLianjiaPod(name):
    if str(name).startswith("LJ") or str(name).startswith("lj") or str(name).startswith(
            "Lianjia"):
        return True
    return False


def dependencyTree(appName, podFileLibrary={}):
    mdContent = "# 依赖关系图\n"
    mdContent += "> 请使用支持mermaid 图的markwodn工具查看。比如 MWeb \n>\n\n"
    mdContent += "[toc]\n\n"
    mdContent += "------\n"

    index = 1
    exclude = []
    while (1):
        leafList = []
        if index == 1:
            graph = "## " + appName + "不含第三方的依赖关系树：\n"
        else:
            graph = "## " + appName + "去掉第" + str(index - 1) + "层叶子节点后：\n"
        graph += "```mermaid\ngraph LR;\n"
        graph += rootNote(appName) + "\n"
        for gitName, gitInfo in podFileLibrary.items():
            if not isLianjiaPod(gitName) or gitName in exclude:
                continue
            if note(gitName) not in graph:
                graph += note(gitName) + "\n"
            abranch = branch(rootNote(appName), note(gitName))
            if abranch not in graph:
                graph += abranch
            isLeaf = True
            for dependence in gitInfo.dependenceList:
                if not isLianjiaPod(dependence):
                    continue
                if dependence in exclude:
                    continue
                isLeaf = False
                abranch = branch(note(gitName), note(dependence))
                if abranch not in graph:
                    graph += abranch
            if isLeaf:
                leafList.append(gitName)
        graph += "\n```\n"

        if len(leafList) == 0:
            break

        mdContent += graph + "\n\n"

        leafContent = "## 第" + str(index) + "层叶子节点\n"

        for leaf in leafList:
            leafContent += "- " + leaf + "\n"
        leafContent += "\n"

        mdContent += leafContent + "\n"

        exclude.extend(leafList)
        index += 1

    dependeceDict = {}
    for gitName, gitInfo in podFileLibrary.items():
        dependeceDict[gitName] = printDependencyTreeByName(gitName, podFileLibrary)
    graph = ""
    for gitName, gitInfo in podFileLibrary.items():
        graph += "##" + gitName + "依赖关系图\n"
        graph += "```mermaid\ngraph LR;\n"
        graph += note(gitName) + "\n"
        tmpGraph = printsubDenpencyTree(gitName, podFileLibrary, dependeceDict)
        tmpGraphList = str(tmpGraph).split("\n")
        formatList = list({}.fromkeys(tmpGraphList).keys())
        graph += "\n".join(formatList)
        graph += "\n```\n    \n"

    mdContent += graph

    mdContent += "## " + appName + "含第三方方库的依赖关系树：\n"
    graph = "```mermaid\ngraph LR;\n"
    for gitName, gitInfo in podFileLibrary.items():
        if note(gitName) not in graph:
            graph += note(gitName) + "\n"
        abranch = branch(rootNote(appName), note(gitName))
        if abranch not in graph:
            graph += abranch
        for dependence in gitInfo.dependenceList:
            abranch = branch(note(gitName), note(dependence))
            if abranch not in graph:
                graph += abranch
    graph += "\n```\n"

    mdContent += graph + "\n\n"

    return mdContent


def printsubDenpencyTree(name, podFileLibrary, dependeceDict):
    graph = dependeceDict[name]
    gitInfo = podFileLibrary[name]
    for dependence in gitInfo.dependenceList:
        graph += printsubDenpencyTree(dependence, podFileLibrary, dependeceDict) + "\n"
    return graph


def printDependencyTreeByName(name, podFileLibrary={}):
    gitInfo = podFileLibrary[name]
    graph = ""
    for dependence in gitInfo.dependenceList:
        abranch = branch(note(name), note(dependence))
        if abranch not in graph:
            graph += abranch
    return graph


def checkopts():
    appName, lockPath, resultPath = getarguments()
    if not fileExist(lockPath):
        formatPrint("找不到podfile.lock文件", "--")
        exit(1)
    if not str(resultPath).endswith(".md"):
        formatPrint("输入的resultPath不是markdown文件")
    lockContent = ''
    with open(lockPath, "r+") as fileReader:
        lockContent = yaml.load(fileReader)
    podDict = lockfile_pods_dict({}, appName, lockContent["PODS"], lockContent["DEPENDENCIES"])
    mdcontent = dependencyTree(appName, podDict)
    if not fileExist(resultPath):
        parentDic = os.path.dirname(resultPath)
        if not fileExist(parentDic):
            os.makedirs(parentDic)
    writeToFile(mdcontent, resultPath)

def main():
    # 调用接口
    checkopts()

if __name__ == "__main__":
    checkopts()
