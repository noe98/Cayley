"""
Sets arbitrary values of variables to be referenced by volume.py.
"""

total_nodes = [[1,None,None,None,None], #total_nodes[gens][links]
               [None,2,3,4,5,6],
               [None,None,5,10,17,26],
               [None,None,7,22,53,106,187],
               [None,None,9,46,161,426],
               [None,None,11,94,485,1706]]

def listify(string):
    liszt = list()
    marks = [-1]
    for i in range(len(string)):
        if string[i] == ',':
            marks.append(i)
    marks.append(len(string)-1)
    for j in range(len(marks)-1):
        try:
            liszt.append(string[marks[j]+2:marks[j+1]-1].split())
        except IndexError:
            liszt.append(string[marks[j]+2:len(string)].split())
    return liszt

def variable(string_key, var_type, value_type = str, start_index = False):
    if not start_index:
        start_index = len(string_key)+3
    with open('variables.txt') as variables:
        reader = variables.readlines()
        for line_ind in range(len(reader)):
            line = reader[line_ind]
            try:
                if line[:len(string_key)] == str(string_key):
                    if var_type == int:
                        return int(line[start_index:])
                    elif var_type == float:
                        return float(line[start_index:])
                    elif var_type == str:
                        return line[start_index:].lstrip().rstrip()
                    elif var_type == list:
                        liszt = listify(line[start_index:])
                        end = list()
                        if value_type == int:
                            for i in range(len(liszt)):
                                end.append([])
                                for j in range(len(liszt[i])):
                                    end[i].append(int(liszt[i][j]))
##                                    except ValueError:
##                                        print("Raised a ValueError")
##                                        if '(' in liszt[i][j]:
##                                            end[i].append(int(liszt[i][j][1:]))
##                                        elif ')' in liszt[i][j]:
##                                            end[i].append(int(liszt[i][j][:len(liszt[i][j])-1]))
                        elif value_type == float:
                            for i in range(len(liszt)):
                                end.append([])
                                for j in range(len(liszt[i])):
                                    end[i].append(float(liszt[i][j]))
##                                    except ValueError:
##                                        print("Raised a ValueError")
##                                        if '(' in liszt[i][j]:
##                                            end[i].append(float(liszt[i][j][1:]))
##                                        elif ')' in liszt[i][j]:
##                                            end[i].append(float(liszt[i][j][:len(liszt[i][j])-1]))
                        elif value_type == str:
                            for i in range(len(liszt)):
                                end.append([])
                                for j in range(len(liszt[i])):
                                    end[i].append(liszt[i][j])
                        if len(end) == 1 and '(' not in line[start_index:]:
                            end = end[0]
                        return end
                    elif var_type == dict:
                        dictionary = {}
                        for end_ind in range(len(reader)):
                            if end_ind >= line_ind and '}' in reader[end_ind]:
                                end_line = reader[end_ind]
                                break
                        dict_lines = reader[line_ind:end_ind+1]
                        for row in dict_lines:
                            try:
                                row = row[row.index('{')+1:]
                            except ValueError:
                                pass
                            row = row.lstrip()
                            try:
                                mark = row.index(':')
                                key = row[:mark]
                                entry = row[mark+1:].lstrip().rstrip()
                                if value_type == int:
                                    key = int(key)
                                    entry = int(entry)
                                if value_type == float:
                                    key = int(key)
                                    entry = float(entry)
                                dictionary[key] = entry
                            except ValueError:
                                pass
                        return dictionary
            except IndexError:
                continue
