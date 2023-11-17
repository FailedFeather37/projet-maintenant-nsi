import string
import lexer
from enum import Enum
import os
import subprocess




def parse_expression(l_actuel):
    if l_actuel[0]=="PARENTHESE_OUVERT":
       l_actuel=l_actuel[1:]
       node_gauche,l_actuel=parse_expression(l_actuel)

    elif isinstance(l_actuel[0], str):
       node_gauche=Chaine(l_actuel[0])
       label_instance_gauche=node_gauche.label()
       node_gauche_dot=f"x1[label = {l_actuel[0]}]"

    elif isinstance(l_actuel[0], int):
       node_gauche=Nombre(l_actuel[0])
       node_gauche_dot=f"x1[label = {l_actuel[0]}]"
    typecheck_gauche=node_gauche
    instance_chaine=typecheck_gauche.typecheck()
    l_actuel=l_actuel[1:]


    if l_actuel and l_actuel[0]!="PARENTHESE_FERME" and l_actuel[0] in ['+', '-', '*', '/']:
       dot_quote=l_actuel[0]
       dot_quote='"'+l_actuel[0]+'"'
       ope_dot=f"x2[label = {dot_quote}]"
       operation = l_actuel[0]
       with open(os.path.join("dot", "test.dot"), "w") as f:
        print("digraph { ", node_gauche_dot,"->",ope_dot, " }", file=f)

       l_actuel=l_actuel[1:]
       node_droite, l_actuel = parse_expression(l_actuel)
       instance_typecheck=Expression(node_gauche,operation,node_droite)
       typecheck=instance_typecheck.typecheck()

       return(Expression(node_gauche,operation,node_droite),l_actuel)

    return(node_gauche,l_actuel)



DOSSIER_DOT = "dot"
DOSSIER_IMAGE = "output"

DOT_EXEC = os.path.join("Graphviz", "bin", "dot.exe")

def creer_dossier(nom_dossier):
    os.makedirs(nom_dossier, exist_ok=True)

def creer_fichier_dot(nom_fichier, contenu_fichier):
    creer_dossier(DOSSIER_DOT)

    with open(os.path.join(DOSSIER_DOT, nom_fichier), "w") as f:
        print("digraph { ", contenu_fichier, " }", file=f)

def creer_image(nom_image, nom_fichier_dot):
    creer_dossier(DOSSIER_IMAGE)
    cmd = [DOT_EXEC, "-Tpng", os.path.join(DOSSIER_DOT, nom_fichier_dot), "-o", os.path.join(DOSSIER_IMAGE, nom_image)]
    subprocess.call(cmd)

def creer_image_depuis_contenu(nom, contenu):
    creer_fichier_dot(nom+".dot", contenu)
    creer_image(nom+".png", nom+".dot")

creer_fichier_dot("test.dot", "A -> 51")
creer_image("test.png", "test.dot")
creer_image_depuis_contenu("test2", "x1[label = {l_actuel[0]}]; x1 -> 51")


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
      def label(self):
          return(self.nombre)

class Chaine(NoeudAST):
      def __init__(self,chaine):
          self.chaine=chaine

      def typecheck(self):
            return(Type.CHAINE)

      def label(self):
            return(self.chaine)

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
print(parse_expression(l_actuel))


if l_actuel:
      arbre, liste = parse_expression(l_actuel)
      instance_fin=arbre
      print(instance_fin.affichage())

      if arbre:
        print("Arbre créé")
else:
      print("Liste vide")



