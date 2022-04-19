import json 
import os
current_file_path = __file__
current_file_dir = os.path.dirname(__file__)
class_json_path = os.path.join(current_file_dir, "json", "classes.json")

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

def filter_search(searched):
    class_list = make_class_list(class_json_path)
    results = search_class(searched, class_list)
    return results
