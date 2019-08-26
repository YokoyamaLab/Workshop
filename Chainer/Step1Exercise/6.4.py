import numpy.random as random

success = 0

for v in range(60466176):

    if v % 100000 == 0:
        print("loading...")

    dice = random.randint(1,7)
    #print(dice)
    count = 0

    for i in range(9):
        value = random.randint(1,7)
        #print(value)
        #print()

        if value > dice:
            a = 1
            #print("lucky!")

        else:
            count = count + 1
            #print("non lucky...")

        dice = value

    #print(count)

    if count == 10:
        last = random.randint(1,7)

        if last > dice:
            success = success + 1

print(success)