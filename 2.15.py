dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}

result = dict1.copy()
result.update(dict2)

print("Combined dictionary:", result)