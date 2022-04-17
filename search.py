import json 

def make_class_list(classesJson):
    class_file = open(classesJson)
    data = json.load(class_file)
    class_list = []

    for key in data:
        sections = []
        for section in data[key]["Sections"]:
            sections.append(section["Section Number"])
        class_list.append((key, sections))
    return class_list


def search_class(prefix, class_list):
    results = []
    for curr in class_list:
        class_name = curr[0]
        if class_name.upper().startswith(prefix.upper()):
            results.append(curr)
    return results
