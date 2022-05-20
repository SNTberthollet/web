# Programme écrit par M Tonnelier
import os
import glob
import re

# Code qui sert à parcourir le code HTML d'une page web ("parseur") :
from html.parser import HTMLParser
from xml.etree import cElementTree as etree

class MyHTMLParser(HTMLParser):
    
    # Le constructeur du parseur
    def __init__(self):
      HTMLParser.__init__(self)
      self.tb = etree.TreeBuilder() #On construit l'arbre des balises HTML
        
    def handle_starttag(self, tag, attributes):
      self.tb.start(tag, dict(attributes))

    def handle_endtag(self, tag):
      self.tb.end(tag)

    def handle_data(self, data):
      self.tb.data(data)

    def close(self):
      HTMLParser.close(self)
      return self.tb.close()     


# Erreurs
erreur_title = "/!\\ ATTENTION il manque la balise <title> /!\\"
erreur_h1 = "/!\\ ATTENTION il manque la balise <h1> /!\\"
erreur_index = "/!\\ ATTENTION il manque le fichier index.html /!\\"

# Code pour parcourir tous les répertoires des élèves :
repertoire="/tmp/dossier/"
page=""
for eleve in os.listdir(repertoire):
    index = False
    for fichier in os.listdir(repertoire+eleve):
        try:
            if(fichier.endswith(".html")):
                # On cherche le fichier index.html
                if(fichier == "index.html"):
                    index = True
                page=fichier
                parser = MyHTMLParser()
                f = open(repertoire+eleve+"/"+fichier)
                html = f.read()
                parser.feed(html)
                parser.reset() 
                arbre = parser.close()
                
                # On cherche le titre (balise title dans head)
                span = arbre.find(".//title")
                if span is None:
                    titre = erreur_title
                else:
                    titre = span.text
                    if(titre is None):
                        titre = erreur_title
                # On cherche le 1er titre principal (balise h1 dans body)
                span = arbre.find(".//h1")
                if span is None:
                    h1 = erreur_h1
                else:
                    h1 = span.text
                    if(h1 is None):
                        h1 =  erreur_h1
        except:
            titre = "ILLISIBLE !!!"
            h1 = ""
        
    if(index):
        print("<li><a href=\"" + eleve + "/\">"+eleve+" : "+titre+" - "+h1+"</a></li>\n")
    # Il manque le fichier index.html
    else:          
        print("<li><a href=\"" + eleve+"/"+page + "\">"+eleve+" : "+titre+" - "+h1+erreur_index+"</a></li>\n")
