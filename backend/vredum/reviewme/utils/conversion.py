from . import dbcomm


# def convert_ids_to_int(ids):
#     print(f"Converting IDs: {ids}")
#     converted_ids = []
#     for id in ids:
#         try:
#             converted_ids.append(int(id))
#         except ValueError:
#             print(f"Invalid ID: {id}")
#             continue
#     print(f"Converted IDs: {converted_ids}")
#     return converted_ids

# def convert_get_ids_tags(ids):
#     tags = []
#     for id in ids:
#         try:
#             tags.append(dbcomm.get_tag_by_id(id))
#         except ValueError:
#             print(f"Invalid ID: {id}")
#             continue
#     return tags

def check_item_id(item_id):
    item = dbcomm.get_item_by_id(item_id)
    if item:
        return True
    else:
        return False

def check_tags(tags):
    valid_tags = []
    warnings_from_checking_tags = []
    for tag in tags:
        if dbcomm.get_Tag(tag):
            valid_tags.append(tag)
        else:
            warnings_from_checking_tags.append(f"Tag '{tag}' does not exist.")
            # print(f"Tag '{tag}' does not exist.")

    return valid_tags, warnings_from_checking_tags