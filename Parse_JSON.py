import pandas as pd
import json
from ast import literal_eval

def recur_eval(x):
    match x:
        case list():
            return [recur_eval(item) for item in x]
        case dict():
            return {k:recur_eval(v) for k,v in x.items()}
        case str():
            try:
                return literal_eval(x)
            except (ValueError, SyntaxError):
                return x
        case _:
            return x

records = [recur_eval(json.loads(line)) for line in open('path/filename')]
dataframe = pd.json_normalize(records)
rename = {value: value.split('.')[-1].replace('@', '') for value in dataframe.columns}
dataframe.rename(columns=rename, inplace=True)
#print(dataframe)

dataframe.to_csv('csv_filename', index=False, mode='w')

