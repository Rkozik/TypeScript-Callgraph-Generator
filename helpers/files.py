import re


def extract_class_name(line):
    class_name = None
    if is_line_commented_out(line) == False:
        class_name = re.search(r'(?<=class )([A-Za-z_\s][A-Za-z0-9_\s]*)(?=\W{)', line)
        if hasattr(class_name, 'group'):
            class_name = class_name.group(1)
            class_name = re.search(r'^([\w\-]+)', class_name).group(1)

    return class_name


def extract_method_name(line):
    method_name = None
    if is_line_commented_out(line) == False:
        line = line.strip()
        if line[0:2] != "if" and line[0:3] != "for" and line[0:8] != "function" and line[-1:] != ";" and "parseInt(" not in line:
            method_name = re.search(r'(?!while|if|case|switch|for)([a-zA-Z_{1}][a-zA-Z0-9_]+)(?=\()', line)
            if hasattr(method_name, 'group'):
                method_name = method_name.group(1)

    return method_name


def extract_field_name(line):
    field_name = None
    if is_line_commented_out(line) == False:
        line = line.strip()
        field_name = re.search(r'(?:public|protected|private|readonly)+\W([a-zA-Z_{1}][a-zA-Z0-9_]+)(?=\:)', line)
        if hasattr(field_name, 'group'):
            field_name = field_name.group(1)

    return field_name


def is_line_commented_out(line):
    line = line.strip()
    if line != "":
        if line[0:2] == "//" or line[0:2] == "/*" or line[0:2] == "*/" or line[0] == "*":
            return True
    return False
