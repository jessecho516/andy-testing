import csv
import json
 
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = {}
    rowCounter = 1
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            newRow = {}
            #create newRow with spaces stripped
            for key in rows:
                newRow[key.strip()] = rows[key]

            # use rowCounter as primary key
            key = rowCounter
            rowCounter += 1

            data[key] = newRow
 
    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


# Driver Code
 
# Decide the two file paths according to your
# computer system
# csvFilePath = 'CS_Classes.csv'
# jsonFilePath = 'webscraper_data.json'
 
# # Call the make_json function
# make_json(csvFilePath, jsonFilePath)

         
#create classes.json 
import collections 

def make_classes_json(webscraperJson, classesJson):
    webscraper_file = open(webscraperJson)
    data = json.load(webscraper_file)
    class_data = {}

    for key in data:
        curr = data[key]
        class_code = curr["Class Code"]
        section_num = curr["Section #"]
        class_title = curr["Class Title"]
        credit_hours = curr["Credit Hours"]
        times = curr["Times"]
        #Fill in later
        class_rating = "5.0"

        if class_code not in class_data: #if we're reading new class
            class_data[class_code] = {}
            class_data[class_code]["Class Title"] = class_title
            class_data[class_code]["Credit Hours"] = credit_hours
            class_data[class_code]["Class Rating"] = class_rating


            class_data[class_code]["Sections"] = []

        curr_section = {"Section Number" : section_num, "Times" : times}
        class_data[class_code]["Sections"].append(curr_section)
    

    with open(classesJson, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(class_data, indent=4))



# webscraperJson = 'webscraper_data.json'
# classesJson = 'classes.json'

# make_classes_json(webscraperJson, classesJson)


def make_professors_json(webscraperJson, professorJson, ratingCsv):
    webscraper_file = open(webscraperJson)
    data = json.load(webscraper_file)
    professor_data = {}

    for key in data:
        curr = data[key]
        class_code = curr["Class Code"]
        section_num = curr["Section #"]
        class_title = curr["Class Title"]
        credit_hours = curr["Credit Hours"]
        times = curr["Times"]
        professor_name = curr["Professors"]
        #to be filled
        professor_rating = "5.0"

        if professor_name not in professor_data: #if we're reading new professor
            professor_data[professor_name] = {}
            professor_data[professor_name]["Professor Rating"] = professor_rating

            professor_data[professor_name]["Courses"] = []

        curr_course = {"Class Title" : class_title, "Section Number" : section_num, "Times" : times}
        professor_data[professor_name]["Courses"].append(curr_course)

    with open(ratingCsv, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            newRow = {}
            print(rows)
            #create newRow with spaces stripped



    with open(professorJson, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(professor_data, indent=4))

# webscraperJson = 'webscraper_data.json'
# professorJson = 'professors.json'

# make_professors_json(webscraperJson, professorJson)



