comparators = {
    '>':"__gt__",
    '<':"__lt__",
    '==':"__eq__",
    '!=':"__ne__",
    '>=':"__ge__",
    '<=':"__le__"
    }

x = input("x: ")
y = input("y: ")
comp = comparators.get("==")
result = x.__getattribute__(comp)(y)
print(result)
