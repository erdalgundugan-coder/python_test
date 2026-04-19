import json

# person_string = '{"name":"ali","languages":["python","c#"]}'
person_dict = {"name":"ali","languages":["python","c#"]}
with open("person.json","w") as f:
    json.dump(person_dict,f)
# # # json string t dict
# # # result = json.loads(person_string)
# # # result = result["name"]
# # # print(type(result))
with open("person.json") as f:
    dat = json.load(f)
    print(dat["name"])
# #     print(dat["languages"][0])
# # #     print(dat["languages"][1])
# # dict to json cevirdik

# # person_dict = {
# #    "name":"ali",
# #    "languages":["python","c#"]
# #    }
# # # result = json.dumps(person_dict)
# # # print(type(result))
# # # print(result)
# # # dosyaya yazdık
# # with open("person.json","w") as f:
# #     json.dump(person_dict,f)
# person_dict = json.loads(person_string)
# result = json.dumps(person_dict, indent=2, sort_keys= True)
# print(person_dict)
# print(result)