import json

def store_data(path,data):
    '''
    store data into a json file
    @param path: path to the json file
    @param data: data that user want to store
    '''
    with open (path, 'w') as fp:
        json.dump(data,fp)
        

def load_data(path):
    '''
    load data from a json file
    @param path: path to the json file
    @return data stored in the json file
    '''
    with open (path, 'r') as fp:    
        return (json.load(fp))
        
    