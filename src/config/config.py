import json 

#this function reads and returns config.json 
def load_config():
    with open(r'src\\config\\config.json') as f:
        data = json.load(f)
        return dict(data)




