#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

@AUTHOR=UKWLE@STUDENT.KIT.EDU

'''



import copy

import time

import numpy as np

import random

import pandas as pd


'''


Beschreibung Modell:

-Graph G = (V, E)

- jeder Knoten v ist durch 2 Koordinaten bestimmt (x_v,y_v)
- v kann ein Startpunkt o, Abholpunkt p oder ein Ziel d ein 
- eine Kante e ist die Verbindung zwischen zwei Knoten

-jeder Fahrer mit privatem Fahrzeug f hat einen eindeutigen Start- und Zielpunkt

-Q_f Anfangskapazität eines Fahrzeugs= Anzahl freier Plätze

-at_v festgelegte Ankunftszeit am Ziel

-An jedem Abholpunkt wartet eine Anzahl an Fahrgästen, wobei jeder Fahrgast ein eindeutiges Ziel und eine 
potentielle Entlohnung r_p,Fahrgast bei der Mitnahme für den Fahrer besitzt


'''

'''

Generierung der Instanzen laut Paper:


-Koordinaten für jeden Abholort: für x und y Koordinate aus gleichmäßiger Verteilung im Bereich [1,85]
-Koordinaten für jeden Stratpunkt: x auf 1 festgelegt und y aus gleichmäßiger Verteilung im Bereich [1,85]
-Koordinaten für jeden Endpunkt: x auf 85 fetsgelegt und y aus gleichmäßiger Verteilung im Bereich [1,85]

-Honorar des Fahrers: aus gleichmäßigen Verteilungen im Bereich [10,40] für jeden Fahrgast

-Anzahl der abzuholenden Fahrgäste: aus gleichmäßigen Verteilungen im Bereich [1,2]
-Ziel jedes Fahrgastes und jedes Fahrzeuges: zufällige Auswahl aus vorhanden Zielen

-Unterscuhung Instanzen:
    -Gruppe 1, p1 bis p10: Jede Instanz besteht aus 6 Startpunkte, 2 Zielorten und 64 Abholorten. 
    -Gruppe 2, p11 bis p15: Jede Instanz besteht aus 12 Startpunkte, 4 Zielorten und 200 Abholorten
    -Gruppe 3, p16 bis p20: Jede Instanz besteht aus 24 Startpunkte, 8 Zielorten und 500 Abholorten
    
-Jedem Startpunkt ist ein Fahreug zugeordnet mit einer Anfangskapazität Q_f
-Q_f beträgt 4, 6 oder 8 und wird gleichmäßig auf die vorhandenen Fahrzeuge verteilt. Bsp: bei 6 Fahrzeugen haben 2 eine 
 Kapazität von 4, 2 eine Kapazität von 6 und 2 eine Kapazität von 8 Plätzen

-Die maximale Fahrtzeit at_f ist für alle auf 100 Zeiteinheiten festgelegt.

'''

seed_nr = 0 #setzt einen Seed für die Generierung einer Probleminstanz
distanz_faktor = 1 #Faktor um die Distanz in Zeiteinheiten umzuwandeln; Wert 1 entspricht euklidischer Distanz

'''

Generierung der Zielpunkte

'''

random.seed(seed_nr)
counter = 1
D = [] #Menge aller Zielpunkte

while counter <= 2:

    yd = random.randint(1, 85)

    name = 'd_' + str(counter)

    exec('d' + str(counter) + ' = [name, 85, yd]')

    exec('D.append(d' + str(counter) + ')')

    counter += 1

'''

Generierung der Abholpunkte

'''

'''

   Überblick der Listenelemente als Information über ein Abholpunkt p:

    p[0]: Name des Abholpunktes, z.B. p_1

    p[1]: x-Koordinate

    p[2]: y-Koordinate

    p[3]: Anzahl der Fahrgäste, die am Abholpunkt p warten 

    p[4]: alle Entlohnungen als Liste abgespeichert für die Fahrgäste am Abholpunkt p, z.B. p[4][0] speichert 
          Entlohnung ab, die der 1. Fahrgast am Abholpunkt p bei Mitnahme in einem Fahrzeug zahlt 

    p[5]: alle Zielorte als Liste abgespeichert für die Fahrgäste am Abholpunkt p, z.B. p[5][0] speichert Zielort des 
          1. Fahrgastes am Abholpunkt p ab 

'''


P = [] #Menge aller Abholpunkte

counter = 1

while counter <= 64:

    p_x = random.randint(1, 85)

    p_y = random.randint(1, 85)

    name = 'p_' + str(counter)

    n_p = random.randint(1, 2) #Zuweisung Anzahl Fahrgäste zu einem Abholpunkt p

    d_p = []

    r_p = []

    for n in range(0, n_p): #Abhängig von der Anzahl an wartenden Fahrgästen am Abholpunkt p wird jedem Fahrgast ein Ziel und eine Belohnung zugeteilt

        d_p.append(random.choice(D)) #Fahrgast an einem Abholort p wird zufällig ein Zielort zugewiesen

        r_p.append(random.randint(10, 40)) #Fahrgast an einem Abholpunkt p wird Belohnung für Fahrer zugewiesen

    P.append([name, p_x, p_y, n_p, r_p, d_p])  #Informationen eines Abholpunktes p aus der Menge P

    counter += 1

'''

Generierung Fahrzeuge

'''

Fahrzeug = [] #Menge aller Fahrzeuge

counter = 1

while counter <= 6:
    name = 'f_' + str(counter)

    Fahrzeug.append([name])

    counter += 1

Q_f = [4, 4, 6, 6, 8, 8] #Auswahlmöglichkeiten für Kapazitäten für die Fahrzeuge

for f in Fahrzeug:

    f.append(random.choice(D))

    nr2 = random.randint(0, len(Q_f) - 1)

    f.append(Q_f[nr2])

    Q_f.remove(Q_f[nr2])

    f.append(0)

    f.append(0)

    f.append(0)


'''

Generierung Startpunkte und Zuweisung eines Fahrzeugs

'''

O = [] #Menge aller Startpunkte

counter = 1

while counter <= 6:

    o_y = random.randint(1, 85)

    name = 'o_' + str(counter)

    nr = random.randint(0, len(Fahrzeug) - 1) #zufällige Zuweisung eines Fahrzeugs

    exec('o' + str(counter) + ' = [name, 1, o_y, Fahrzeug[nr]]')

    Fahrzeug.remove(Fahrzeug[nr]) #nach Zuweisung löschen des Fahrzeugs aus Liste, damit Fahrzeug nicht noch einmal verwendet werden kann

    exec('O.append(o' + str(counter) + ')')

    counter += 1


'''

   Überblick der Listenelemente als Information über ein Fahrzeug f:

    f[0]: Name des Fahrzeugs, z.B. f_1

    f[1]: Ziel des Fahrzeugs

    f[2]: Kapazität des Fahrzeugs

    f[3]: aktuelle Anzahl der Fahrgäste im Fahrzeug

    f[4]: bisherige akkumulierte Entlohnung für den Fahrer des Fahrzeugs

    f[5]: bisher verbrauchte Fahrtzeit

'''


'''

-Aufteilung in Teilprobleme

-Ein Teilproblem beinhaltet alle Knoten mit Fahrgästen, welche dasselbe Fahrtziel besitzen

'''


for k in range(1, len(D) + 1): #Wählt ein Zielpunkt aus

    exec('Teilproblem' + str(k) + ' = []') #Erstellen eines Teilproblems

    for p in P: #Wählt einen Abholpunkt aus

        r_p = []

        ind = -1

        counter = 0

        for i in p[5]: #wählt für jeden Fahrgast am Abholpunkt p den Zielort aus

            fertig = False

            ind += 1

            if i == D[k - 1]:    #wenn der Zielort zum momentan betrachteten Teilproblem gehört

                r_p.append(p[4][ind]) #nur Belohnung der Fahrgäste eines Abholpunktes p, die zum Teilproblem gehören, werden gespeichert

                counter += 1 #Anzahl der Fahrgäste am Abholpunkt p, die zum Teilproblem gehören

                a = i.copy()

        fertig = True

        if fertig == True and counter != 0:
            exec('Teilproblem' + str(k) + '.append([p[0], p[1], p[2], counter, r_p, a])')


#Initialaisierung durch Erstellung einer Startlösung: jeder Abholpunkt in einer machbaren Route enthalten mit Start, Abholpunkt, Ziel:

init_routen = []

for k in range(1, len(D) + 1):

    for p in eval('Teilproblem' + str(k)): # Initialisierung ist für jedes Teilproblem seperat

        machbar = False

        if machbar == False:
            O_auswahl = copy.deepcopy(O)
            i=0
            while i <= len(O):
                if len(O_auswahl) != 0:
                    o = random.choice(O_auswahl) #wählt Startpunkt einer Route zufällig aus
                    O_auswahl.remove(o) #Startpunkte werden gleichmäßig unter die Routen aufgeteilt
                    f = copy.deepcopy(o)
                    i += 1
                if len(O_auswahl) == 0:
                    O_auswahl = copy.deepcopy(O)

                if machbar == False:
                    if o[3][1] == p[5]:

                        c = (np.sqrt((o[1] - p[1]) ** 2 + (o[2] - p[2]) ** 2))/distanz_faktor + (

                            np.sqrt((p[5][1] - p[1]) ** 2 + (p[5][2] - p[2]) ** 2))/distanz_faktor  #Berechnung der Fahrzeit zwischen 2 Knoten

                        if c <= 100 and p[3] <= o[3][2] - p[3]:  #Wenn Zeitfenster und Kapazität eingehalten werden

                            machbar = True

                            f[3][2] = o[3][2] - p[3] #Kapazität eines Fahrzeugs wird aktualisiert

                            f[3][3] = o[3][3] + p[3] #aktuelle Anzahl der Fahrgäste in einem Fahrzeug wird aktualisiert

                            f[3][4] = np.sum(p[4]) #Belohnung für den Fahrer durch Mitnahme der Fahrgäste an diesem Abholpunkt wird summiert und aktualisiert

                            f[3][5] = c #verbrauchte Fahrtzeit wird abgespeichert

                            init_routen.append({'Teilproblem': 'Teilproblem' + str(k), 'Fahrzeug': f,

                                                'Abholort': p, 'Ziel': o[3][1]})


def stochastische_Reisezeiten_zufuegen(loesung, anzahl_simulationen):
    '''
    Hinzufügen von stochastichen Reisezeiten zu einer vorgeschlagenen Lösung unter Angabe der Anzahl der Simulationsdurchläufe

    Ergebnis ist folgend aufbaut für jedes Fahrzeug:
    1. Position der Liste: Name des Fahrzeugs
    2. Position der Liste: Anzahl Verpätungen
    restliche Positionen: generierte Werte für stochastische Reisezeit
    '''

    def lognormal(m, var):  # Log-normale Wahrscheinlichkeitsverteilung

        if m == 0.0:  # Problembehandlung, falls 2 Abholpunkte genau dieselben Koordinaten besitzen, da 0.0 ungültig ist
            m = 0.0000000000001
        s = np.sqrt(var)
        mean = np.log(m ** 2 / np.sqrt(m ** 2 + s ** 2))
        sd = np.sqrt(np.log((m ** 2 + s ** 2) / m ** 2))
        a = np.random.lognormal(mean=mean, sigma=sd)
        return a

    F = []

    for o in range(1, len(O) + 1):
        exec('f' + str(o) + '= ["f_' + str(o) + '", 0]')
        exec('F.append(f' + str(o) + ')')

    for nummer in range(1, anzahl_simulationen + 1):

        Belohnung = []
        print_print = []

        for l in loesung:
            c_arr_stoch = []
            c_arr_det = []
            for i in range(0, len(l) - 1):
                c_det = (np.sqrt((l[i][1] - l[i + 1][1]) ** 2 + (l[i][2] - l[i + 1][2]) ** 2)) / distanz_faktor
                c_arr_det.append(c_det)
                c_arr_stoch.append(lognormal(c_det, 50))
            C_stoch = np.sum(c_arr_stoch)

            '''
            neue Belohnung berechnen:
            ab 5, 15 und 30 Minuten: Kürzung von 20, 40 bzw 100% der gesammelten Belohnung:
            '''

            if (C_stoch - 100) > 5:  # mehr als 5 Zeiteinheiten Verspätung
                r_neu = (0.8 * l[0][3][4])
                verspaetung = 1
            if (C_stoch - 100) > 15:  # mehr als 15 Zeiteinheiten Verspätung
                r_neu = (0.6 * l[0][3][4])
                verspaetung = 1
            if (C_stoch - 100) > 30:  # mehr als 30 Zeiteinheiten Verspätung
                r_neu = (0 * l[0][3][4])
                verspaetung = 1
            if C_stoch <= 105:
                verspaetung = 0
                r_neu = l[0][3][4]

            Belohnung.append(r_neu)
            print_print.append([l[0][3][0], r_neu])
            for f in F:
                if l[0][3][0] == f[0]:
                    f.append(r_neu)
                    f[1] = f[1] + verspaetung


    for f in F:
        print('Fahrzeug: ' + str(f))
        print('durchschnittliche Belohnung: '+ str(round(sum(f[2:]) / 100, 1)))
        print('Zuverlässigkeit: '+ str(1 - f[1] / 100))


def deterministischer_Algorithmus(alpha):
    fertig = False
    nr_teilproblem = 1
    routen = []
    loesung = []
    counter = 0
    init_r = copy.deepcopy(init_routen)
    k = 0

    while fertig != True:
        counter += 1

        if counter == 1 and nr_teilproblem <= len(D):

            routen = []

            knoten_abgearbeitet = []

            data = []

            for i in init_r:

                for j in init_r:

                    if i != j:

                        if i['Teilproblem'] == 'Teilproblem' + str(nr_teilproblem) and i['Teilproblem'] == j[
                            'Teilproblem'] \
                                and i['Fahrzeug'][0:2] == j['Fahrzeug'][0:2]:

                            c_oj = np.sqrt(

                                (j['Fahrzeug'][1] - j['Abholort'][1]) ** 2 + (
                                        j['Fahrzeug'][2] - j['Abholort'][2]) ** 2)

                            c_in = np.sqrt(
                                (i['Ziel'][1] - i['Abholort'][1]) ** 2 + (i['Ziel'][2] - i['Abholort'][2]) ** 2)

                            c_ij = np.sqrt(

                                (i['Abholort'][1] - j['Abholort'][1]) ** 2 + (i['Abholort'][2] - j['Abholort'][2]) ** 2)

                            u_i = np.sum(i['Abholort'][4])

                            u_j = np.sum(j['Abholort'][4])

                            saving = alpha * (c_in + c_oj - c_ij) / distanz_faktor + (1 - alpha) * (u_i + u_j)

                            if saving >= 0:
                                data.append([i['Fahrzeug'], i["Abholort"], j["Abholort"], i["Ziel"], saving])

                            # #r[0][3][2](i['Fahrzeug'][0], i['Fahrzeug'][1], i['Fahrzeug'][2], i['Fahrzeug'][3], i["Abholort"][0], i["Abholort"][1], i["Abholort"][2],j["Abholort"], j["Abholort"][1], j["Abholort"][2], i["Ziel"], saving)

            df = pd.DataFrame(data, columns=["Fahrzeug:", "Abholpunkt i", "Abholpunkt j", "Ziel", "Einsparung"])
            df = df.sort_values(by=["Einsparung"], ascending=False)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            counter += 1

            '''

            Einsparungsliste von Kanten, wobei die Einsparung, die mit einer Kante verbunden ist, 

            die die Orte i und j verbindet, wie folgt berechnet wird: savingsij = α(cin +c0j -cij)+(1-α)(ui +uj), wobei α ∈ (0,1) 

            ein Algorithmusparameter ist, cij die Reisezeit zwischen i und j, n der Zielknoten, 0 der Ausgangspunkt und ui, uj die 

            zugehörigen Belohnungen an jedem Knoten. Diese Einsparungen berücksichtigen also sowohl die Reisezeiten als auch die

            die aggregierte Belohnung, die durch den Besuch beider Orte erzielt wird.

            '''

        if counter == 2:
            for a in init_r:
                if a['Teilproblem'] == 'Teilproblem' + str(nr_teilproblem):
                    routen.append([a['Fahrzeug'], a['Abholort'], a['Ziel']])
            counter += 1

        if counter >= 3 and df.empty != True and nr_teilproblem <= len(D):


            if df.iloc[0, 1] not in knoten_abgearbeitet and df.iloc[0, 2] not in knoten_abgearbeitet:

                k += 1

                c_oi = np.sqrt((df.iloc[0, 0][1] - df.iloc[0, 1][1]) ** 2 + (df.iloc[0, 0][2] - df.iloc[0, 1][2]) ** 2)

                c_ij = np.sqrt((df.iloc[0, 1][1] - df.iloc[0, 2][1]) ** 2 + (df.iloc[0, 1][2] - df.iloc[0, 2][2]) ** 2)

                c_jn = np.sqrt((df.iloc[0, 3][1] - df.iloc[0, 2][1]) ** 2 + (df.iloc[0, 3][2] - df.iloc[0, 2][2]) ** 2)

                c = (c_oi + c_ij + c_jn)/distanz_faktor

                if c <= 100 and df.iloc[0, 0][3][2] >= df.iloc[0, 1][3] + df.iloc[0, 2][3]:

                    exec('route' + str(k) + ' = []')

                    exec('route' + str(k) + '.append(df.iloc[0, 0])')

                    exec('route' + str(k) + '.append(df.iloc[0, 1])')

                    exec('route' + str(k) + '.append(df.iloc[0, 2])')

                    exec('route' + str(k) + '.append(df.iloc[0, 3])')

                    knoten_abgearbeitet.append(df.iloc[0, 1])

                    knoten_abgearbeitet.append(df.iloc[0, 2])

                    for r in routen:

                        if df.iloc[0, 2] in r:
                            ind = routen.index(r)

                    for r in routen:

                        if df.iloc[0, 1] == r[1]:
                            r[0][3][5] = c

                            r[0][3][4] = r[0][3][4] + routen[ind][0][3][4]

                            r[0][3][2] = r[0][3][2] - routen[ind][0][3][3]

                            r[0][3][3] = r[0][3][3] + routen[ind][0][3][3]

                            exec('r.insert(-1,df.iloc[0, 2])')

                            routen.pop(ind)

            if df.iloc[0, 1] not in knoten_abgearbeitet and df.iloc[0, 2] in knoten_abgearbeitet:

                for r in routen:

                    if df.iloc[0, 1] in r:
                        ind = routen.index(r)

                for r in routen:

                    if df.iloc[0, 2] == r[1]:

                        c_or = np.sqrt(

                            (df.iloc[0, 0][1] - df.iloc[0, 2][1]) ** 2 + (df.iloc[0, 0][2] - df.iloc[0, 2][2]) ** 2)

                        c_oi = np.sqrt(

                            (df.iloc[0, 0][1] - df.iloc[0, 1][1]) ** 2 + (df.iloc[0, 0][2] - df.iloc[0, 1][2]) ** 2)

                        c_ir = np.sqrt(

                            (df.iloc[0, 1][1] - df.iloc[0, 2][1]) ** 2 + (df.iloc[0, 1][2] - df.iloc[0, 2][2]) ** 2)

                        c = r[0][3][5] + (- c_or + c_oi + c_ir)/distanz_faktor #Berechnung Fahrtzeit beim
                        #  Hinzufügen eines Abholknoten zur Route

                        if c <= 100 and r[0][3][2] >= routen[ind][0][3][3]:

                            exec('r.insert(1,df.iloc[0, 1])')

                            r[0][3][2] = r[0][3][2] - routen[ind][0][3][3]

                            r[0][3][3] = r[0][3][3] + routen[ind][0][3][3]

                            r[0][3][5] = c

                            r[0][3][4] = r[0][3][4] + routen[ind][0][3][4]

                            knoten_abgearbeitet.append(df.iloc[0, 1])

                            routen.pop(ind)

            if df.iloc[0, 1] in knoten_abgearbeitet and df.iloc[0, 2] not in knoten_abgearbeitet:

                for r in routen:

                    if df.iloc[0, 2] in r:
                        ind = routen.index(r)

                for r in routen:

                    if df.iloc[0, 1] == r[-2]:

                        c_rd = np.sqrt(

                            (df.iloc[0, 1][1] - df.iloc[0, 3][1]) ** 2 + (df.iloc[0, 1][2] - df.iloc[0, 3][2]) ** 2)

                        c_ri = np.sqrt(

                            (df.iloc[0, 1][1] - df.iloc[0, 2][1]) ** 2 + (df.iloc[0, 1][2] - df.iloc[0, 2][2]) ** 2)

                        c_id = np.sqrt(

                            (df.iloc[0, 2][1] - df.iloc[0, 3][1]) ** 2 + (df.iloc[0, 2][2] - df.iloc[0, 3][2]) ** 2)

                        c = r[0][3][5] + (- c_rd + c_ri + c_id)/distanz_faktor

                        if c <= 100 and r[0][3][2] >= routen[ind][0][3][3]:
                            # Nebenbedingungen werden nicht verletzt: Platz und Zeit

                            exec('r.insert(-1,df.iloc[0, 2])')

                            r[0][3][2] = r[0][3][2] - routen[ind][0][3][3]

                            r[0][3][3] = r[0][3][3] + routen[ind][0][3][3]

                            r[0][3][5] = c

                            r[0][3][4] = r[0][3][4] + routen[ind][0][3][4]

                            knoten_abgearbeitet.append(df.iloc[0, 2])

                            routen.pop(ind)

            if df.iloc[0, 1] in knoten_abgearbeitet and df.iloc[0, 2] in knoten_abgearbeitet:

                for r in routen:

                    if df.iloc[0, 2] in r:
                        ind = routen.index(r)

                for a in routen:

                    if df.iloc[0, 1] in a:
                        ind2 = routen.index(a)

                if ind != ind2:

                    for r in routen:

                        if df.iloc[0, 1] == r[-2]:

                            c = r[0][3][5] + routen[ind][0][3][5]

                            if c <= 100 and r[0][3][2] >= routen[ind][0][3][3]:
                                # Nebenbedingungen werden nicht verletzt: Platz und Zeit

                                for i in range(0, len(routen[ind][1:])):
                                    exec('r.insert(-1,routen[ind][1:][i])')

                                r[0][3][2] = r[0][3][2] - routen[ind][0][3][3]

                                r[0][3][3] = r[0][3][3] + routen[ind][0][3][3]

                                r[0][3][5] = c

                                r[0][3][4] = r[0][3][4] + routen[ind][0][3][4]

                                routen.pop(ind)

            df = df.iloc[1:]

        if df.empty == True and nr_teilproblem <= len(D):

            for o in O:

                if o[3][1] == D[nr_teilproblem - 1]:
                    ind = None

                    for r in routen:

                        if o[0] == r[0][0]:
                            if ind is not None:
                                if r[0][3][4] > routen[ind][0][3][4]:
                                    ind = routen.index(r)
                            if ind is None:
                                ind = routen.index(r)
                    if ind is not None:
                        loesung.append(routen[ind])

            counter = 0
            nr_teilproblem += 1

        if nr_teilproblem > len(D) and df.empty:
            fertig = True
            arr = []
            Fahrzeuge_reihenfolge=[]
            for l in loesung:
                Fahrzeuge_reihenfolge.append(l[0][3][0])
                arr.append(l[0][3][4])
            print(loesung)
            print('Gesamtbelohnung ' + str(sum(arr)))
            nr_teilproblem=0


def stochastischer_Algorithmus(alpha, nr_teilproblem, durchlaufzeit):
    alle_belohnungen = []
    alle_loesungen = []
    random.seed(alpha+nr_teilproblem)
    beta = random.uniform(0.10000000000000001, 0.3) #Auswahl beta zwischen (0.1, 0.3)
    alle_generierten_z_Werte = []
    init_r = copy.deepcopy(init_routen)
    fertig = False
    counter = 0
    k = 0

    counter += 1
    while fertig != True :


        if counter == 1:
            data = []


            for i in init_r:

                for j in init_r:

                    if i != j:

                        if i['Teilproblem'] == 'Teilproblem' + str(nr_teilproblem) and i['Teilproblem'] == j[
                            'Teilproblem'] \
                                and i['Fahrzeug'][0:2] == j['Fahrzeug'][0:2]:
                            c_oj = np.sqrt((j['Fahrzeug'][1] - j['Abholort'][1]) ** 2 + (
                                    j['Fahrzeug'][2] - j['Abholort'][2]) ** 2)

                            c_in = np.sqrt(
                                (i['Ziel'][1] - i['Abholort'][1]) ** 2 + (i['Ziel'][2] - i['Abholort'][2]) ** 2)

                            c_ij = np.sqrt(

                                (i['Abholort'][1] - j['Abholort'][1]) ** 2 + (
                                        i['Abholort'][2] - j['Abholort'][2]) ** 2)

                            u_i = sum(i['Abholort'][4])

                            u_j = sum(j['Abholort'][4])

                            saving = alpha * (c_in + c_oj - c_ij) / distanz_faktor + (1 - alpha) * (u_i + u_j)

                            if saving >= 0:
                                data.append([i["Fahrzeug"], i["Abholort"], j["Abholort"], i["Ziel"], saving])


            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            counter += 1

            '''

            Einsparungsliste von Kanten, wobei die Einsparung, die mit einer Kante verbunden ist, 

            die die Orte i und j verbindet, wie folgt berechnet wird: savingsij = α(cin +c0j -cij)+(1-α)(ui +uj), wobei α ∈ (0,1) 

            ein Algorithmusparameter ist, cij die Reisezeit zwischen i und j, n der Zielknoten, 0 der Ausgangspunkt und ui, uj die 

            zugehörigen Belohnungen an jedem Knoten. Diese Einsparungen berücksichtigen also sowohl die Reisezeiten als auch die

            die aggregierte Belohnung, die durch den Besuch beider Orte erzielt wird.

            '''

        if counter == 2:

            routen=[]
            for a in init_r:
                if a['Teilproblem'] == 'Teilproblem' + str(nr_teilproblem):
                    routen.append([a['Fahrzeug'], a['Abholort'], a['Ziel']])
            counter += 1
            start = time.time()
            end = 0

        if counter == 3:

            routen_copy = copy.deepcopy(routen)

            df_copy = pd.DataFrame(data, columns=["Fahrzeug:", "Abholpunkt i", "Abholpunkt j", "Ziel", "Einsparung"])
            df_copy = df_copy.sort_values(by=["Einsparung"], ascending=False)
            counter += 1
            knoten_abgearbeitet = []

            z_arr = []

        if counter >= 4 and df_copy.empty != True:

            if (end - start) <= durchlaufzeit: #Einhaltung Durchführungszeit des ALgorithmus
                if df_copy.empty != True:

                    nr_in_range = False

                    while nr_in_range == False:

                        '''
                        Generiert Werte mithilfe der geometrischen Verteilung, die aber der Position von Listenelemneten 
                        entsprechen 
                        '''

                        z = np.random.geometric(beta)
                        if z <= len(df_copy.index):
                            nr_in_range = True
                            z = z - 1
                            z_arr.append(z)


                    if df_copy.iloc[z, 1] not in knoten_abgearbeitet and df_copy.iloc[z, 2] not in knoten_abgearbeitet:

                        k += 1

                        c_oi = np.sqrt((df_copy.iloc[z, 0][1] - df_copy.iloc[z, 1][1]) ** 2 + (
                                df_copy.iloc[z, 0][2] - df_copy.iloc[z, 1][2]) ** 2)

                        c_ij = np.sqrt((df_copy.iloc[z, 1][1] - df_copy.iloc[z, 2][1]) ** 2 + (
                                df_copy.iloc[z, 1][2] - df_copy.iloc[z, 2][2]) ** 2)

                        c_jn = np.sqrt((df_copy.iloc[z, 3][1] - df_copy.iloc[z, 2][1]) ** 2 + (
                                df_copy.iloc[z, 3][2] - df_copy.iloc[z, 2][2]) ** 2)

                        c = (c_oi + c_ij + c_jn) / distanz_faktor  #

                        if c <= 100 and df_copy.iloc[z, 0][3][2] >= df_copy.iloc[z, 1][3] + df_copy.iloc[z, 2][3]:

                            exec('route' + str(k) + ' = []')

                            exec('route' + str(k) + '.append(df_copy.iloc[z, 0])')

                            exec('route' + str(k) + '.append(df_copy.iloc[z, 1])')

                            exec('route' + str(k) + '.append(df_copy.iloc[z, 2])')

                            exec('route' + str(k) + '.append(df_copy.iloc[z, 3])')

                            knoten_abgearbeitet.append(df_copy.iloc[z, 1])

                            knoten_abgearbeitet.append(df_copy.iloc[z, 2])

                            for r in routen_copy:

                                if df_copy.iloc[z, 2] in r:
                                    ind = routen_copy.index(r)

                            for r in routen_copy:

                                if df_copy.iloc[z, 1] == r[1]:
                                    r[0][3][5] = c

                                    r[0][3][4] = r[0][3][4] + routen_copy[ind][0][3][4]

                                    r[0][3][2] = r[0][3][2] - routen_copy[ind][0][3][3]

                                    r[0][3][3] = r[0][3][3] + routen_copy[ind][0][3][3]

                                    exec('r.insert(-1,df_copy.iloc[z, 2])')

                                    routen_copy.pop(ind)

                    if df_copy.iloc[z, 1] not in knoten_abgearbeitet and df_copy.iloc[z, 2] in knoten_abgearbeitet:

                        for r in routen_copy:

                            if df_copy.iloc[z, 1] in r:
                                ind = routen_copy.index(r)

                        for r in routen_copy:

                            if df_copy.iloc[z, 2] == r[1]:

                                c_or = np.sqrt(

                                    (df_copy.iloc[z, 0][1] - df_copy.iloc[z, 2][1]) ** 2 + (
                                            df_copy.iloc[z, 0][2] - df_copy.iloc[z, 2][2]) ** 2)

                                c_oi = np.sqrt(

                                    (df_copy.iloc[z, 0][1] - df_copy.iloc[z, 1][1]) ** 2 + (
                                            df_copy.iloc[z, 0][2] - df_copy.iloc[z, 1][2]) ** 2)

                                c_ir = np.sqrt(

                                    (df_copy.iloc[z, 1][1] - df_copy.iloc[z, 2][1]) ** 2 + (
                                            df_copy.iloc[z, 1][2] - df_copy.iloc[z, 2][2]) ** 2)

                                c = r[0][3][5] + (- c_or + c_oi + c_ir) / distanz_faktor  #

                                if c <= 100 and r[0][3][2] >= routen_copy[ind][0][3][3]:
                                    exec('r.insert(1,df_copy.iloc[z, 1])')

                                    r[0][3][2] = r[0][3][2] - routen_copy[ind][0][3][3]

                                    r[0][3][3] = r[0][3][3] + routen_copy[ind][0][3][3]

                                    r[0][3][5] = c

                                    r[0][3][4] = r[0][3][4] + routen_copy[ind][0][3][4]

                                    knoten_abgearbeitet.append(df_copy.iloc[z, 1])

                                    routen_copy.pop(ind)

                    if df_copy.iloc[z, 1] in knoten_abgearbeitet and df_copy.iloc[z, 2] not in knoten_abgearbeitet:

                        for r in routen_copy:

                            if df_copy.iloc[z, 2] in r:
                                ind = routen_copy.index(r)

                        for r in routen_copy:

                            if df_copy.iloc[z, 1] == r[-2]:

                                c_rd = np.sqrt(

                                    (df_copy.iloc[z, 1][1] - df_copy.iloc[z, 3][1]) ** 2 + (
                                            df_copy.iloc[z, 1][2] - df_copy.iloc[z, 3][2]) ** 2)

                                c_ri = np.sqrt(

                                    (df_copy.iloc[z, 1][1] - df_copy.iloc[z, 2][1]) ** 2 + (
                                            df_copy.iloc[z, 1][2] - df_copy.iloc[z, 2][2]) ** 2)

                                c_id = np.sqrt(

                                    (df_copy.iloc[z, 2][1] - df_copy.iloc[z, 3][1]) ** 2 + (
                                            df_copy.iloc[z, 2][2] - df_copy.iloc[z, 3][2]) ** 2)

                                c = r[0][3][5] + (- c_rd + c_ri + c_id) / distanz_faktor  #

                                if c <= 100 and r[0][3][2] >= routen_copy[ind][0][3][3]:
                                    exec('r.insert(-1,df_copy.iloc[z, 2])')

                                    r[0][3][2] = r[0][3][2] - routen_copy[ind][0][3][3]

                                    r[0][3][3] = r[0][3][3] + routen_copy[ind][0][3][3]

                                    r[0][3][5] = c

                                    r[0][3][4] = r[0][3][4] + routen_copy[ind][0][3][4]

                                    knoten_abgearbeitet.append(df_copy.iloc[z, 2])

                                    routen_copy.pop(ind)

                    if df_copy.iloc[z, 1] in knoten_abgearbeitet and df_copy.iloc[z, 2] in knoten_abgearbeitet:

                        for r in routen_copy:

                            if df_copy.iloc[z, 2] in r:
                                ind = routen_copy.index(r)

                        for a in routen_copy:

                            if df_copy.iloc[z, 1] in a:
                                ind2 = routen_copy.index(a)

                        if ind != ind2:

                            for r in routen_copy:

                                if df_copy.iloc[z, 1] == r[-2]:

                                    c = r[0][3][5] + routen_copy[ind][0][3][5]

                                    if c <= 100 and r[0][3][2] >= routen_copy[ind][0][3][3]:

                                        for i in range(0, len(routen_copy[ind][1:])):
                                            exec('r.insert(-1,routen_copy[ind][1:][i])')

                                        r[0][3][2] = r[0][3][2] - routen_copy[ind][0][3][3] #Aktualisierung Kapazität

                                        r[0][3][3] = r[0][3][3] + routen_copy[ind][0][3][3] #Aktualisierung aktuell mitfahrende Fahrgäste

                                        r[0][3][4] = r[0][3][4] + routen_copy[ind][0][3][4]  # Aktualiksierung erzielte Belohnung

                                        r[0][3][5] = c #Aktualisierung Fahrtzeit


                                        routen_copy.pop(ind)
                    df_copy = df_copy.drop(df_copy.index[z])


                if df_copy.empty == True and counter == 4:
                    end = time.time()
                    loesung = []
                    for o in O:
                        if o[3][1] == D[nr_teilproblem - 1]:

                            ind = None

                            for r in routen_copy:
                                if o[0] == r[0][0]:
                                    if ind is not None:
                                        if r[0][3][4] > routen_copy[ind][0][3][4]:
                                            ind = routen_copy.index(r)
                                    if ind is None:
                                        ind = routen_copy.index(r)
                            if ind is not None:  # o nicht vergeben
                                loesung.append(routen_copy[ind])



                    alle_generierten_z_Werte.append(z_arr)
                    alle_loesungen.append(loesung)

                    counter = 3

                if (end - start) > durchlaufzeit and counter == 3 and df_copy.empty == True: #Falls die Zeit abgelaufen
                    # und die letzte Iteration beendet ist

                    for l in alle_loesungen:
                        arr = []
                        for i in l:
                            arr.append(i[0][3][4])
                        alle_belohnungen.append(sum(arr))

                    fertig = True

                    max_bel = max(alle_belohnungen)

                    ind = alle_belohnungen.index(max_bel)
                    print('Index der besten Lösung: ' + str(ind))
                    print('Verwendete z_Werte bei bester Lösung: ' +str(alle_generierten_z_Werte[ind]))
                    print('Beta-Wert :' +str(beta))
                    print('Beste Lösung :' + str(alle_loesungen[ind]))
                    print('Maximal erzielte Belohnung bei bester Lösung: ' +str(max_bel))


''''
Beispiel Eingaben:

-deterministischer_Algorithmus(1)
-stochastischer_Algorithmus(1,1,10)
-stochastische_Reisezeiten_zufuegen([[['o_4', 1, 25, ['f_3', ['d_1', 85, 50], 3, 5, 132, 99.81647514841738]], 
['p_48', 24, 13, 1, [10], ['d_1', 85, 50]], ['p_25', 24, 16, 2, [33, 39], ['d_1', 85, 50]], ['p_6', 67, 34, 1, [12], 
['d_1', 85, 50]], ['p_16', 68, 36, 1, [38], ['d_1', 85, 50]], ['d_1', 85, 50]], [['o_5', 1, 15, ['f_1', ['d_1', 85, 50], 
0, 4, 79, 99.09720603699095]], ['p_3', 18, 13, 2, [19, 33], ['d_1', 85, 50]], ['p_27', 29, 10, 1, [11], ['d_1', 85, 50]],
 ['p_24', 48, 15, 1, [16], ['d_1', 85, 50]], ['d_1', 85, 50]], [['o_1', 1, 48, ['f_2', ['d_2', 85, 54], 0, 4, 118, 98.61126916508039]],
  ['p_9', 19, 70, 1, [38], ['d_2', 85, 54]], ['p_52', 34, 72, 1, [40], ['d_2', 85, 54]], ['p_58', 51, 71, 1, [13], 
  ['d_2', 85, 54]], ['p_10', 66, 63, 1, [27], ['d_2', 85, 54]], ['d_2', 85, 54]], [['o_2', 1, 34, ['f_6', 
  ['d_2', 85, 54], 3, 5, 121, 98.43969329479923]], ['p_35', 31, 62, 2, [31, 28], ['d_2', 85, 54]], 
  ['p_49', 36, 58, 1, [14], ['d_2', 85, 54]], ['p_39', 82, 58, 2, [11, 37], ['d_2', 85, 54]], ['d_2', 85, 54]], 
  [['o_3', 1, 22, ['f_5', ['d_2', 85, 54], 1, 5, 163, 99.48744617607146]], ['p_48', 24, 13, 1, [30], ['d_2', 85, 54]], 
  ['p_20', 35, 15, 1, [35], ['d_2', 85, 54]], ['p_11', 38, 16, 1, [24], ['d_2', 85, 54]], ['p_29', 51, 26, 2, [38, 36], 
  ['d_2', 85, 54]], ['d_2', 85, 54]], [['o_6', 1, 4, ['f_4', ['d_2', 85, 54], 4, 2, 44, 98.25575360639215]], 
  ['p_31', 21, 21, 2, [13, 31], ['d_2', 85, 54]], ['d_2', 85, 54]]], 100)

'''

deterministischer_Algorithmus(1)
