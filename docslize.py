import random
from source import CATEGORIES, collect

unique_ids = {}

print('Welcome to docslize')
print('Please choice and enter the id of document you want to download : ')
print()
for cat, subs in CATEGORIES.items():
    print((' '*2)+'[*] '+cat)
    for s, v in subs.items():
        uniqueid = str(random.randint(111, 999))
        print((' '*5)+'|--['+uniqueid+'] '+s)
        unique_ids[uniqueid] = v
    print()

first_time_alert = False
while True:
    i = input("[ID] >> ")
    if i not in unique_ids:
        print((' '*2)+'[ERROR] Invalid id')
        continue
    if not first_time_alert:
        print((' '*2)+'Note: documents are download in "collected" folder.')
        first_time_alert = True
    try:
        collect.Collect(unique_ids[i])
    except:
        print('An error occurred !')
