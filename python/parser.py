# Parse a html document

import os

rootDir = "../"
includeDir = rootDir+"includes/"
templateDir = rootDir+"templates/"

def isCodeLine(line):
    contents = line.split()
    return (len(contents) != 0 and contents[0] == "{%")

def findNextArgument(line, index):
    last_space = index
    argument = ""
    while (line[index] != '='):
        if (line[index] == ' '):
            last_space = index
        index += 1
    argument = line[last_space+1:index]
    return (argument,index)

def readArgumentValue(line, index):
    #index is on space
    begin_index = index + 1
    end_index = begin_index+1
    value = ""
    end_char = ' '
    if (line[begin_index] == '"'):
        begin_index += 1
        end_char = '"'
    while (line[end_index] != end_char):
        end_index += 1
    return (line[begin_index:end_index], end_index)


def parseCommandArguments(line):
    argument_number = line.count('=')
    index = 0
    arguments = dict()
    for i in range(argument_number):
        argument,index = findNextArgument(line, index)
        value,index = readArgumentValue(line, index)
        arguments[argument] = value
    return arguments

def hasParameter(line):
    return line.find("{{") != -1

def replaceParameter(line, command_arguments):
    line_beginning = line.split("{{")[0]
    line_end = line.split("}}")[1]
    parameter = line.split("{{")[1].split("}}")[0]
    argument,index = findNextArgument(parameter, 0)
    # default value, if the argument was not specified in the command
    value,index = readArgumentValue(parameter, index)
    if (argument in command_arguments):
        value = command_arguments[argument]
    return line_beginning + value + line_end;

def interpreteCode(line, result, command_arguments):
    contents = line.split()
    assert(len(contents) >= 3)
    assert(contents[0] == "{%")
    instruction = contents[1]
    if instruction == "include":
        fileName = command_arguments['file_name']
        include = open(includeDir+fileName)
        indentation = line.split('{')[0]
        while True:
            s = include.readline()
            if (s == ''):
                break;
            if (hasParameter(s)):
                s = replaceParameter(s, command_arguments)
            result.write(indentation+s)
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
            # parse command_arguments
            # /!\ an argument may be composed of strings with spaces !!
            command_arguments = parseCommandArguments(s)
            interpreteCode(s, result, command_arguments)
    template.close()
    result.close()

def recursiveExplorer(currentDir):
    contentList = os.listdir(templateDir+currentDir)
    for content in contentList:
        if content[0] in "_.":
            continue
        if os.path.isdir(templateDir+currentDir+content):
            recursiveExplorer(currentDir+content+"/")
        else:
            os.makedirs(rootDir+currentDir, exist_ok=True)
            parser(templateDir+currentDir+content, rootDir+currentDir+content)

def parseAllTemplates():
    recursiveExplorer("")

if (__name__ == "__main__"):
    parseAllTemplates()

