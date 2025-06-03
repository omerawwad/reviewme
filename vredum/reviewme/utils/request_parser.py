def get_page_details(parameters):
    """
    Extracts pagination details from the request parameters.
    """
    print("Parameters received for pagination:", parameters)
    
    if 'page' in parameters:
        try:
            page = int(parameters.get('page'))
        except ValueError:
            page = 1
    else:
        page = 1

    if 'size' in parameters:
        try:
            size = int(parameters.get('size'))
        except ValueError:
            size = 10
    else:
        size = 10

    if page < 1:
        page = 1

    if size < 1:
        size = 10

    # TODO: Add sorting functionality


    return page, size

def get_notification_id(parameters):
    """
    Extracts notification ID from the request parameters.
    """
    if 'notification_id' in parameters:
        try:
            notification_id = int(parameters.get('notification_id'))
            return notification_id
        except ValueError:
            return None
    return None