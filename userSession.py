loggedInUser = None

def set_loggedInUser(username):
    global loggedInUser
    loggedInUser = username

def get_loggedInUser():
    return loggedInUser

def clear_loggedInUser():
    global loggedInUser
    loggedInUser = None
