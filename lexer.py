import string
from enum import Enum


def nom_fichier():
    with open("calcul.py",encoding="utf-8")as fichier:
        l=fichier.read()
    return(l)



def parse_nombre(texte):
    ord_liste=[48,49,50,51,52,53,54,55,56,57]
    L=[]
    for c in texte:
        c=ord(c)
        if c==65279 or c==34:
            continue
        if 48<=c<=57:

            c-=ord("0")
            L.append(c)
        else:
            break
    p=0
    for i in range(len(L)):
        p+=L[i]*10**(len(L)-1-i)
    if p==0:
       return(None)
    else:
         return(p,len(L))



def lire_espaces(texte):
    compteur=0
    for c in texte:
        if c==" ":
           compteur+=1
    return(compteur)



def parse_chaine(texte):
    L = ""
    in_quotes = False
    for c in texte:
        if c == '"':
            in_quotes = not in_quotes
        elif in_quotes:
            L += c
        elif L:
            break
    return(L,len(L))



def parse_operation(texte):
    list_ope=['+','-','/','*']
    for c in texte:
        if c in list_ope:
           return(c,1)



def lexer(texte):
    l=[]
    texte_actuel=texte

    while texte_actuel:
          if texte_actuel[0]=="(":
             l.append(PARENTHESE.PARENTHESE_OUVERT.name)

          if texte_actuel[0]==")":
             l.append(PARENTHESE.PARENTHESE_FERME.name)
             texte_actuel=texte_actuel[1:]

          if texte_actuel[0] in ['+','-','/','*']:
             q,r=parse_operation(texte_actuel)
             l.append(q)
             texte_actuel=texte_actuel[r:]

          elif texte_actuel[0].isdigit():
             a,p=parse_nombre(texte_actuel)
             l.append(a)
             texte_actuel=texte_actuel[p:]

          elif texte_actuel[0] == '"' or texte_actuel[0] == "'":
             b,m=parse_chaine(texte_actuel)
             texte_actuel=texte_actuel[m+2:]
             l.append(b)

          else:
               texte_actuel=texte_actuel[1:]

    return(l)


class PARENTHESE(Enum):
      PARENTHESE_OUVERT=3
      PARENTHESE_FERME=4


def main():
    texte=nom_fichier()
    print(lexer(texte))



if __name__=="__main__":
    main()