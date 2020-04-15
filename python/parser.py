# Parse a html document

import os

rootDir = "../"
includeDir = rootDir+"includes/"
templateDir = rootDir+"templates/"

def isCodeLine(line):
    contents = line.split()
    return (len(contents) != 0 and contents[0] == "{%")

def interpreteCode(line, result):
    contents = line.split()
    assert(len(contents) >= 3)
    assert(contents[0] == "{%")
    instruction = contents[1]
    if instruction == "include":
        assert(len(contents) == 4)
        fileName = contents[2]
        include = open(includeDir+fileName)
        while True:
            s = include.readline()
            if (s == ''):
                break;
            result.write(s)
        include.close()

def parser(templateName, resultName):
    template = open(templateName, 'r')
    result = open(resultName, 'w')
    while True:
        s = template.readline()
        if (s == ''):
            break;
        if not isCodeLine(s):
            result.write(s)
        else:
            interpreteCode(s, result)
    template.close()
    result.close()

def recursiveExplorer(currentDir):
    contentList = os.listdir(templateDir+currentDir)
    for content in contentList:
        if os.path.isdir(templateDir+currentDir+content):
            recursiveExplorer(currentDir+content+"/")
        else:
            os.makedirs(rootDir+currentDir, exist_ok=True)
            parser(templateDir+currentDir+content, rootDir+currentDir+content)

def parseAllTemplates():
    recursiveExplorer("")

if (__name__ == "__main__"):
    parseAllTemplates()

