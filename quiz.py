def separate_file(path: str, separator: str = "  -  ", reversing:bool = False):
    with open(path) as f:
        line = f.read()
        wet = line.split("\n")
        task = {}
        for part in wet:
            if separator in part and len(part.split(separator)) == 2:
                if reversing:
                    answer, question = part.split(separator)
                else:
                    question, answer = part.split(separator)
                task[question] = answer
    return task


def file_check(path: str, separator: str = "  -  "):
    with open(path) as f:
        line = f.read()
        if separator in line and line.count(separator) > 1:
            return True
        else:
            return False


def file_empty_check(path: str, separator: str = "  -  "):
    with open(path) as f:
        line = f.read()
        if line == " \n" or len(line) == 0:
            return True
        else:
            return False
