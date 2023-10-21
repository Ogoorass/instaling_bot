

#---queue---
lista_kont = []
try:
    with open("lista_kont.txt", "r") as f:
        for line in f:
            lista_kont.append(line.strip('\n').split())
except FileNotFoundError:
    print("Nie znaleziono pliku z lisą kont!\n")
    exit(1)

print(lista_kont)

#---iteracja przez queue---
#logowanie
#rozpocznij sesje dzeiną

#---zrób sesję kożystając z bazy dancyh słówek---

