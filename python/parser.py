# Parse a html document

import os

rootDir = "../"
includeDir = rootDir+"includes/"
templateDir = rootDir+"templates/"

# beginning of new system

argument_store = { "global" : dict(), "local" : dict() }

class Error(Exception):
    pass

class ParameterError(Error):
    def __init__(self, line, message):
        self.line = line
        self.message = message

class ParameterBoundError(ParameterError):
    """Raised when a parameter has incorrect boundaries"""
    pass

class ValueError(ParameterError):
    pass

class ValueIncompleteStringError(ValueError):
    """Raised when the value of a parameter begins with '"' but does not end with '"'"""
    pass

class ValueTooManyItemsError(ValueError):
    """Raised when the value of a parameter has several items in an unsupported way"""
    pass

class Element():
    def __init__(self, line):
        self.line = line
    def interprete(self):
        return self

class Parameter(Element):
    def __init__(self, line):
        self.line = line
        self.__cut(line)
    def __format_argument(self, arg):
        i = 0
        # remove trailing spaces
        while arg[i].isspace():
            i += 1
        # read argument name
        self.argument = ""
        while i < len(arg):
            # replace spaces that are not at the end of the arg by '_'
            if arg[i].isspace():
                if i+1 < len(arg) and not arg[i+1].isspace():
                    self.argument += '_'
            else:
                self.argument += arg[i]
            i += 1
        # separate context
        if self.argument.find(':') != -1:
            context_pos = self.argument.rindex(':')
            self.context = self.argument[0:context_pos]
            self.argument = self.argument[context_pos+1:len(self.argument)]
        else:
            self.context = None
    def __format_value(self, val):
        i = 0
        # remove trailing spaces
        while val[i].isspace():
            i += 1
        # read value
        if val[i] == '"':
            j = i
            while True:
                # keep everything from here until the ending '"'
                end_pos = val.find('\"', j+1)
                if end_pos == -1:
                    # error, there is no end to the string
                    raise ValueIncompleteStringError(val, "no ending '\"' was found")
                if val[end_pos-1] != '\\':
                    break
                j = end_pos+1
            self.default_value = val[i+1:end_pos]
            # check if there are more stuff after string end
            j += end_pos + 1
            while j < len(val):
                j += 1
                if not val[j].isspace():
                    raise ValueTooManyItemsError(val, "there is stuff after ending \" : " + val[j])
        else:
            self.default_value = ""
            while i < len(val):
                if not val[i].isspace() or (i+1 < len(val) and not val[i+1].isspace()):
                    self.default_value += val[i]
                i += 1
    def __cut(self, line):
        equal_sign_pos = line.find('=')
        if equal_sign_pos == -1:
            self.__format_argument(line)
            self.default_value = ""
        else:
            self.__format_argument(line[:equal_sign_pos])
            self.__format_value(line[equal_sign_pos+1:])
    def interprete(self):
        # if there is a context we want the value in the context, and if it's not there just the default value
        if (self.context):
            # search associated dict
            if (self.context in argument_store and self.argument in argument_store[self.context]):
                return parseLine(argument_store[self.context][self.argument])
        # if there is no context, we first try local, then global, before getting back to default value
        elif self.argument in argument_store["local"]:
            return parseLine(argument_store["local"][self.argument])
        elif self.argument in argument_store["global"]:
            return parseLine(argument_store["global"][self.argument])
        return parseLine(self.default_value)

def parseParameter(line):
    assert(line[0] == '{')
    assert(line[1] == '{')
    # detect end of parameter
    depth = 1
    i = 2
    while depth > 0 and i < len(line):
        if line[i] == '}' and (i < len(line)-1 and line[i+1] == '}'):
            depth -= 1
        elif line[i] == '{' and (i < len(line)-1 and line[i+1] == '{'):
            depth += 1
        i += 1
    if depth != 0:
        raise ParameterBoundError(line, "depth of parameter at line end is "+str(depth))
    endpos = i-1
    return Parameter(line[2:endpos]), endpos+1

def parseLine(line):
    last_stored_pos = 0
    line_cut = []
    for i in range(len(line)):
        # if it looks like a parameter or a command
        if (line[i] == '{'):
            # if it's the end of the line, ignore
            if (i+1 >= len(line)):
                continue
            # here we know there is a next char
            if (line[i+1] == '{'):
                # it should be a parameter
                # store line beginning
                if (last_stored_pos < i-1):
                    line_cut.append(Element(line[last_stored_pos:i]))
                # store parameter
                parameter,end_pos = parseParameter(line[i:])
                i += end_pos
                line_cut.append(parameter)
                last_stored_pos = i+1
            if (line[i+1] == '%'):
                # it should be a command
                # TODO
                pass
    if (last_stored_pos < len(line)):
        line_cut.append(Element(line[last_stored_pos:len(line)]))
    return line_cut

def interpreteLine(line_cut):
    i = 0
    while i < len(line_cut):
        begin = line_cut[:i]
        current = line_cut[i]
        if i+1 < len(line_cut):
            end = line_cut[i+1:]
        else:
            end = []
        while type(current) != Element:
            l = current.interprete()
            current = l[0]
            if len(l) > 1:
                end = l[1:] + end
        line_cut = begin + [current] + end
        i += 1
    line = ""
    for e in line_cut:
        line += e.line
    return line

# end of new system

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
    project_data_files.sort(reverse=True)
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

