from itertools import chain, combinations

arr = [
    'sg9',
    'si1',
    'sq9',
    'st7',
    'sb6',
    'sl1'
]

for i in range(len(arr)+1):
    for item in list(combinations(arr,i)):
        item = str(item)[2:-2].replace("'", "").replace(",","")
        print(f"so0 se3 sa4 ss5 {item}")