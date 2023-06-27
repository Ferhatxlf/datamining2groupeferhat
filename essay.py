def predict(self, racine, data, att, pr=None):
    if racine != None:
        if racine.etiquette_gauche != None:
            print('gauche', racine.etiquette_gauche)
            pr = racine.getEtiquettegauche()

        elif racine.etiquette_droit is not None:
            print('droit', racine.etiquette_droit)
            pr = racine.getEtiquettedroit()
        else:
            for i in range(len(att)):
                if att[i] == racine.name:
                    condidat = i
            if data[condidat] <= racine.separation:
                self.predict(racine.gauche, data, att, pr)
            else:
                self.predict(racine.droit, data, att, pr)

    return pr