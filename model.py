import math
from Neoud import arbre


class Model:
    def __init__(self):
        self.__x = None
        self.__y = None

    def entropie(self, s):
        H = 0
        nbr1 = s.count(1)
        nbr0 = s.count(0)
        s1 = 0
        s2 = 0
        if nbr1 != 0:
            s1 = (nbr1 / len(s)) * math.log(nbr1 / len(s), 2)
        if nbr0 != 0:
            s2 = (nbr0 / len(s)) * math.log(nbr0 / len(s), 2)
        H = -(s1 + s2)
        return round(H, 3)

    def gain_info(self, l):
        l1 = list(set(l))
        s = 0
        for i in l1:
            list_lg = []
            for j in range(len(l)):
                if l[j] == i:
                    list_lg.append(self.__y[j])
            s += self.entropie(list_lg) * (l.count(i) / len(l))

        return round(self.entropie(self.__y) - s, 3)

    def Attribut_Continue(self, l, m=None):
        l1 = list(set(l))
        l1.sort()
        gi = []
        m = 1
        for i in range(1, len(l1)):
            part_1 = l1[:i]
            part_2 = l1[i:]
            s = 0
            s1 = 0
            lis_1 = []
            lis_2 = []
            prob1 = 0
            prob2 = 0
            for k in part_1:
                for j in range(len(l)):
                    if l[j] == k:
                        prob1 += 1
                        lis_1.append(self.__y[j])
            s += self.entropie(lis_1) * prob1 / len(l)

            for z in part_2:
                for j in range(len(l)):
                    if l[j] == z:
                        prob2 += 1
                        lis_2.append(self.__y[j])
            s1 += self.entropie(lis_2) * prob2 / len(l)
            gi.append(round(self.entropie(self.__y) - s1 - s, 3))

            maximum = max(gi)
            for p in range(len(gi)):
                if gi[p] == maximum:
                    m = l1[p]
        return m

    def indice_gain_maximum(self, data):
        max = 0
        indice = 0
        for i in range(len(data)):
            g = self.gain_info(data[i])
            if max < g:
                max = g
                indice = i
        return indice

    def fit(self, x: [], y: []):
        self.__x = x
        self.__y = y

        att = ["GRE_Score", "TOEFL_Score", "University_Rating", "SOP", "LOR", "CGPA", "Research"]
        data = [[], [], [], [], [], [], []]

        for i in range(len(x)):
            for j in range(len(data)):
                data[j].append(x[i, j])

        indice = self.indice_gain_maximum(data)
        Noeud = arbre(att[indice])
        Noeud.setSeparation(self.Attribut_Continue(data[indice]))

        R = self.essay(Noeud, indice, data, att)
        return R

    def predict(self, racine, data, att, pr=[]):
        for i in range(len(att)):
            if att[i] == racine.name:
                condidat = i
        if data[condidat] <= racine.separation:
            if racine.etiquette_gauche is not None:
                pr.append(racine.etiquette_gauche)

            elif racine.gauche is not None:
                self.predict(racine.gauche, data, att, pr)

        else:
            if racine.etiquette_droit is not None:
                pr.append(racine.etiquette_droit)
            elif racine.gauche is not None:
                self.predict(racine.droit, data, att, pr)
        return pr

    def essay(self, Noeud, indice, data, att, class_maj=1, learning_rate=0.5):
        if len(data) > 0:

            y_part_1 = []
            y_part_2 = []
            data_inf_separation = []
            data_sup_separation = []
            for i in range(len(data)):
                data_inf_separation.append([])
                data_sup_separation.append([])

            for i in range(len(data[indice])):
                if data[indice][i] <= Noeud.getseparation():
                    y_part_1.append(self.__y[i])
                    for j in range(len(data)):
                        data_inf_separation[j].append(data[j][i])
                else:
                    y_part_2.append(self.__y[i])
                    for j in range(len(data)):
                        data_sup_separation[j].append(data[j][i])

            if len(y_part_1) == 0:
                Noeud.setEtiquette_gauche(class_maj)
            elif len(y_part_1) == 1:
                if y_part_1.count(0) != 0:
                    Noeud.setEtiquette_gauche(0)
                else:
                    Noeud.setEtiquette_gauche(1)
            elif y_part_1.count(1) / len(y_part_1) >= learning_rate:
                Noeud.setEtiquette_gauche(1)
            elif y_part_1.count(0) / len(y_part_1) >= learning_rate:
                Noeud.setEtiquette_gauche(0)
            else:
                data_inf_separation.remove(data_inf_separation[indice])
                att.remove(att[indice])
                i = self.indice_gain_maximum(data_inf_separation)

                noeud = arbre(att[i])
                noeud.setSeparation(self.Attribut_Continue(data_inf_separation[i]))
                Noeud.gauche = noeud
                if y_part_1.count(0) >= y_part_1.count(1):
                    class_maj = 0
                else:
                    class_maj = 1
                self.essay(Noeud.gauche, i, data_inf_separation, att, class_maj)

            if len(y_part_2) == 0:
                Noeud.setEtiquette_droit(class_maj)
            elif len(y_part_2) == 1:
                if y_part_2.count(0) != 0:
                    Noeud.setEtiquette_droit(0)
                else:
                    Noeud.setEtiquette_droit(1)
            elif y_part_2.count(1) / len(y_part_2) >= learning_rate:
                Noeud.setEtiquette_droit(1)
            elif y_part_2.count(0) / len(y_part_2) >= learning_rate:
                Noeud.setEtiquette_droit(0)
            else:
                data_sup_separation.remove(data_sup_separation[indice])

                i = self.indice_gain_maximum(data_sup_separation)
                att.remove(att[indice])
                noeud = arbre(att[i])
                noeud.setSeparation(self.Attribut_Continue(data_sup_separation[i]))

                Noeud.droit = noeud
                if y_part_2.count(0) >= y_part_2.count(1):
                    class_maj = 0
                else:
                    class_maj = 1
                self.essay(Noeud.droit, i, data_sup_separation, att, class_maj)

            return Noeud

    def predict_all(self, racine, data, att):
        predictions = []
        for d in data:
            predictions.append(self.predict(racine, d, att))

        return predictions
