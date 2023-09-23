import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def getNextProbableWords(classes, statements):
    # Convert the class from list to dict
    class_dict = {}
    for c in classes:
        for key, value in c.items():
            class_dict[key] = value

    def get_next_words(statement):
        # Split the statement based on the . location
        parts = statement.split('.')
        # Case where the last part is empty
        if parts[-1] == '':
            # There should be 3 cases, 1. Dict, 2. List, 3. String
            # After the first dictionary search, the output should be one of the above
            if parts[0] in class_dict and isinstance(class_dict[parts[0]], dict):
                # use the initial dictionary to search for the next dictionary
                current_dict = class_dict[parts[0]]
                for part in parts[1:-1]:
                    if part in current_dict and isinstance(current_dict[part], dict):
                        current_dict = current_dict[part]
                    elif part in current_dict and isinstance(current_dict[part], list):
                        return sorted(current_dict[part])[:5]
                    else:
                        return [""]
                return sorted(list(current_dict.keys()))[:5]
            # Assume that there shouldn't be any dictionary included in the list
            # As the permutation, it was told that it was a list of strings
            elif parts[0] in class_dict and isinstance(class_dict[parts[0]], list):
                return sorted(class_dict[parts[0]])[:5]
            # Case where the first part is a empty string
            else:
                return [""]
        # Case where the last part is another word
        elif parts[-1] != '':
            # Case where the first part is a dictionary - similar to the first part
            if parts[0] in class_dict and isinstance(class_dict[parts[0]], dict):
                current_dict = class_dict[parts[0]]
                for part in parts[1:-2]:
                    if part in current_dict and isinstance(current_dict[part], dict):
                        current_dict = current_dict[part]
                    elif part in current_dict and isinstance(current_dict[part], list):
                        type_name = current_dict[part]
                        return sorted(class_dict[type_name])[:5]
                    else:
                        return [""]
                # Add the case where we want to find which sub-dictionary the last part belongs to
                if parts[-2] in current_dict and isinstance(current_dict[parts[-2]], dict):
                    type_name = current_dict[parts[-2]]
                    if type_name.startswith('List<') and type_name.endswith('>'):
                        type_name = type_name[5:-1]
                    if type_name in class_dict:
                        if isinstance(class_dict[type_name], dict):
                            return sorted(list(class_dict[type_name].keys()))[:5]
                        elif isinstance(class_dict[type_name], list):
                            return sorted(class_dict[type_name])[:5]
                        else:
                            return [""]
                    else:
                        return [""]
                elif parts[-2] == parts[0]:
                    return sorted([x for x in class_dict[parts[0]] if x.startswith(parts[-1])])[:5]
                else:
                    return sorted([key for key in current_dict[parts[-2]] if key.startswith(parts[-1])])[:5]
            # Any list returns
            elif parts[0] in class_dict and isinstance(class_dict[parts[0]], list):
                return sorted([x for x in class_dict[parts[0]] if x.startswith(parts[-1])])[:5]
            else:
                return [""]
        else:
            return [""]

    result = {}
    for statement in statements:
        result[statement] = get_next_words(statement)

    return result

@app.route('/lazy-developer', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data.get("input")
    classes = data["classes"]
    statements = data["statements"]
    
    result = getNextProbableWords(classes, statements)
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)
