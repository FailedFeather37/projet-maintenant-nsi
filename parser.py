import string
import lexer
from enum import Enum


def parse_expression(l_actuel):
    if l_actuel[0]=="PARENTHESE_OUVERT":
       l_actuel=l_actuel[1:]

       node_gauche,l_actuel=parse_expression(l_actuel)

    elif isinstance(l_actuel[0], str):
       node_gauche=Chaine(l_actuel[0])

    elif isinstance(l_actuel[0], int):
       node_gauche=Nombre(l_actuel[0])
    typecheck_gauche=node_gauche
    instance_chaine=typecheck_gauche.typecheck()
    l_actuel=l_actuel[1:]


    if l_actuel and l_actuel[0]!="PARENTHESE_FERME" and l_actuel[0] in ['+', '-', '*', '/']:

       operation = l_actuel[0]
       l_actuel=l_actuel[1:]
       node_droite, l_actuel = parse_expression(l_actuel)
       instance_typecheck2=Expression(node_gauche,operation,node_droite)
       typecheck2=instance_typecheck2.typecheck()

       return(Expression(node_gauche,operation,node_droite),l_actuel)

    return(node_gauche,l_actuel)




class Type(Enum):
      NOMBRE=1
      CHAINE=2


class Parenthese(Enum):
      PARENTHESE_OUVERT=3
      PARENTHESE_FERME=4




class NoeudAST():
      pass

class Nombre(NoeudAST):
      def __init__(self,nombre):
          self.nombre=nombre

      def typecheck(self):
          return(Type.NOMBRE)

class Chaine(NoeudAST):
      def __init__(self,chaine):
          self.chaine=chaine

      def typecheck(self):
            return(Type.CHAINE)

class Expression(NoeudAST):
      def __init__(self,gauche,operation,droite):
          self.gauche=gauche
          self.operation=operation
          self.droite=droite

      def typecheck(self):
          if self.gauche.typecheck()==self.droite.typecheck():
              return(self.droite.typecheck())
          else:
              return(None)

      def affichage(self):
          if self.droite.typecheck()!=None:
             return("Expression valide")
          else:
             return("Expression invalide")


contenu=lexer.nom_fichier()
l_actuel=lexer.lexer(contenu)
#print(parse_expression(l_actuel))


if l_actuel:
    arbre, liste = parse_expression(l_actuel)
    instance_fin=arbre
    print(instance_fin.affichage())

    if arbre:
        print("Arbre créé")
else:
    print("Liste vide")





