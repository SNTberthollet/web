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
erreur_title = " /!\\ ATTENTION il manque la balise title /!\\"
erreur_h1 = " /!\\ ATTENTION il manque la balise h1 /!\\"
erreur_index = " /!\\ ATTENTION il manque le fichier index.html /!\\"
erreur_html = " /!\\ ERREUR dans la lecture du fichier HTML /!\\"
erreur_sous_repertoire = " /!\\ ATTENTION il ne doit pas y avoir de répertoire dans le dossier, que des fichiers /!\\"

# Code pour parcourir tous les répertoires des élèves :
repertoire="/tmp/eleves/Sites_web/"
page=""

repertoires=os.listdir(repertoire)
repertoires = sorted(repertoires)

for eleve in repertoires:
	index = False
	sous_repertoire = False
	css = False
	titre = ""
	h1 = ""
    

	fichiers = os.listdir(repertoire+eleve)
	index = "index.html" in fichiers
	page_accueil = "eleves/"+eleve

	for fichier in fichiers:
		chemin = repertoire+eleve+"/"+fichier
		# Vérifier s'il y a un sous-dossier
		sous_repertoire= not(os.path.isfile(chemin))
		if sous_repertoire:
			page_accueil+="/"+fichier+"/"
			break
		else:

			try:
				if(fichier.endswith(".css")):
					css = True
				
				# On parcourt le fichier si son extension est html
				if(fichier.endswith(".html")):
					page = fichier
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
			# Si le parcours de l'arbre HTML a échoué
			except:
				titre = erreur_html

	# Le fichier index.html est-il présent ?
	if(index):
		intitule = eleve+" : "+titre+" - "+h1
	else:
		page_accueil += "/"+page
		intitule = eleve+" : "+titre+" - "+h1+erreur_index
	if(sous_repertoire):
		intitule = "Il ne doit pas y avoir de sous-répertoire "+intitule
		url = chemin
      else:  
		url = "<a href=\""+ page_accueil+"\">"+page_accueil+"</a>"

	print("<tr>")
	print("\t<td>"+eleve+"</td>")
	print("\t<td>"+url+"</td>")
	if(sous_repertoire):
		print("\t<td>"+erreur_sous_repertoire+"</td>")
	else:
		print("\t<td>OK</td>")
	if(index):
		print("\t<td>Oui</td>")
	else:
		print("\t<td>Non</td>")
	print("\t<td>"+titre+"</td>")
	print("\t<td>"+h1+"</td>")
	if(css):
		print("\t<td>Oui</td>")
	else:
		print("\t<td>Non</td>")
	print("</tr>")

