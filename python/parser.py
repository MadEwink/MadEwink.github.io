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
    while (hasParameter(line)):
        line_beginning = line.partition("{{")[0]
        line_end = line.partition("}}")[2]
        parameter = line.partition("{{")[2].partition("}}")[0]
        argument,index = findNextArgument(parameter, 0)
        # default value, if the argument was not specified in the command
        value,index = readArgumentValue(parameter, index)
        if (argument in command_arguments):
            value = command_arguments[argument]
        line = line_beginning + value + line_end
    return line

def interpreteCode(line, result, command_arguments, global_arguments):
    contents = line.split()
    assert(len(contents) >= 3)
    assert(contents[0] == "{%")
    indentation = line.split('{')[0]
    instruction = contents[1]
    if instruction == "include":
        fileName = command_arguments['file_name']
        include = open(includeDir+fileName)
        while True:
            s = include.readline()
            if (s == ''):
                break
            if (hasParameter(s)):
                s = replaceParameter(s, command_arguments)
            result.write(indentation+s)
        include.close()
    elif instruction == "make-posts":
        createProjectPosts(result, indentation)
    elif instruction == "load-arguments":
        fileName = command_arguments['file_name']
        loaded_arguments = parseProjectData(includeDir+fileName)
        for key in loaded_arguments:
            global_arguments[key] = loaded_arguments[key]

def parser(templateName, resultName):
    global_arguments = dict()
    template = open(templateName, 'r')
    result = open(resultName, 'w')
    while True:
        s = template.readline()
        if (s == ''):
            break
        if isCodeLine(s):
            # parse command_arguments
            # /!\ an argument may be composed of strings with spaces !!
            command_arguments = parseCommandArguments(s)
            interpreteCode(s, result, command_arguments, global_arguments)
        elif hasParameter(s):
            s = replaceParameter(s,global_arguments)
            result.write(s)
        else:
            result.write(s)
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

def appendData(project_data, data_type, content):
    if (data_type == "tags"):
        tag_list = content.split(',')
        project_data[data_type] = tag_list
    elif (content != "none"):
        project_data[data_type] = content

def parseProjectData(fileName):
    data_file = open(fileName, 'r')
    project_data = dict()
    while True:
        s = data_file.readline()
        if (s == ''):
            break
        partition = s.partition('=')
        appendData(project_data, partition[0], partition[2].rstrip('\n'))
    return project_data

def createTags(projects_data, indentation, tag_indentation):
    if (not ("tags" in projects_data)):
        return ""
    tags = projects_data["tags"]
    s = tag_indentation+"<li>"
    for i in range(len(tags)-1):
        s += tags[i] + "</li>\n"+indentation+tag_indentation+"<li>"
    s += tags[-1] + "</li>\n"
    return s

def createProjectPosts(result, indentation):
    data_dir = includeDir+"projects_data/"
    project_data_files = os.listdir(data_dir)
    project_data_files.sort()
    for project_data_file in project_data_files:
        if project_data_file[0] in "_.":
            continue
        project_data = parseProjectData(data_dir+project_data_file)
        project_post_template = open(includeDir+"project_post.html", 'r')
        while True:
            s = project_post_template.readline()
            if (s == ''):
                break
            if (hasParameter(s)):
                if (s.find("{{ tags }}") != -1):
                    tag_indentation = s.partition('{')[0]
                    s = createTags(project_data, indentation, tag_indentation)
                else:
                    s = replaceParameter(s, project_data)
            result.write(indentation+s)
        project_post_template.close()


if (__name__ == "__main__"):
    parseAllTemplates()

