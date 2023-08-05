from tojasteszter import test

#azt a számot kell visszaadni ami a legnagyobb és nem igaz rá, hogy törik
#ebben a tesztesetben ez 1-től 100-ig bármilyen egész szám lehet
#azt hogy törik-e a tojás, a paraméterként adott törik függvény segítségével derítheted ki
#a cél, hogy minél kevesebbszer kelljen ezt a függvényt meghívni
#illetve ebben a konkrét tesztesetben ha másodszor IGAZ értéket adott vissza a törik függvény
#nem lehet többször meghívni, mert csak két tojásunk van


def megoldas1(torik):
    for i in range(1,101):
        if torik(i):
            return i - 1
    return 100

test(megoldas1)

def megoldas2(torik):
    if torik(50):
        for i in range(1,50):
            if torik(i):
                return i - 1
        return 49
    else:
        for i in range(51,101):
            if torik(i):
                return i-1
        return 100

test(megoldas2)


def megoldas3(torik):
    if torik(50):
        if torik(25):
            for i in range(1,25):
                if torik(i):
                    return i - 1
            return 24
        else:
            for i in range(26,50):
                if torik(i):
                    return i - 1
            return 49
            
    else:
        for i in range(51,101):
            if torik(i):
                return i-1
        return 100

test(megoldas3)

