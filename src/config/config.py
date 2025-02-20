import json 

#this function reads and returns config.json which has database connection URI 
def load_config():
    with open(r'config.json') as f:
        data = json.load(f)
        return dict(data)




