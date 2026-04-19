import random
result = random.randint(0,3)
names = ['ali', 'deniz','yaşar','cenk','selim','halil']
#result = names[random.randint(0, len(names)-1)]
result = random.choice(names)
greeting = 'Hello there'
result = random.choice(greeting)
liste = list(range(1,11))
random.shuffle(liste)
result = liste
liste = range(100)
result = random.sample(liste,10)

print(result)