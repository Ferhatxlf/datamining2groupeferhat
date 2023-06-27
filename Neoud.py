class arbre:
    def __init__(self, name):
        self.name = name
        self.etiquette_gauche = None
        self.etiquette_droit = None
        self.separation = None
        self.gauche = None
        self.droit = None

    def getseparation(self):
        return self.separation

    def getEtiquettegauche(self):
        return self.etiquette_gauche

    def getEtiquettedroit(self):
        return self.etiquette_droit

    def add_children(self, child):
        self.children.append(child)

    def add_values(self, value):
        self.values.append(value)

    def setSeparation(self, sep):
        self.separation = sep

    def setEtiquette_gauche(self, et):
        self.etiquette_gauche = et

    def setEtiquette_droit(self, et):
        self.etiquette_droit = et

    def insert_gauche(self, value):
        if self.gauche is None:
            self.gauche = arbre(value)
        else:
            noeud = arbre(value)
            noeud.gauche = self.gauche
            self.gauche = noeud

    def insert_droit(self, value):
        if self.droit == None:
            self.droit = arbre(value)
        else:
            noeud = arbre(value)
            noeud.droit= self.droit
            self.droit=noeud
