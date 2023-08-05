import json
#import .fs_tools as fs_tools

def is_json(json_text):
  try:
    json_object = json.loads(json_text)
  except ValueError:
    return False
  return True    
  

def load_json(json_file):
  with open(json_file , encoding='utf-8') as json_fh:
    config = json.load(json_fh)
  return config    

def pretty_json(file=None,text=None) :

#  if file is None and text = None :
#    raise ValueError('pretty_json(file,text), at least one of (file,text) should not be None.')
    
#  json_text = text
  
#  if file is not None:
#    json_text = fs_tools.read_file(file)

#  if is_json(json_text) == False:
#    raise ValueError('pretty_json(file,text): The json text is invalid.') 
  return (json.dumps(json.loads(text), sort_keys=True, indent=2))
  
  
if __name__ == "__main__": 
  pass