from app.model.config import Config
from app import taskList

def signQueue(userId: str):
    user = Config.get_or_none(Config.phone == userId)
    if user is None:
        return False
    user = user.__data__
    if user['enable'] is False:
        return False
    if user['planId'] is None or user['planId'] == "":
        return False
    if user['longitude'] is None or user['longitude'] == "":
        return False
    if user['latitude'] is None or user['latitude'] == "":
        return False
    if user['address'] is None or user['address'] == "":
        return False
    if user['enable'] == True:
        joinTask(userId)
        taskList.append(userId)
        
        
    
    
def joinTask():
    pass