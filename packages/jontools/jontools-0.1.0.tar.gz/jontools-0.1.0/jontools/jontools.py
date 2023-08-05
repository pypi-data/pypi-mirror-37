# Name: JonTools
# Import Name: jon_tools
# Description: Jon's Tools Duh

def create_list_index(model_values, unique_field_name='id'):
    index = {}
    for i in model_values:
        key = i[unique_field_name]
        if key not in index:
            index[key] = []
        index[key].append(i)
    return index