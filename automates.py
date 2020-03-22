import subprocess
import os

"""
    Dans  ce TP j'ai implémenter les fonctionnalités des automates finis
    suivant le modèle mathématique (ie : suivant les ensembles )
    et en définissant un automate comme etant un quintuplet 
    <Alphabet ,Etats,Etats_initaux,Etats_finaux,Transition>
    ou transition est un objet défini par : (etat_de_depart,mot,etat_d_arrive)
    pour l'ensemble des Etats_initiaux en se contente juste d'un seul etat initial

    E : représente epsilon
    f : represenete un etat final ajouté 
    p : représente une etat puis 
"""

class Automate(object):
    """
    Une classe définissant un automate d'état fini 
    
    """

    def __init__(self,alphabet,etats=(),etats_initial=(),etats_finaux=(),transitions=()):

        #L'alphabet concernant cet automate A
        self.alphabet=set(alphabet)

        #les etats de A
        self.etats=set(etats)

        #les etats initials de A
        self.etats_initiaux=set(etats_initial)

        #les etats finaux de A
        self.etats_finaux=set(etats_finaux)

        #les transitions de A
        self.transitions=set(transitions)

    #la surdéfinition de la méthode str pour afficher les informations de l'automate "sous console"

    def __str__(self):
        ret= "Automate :\n"
        ret += "   - alphabet  : '"+str(list(self.alphabet))+"'\n"
        ret += "   - init       : " + str(list(self.etats_initiaux)) + "\n"
        ret += "   - finals     : " + str(list(self.etats_finaux)) + "\n"
        ret += "   - states (%d) :\n" % (len(self.etats))
        list_etat=list(self.etats)
        transitions=list(self.transitions)
        for etat in list_etat :
            ret += "       - (%s) :\n" % (etat)
            boolean=False
            for tr in transitions:
                if tr.etat_de_depart == etat :
                    boolean = True
                    ret +=  "          --(%s)--> (%s)\n" % (tr.mot, tr.etat_d_arrive)

            if not(boolean):
                ret += ".\n"
        return ret

    def ajouterUnEtat(self,etat):
        if not(etat in self.etats):
            self.etats.add(etat)
    
    def retirerUnEtat(self,etat):
        self.etats.remove(etat)
        tr_a_supprimer=[]
        for tr in self.transitions:
            if (tr.etat_d_arrive == etat) or (tr.etat_de_depart ==etat ):
                tr_a_supprimer.append(tr)

        for tr in tr_a_supprimer:
            self.retirerUneTransition(tr)



    def ajouterUnEtatInitial(self,init_etat):
        if not(init_etat in self.etats_initiaux) :
            self.etats_initiaux.add(init_etat)

    def retirerUnEtatInitial(self,init_etat):

        self.etats_initiaux.remove(init_etat)

    def ajouterUnEtatFinal(self,end_etat):
        if not(end_etat in self.etats_finaux):
            self.etats_finaux.add(end_etat)

    def retirerUnEtatFinal(self,end_etat):

        self.etats_finaux.remove(end_etat)

    def ajouterUneTransition(self,transition):

        self.transitions.add(transition)

    def retirerUneTransition(self,transition):

        self.transitions.remove(transition)

    def afficherEtats(self):
        for e in self.etats :
            print(e)

    def afficherTransitions(self):
        for tr in self.transitions :
            print ("({0} {1} {2})".format(tr.etat_de_depart,tr.mot,tr.etat_d_arrive))


            
    """ La reduction d'un automate """

    def reduireAutomate(self):
        """
            les etapes de l'algorithme
            1-suppression des etats non accessible:
                -parcours de tous les chemins partant de l'etat initial et on marque les etats accessible
                -le marquage dans cette algorithme se fait par ajout a la liste "a_traiter"
                -a la fin de la premiere etape on supprime les etats non apparu dans la liste des etats no accessible

            2-suppresion des etats non co-accessible:
                -parcours de tous les chemins partant des etats finaux et on marque tous les etats co-accessible
                -le marquage dans cette etape aussi se fait par ajout a la liste "a_traiter"
                -à la fin de la deuxieme étape on supprime les etats non apparu dans la liste "co_acccessible"
        """

        a=Automate(self.alphabet,self.etats,self.etats_initiaux,self.etats_finaux,self.transitions)
        #La suppression des etats no accessible 
        #un etat est accessible ssi il existe une chemin vers celui-ci de l'etat initial
        etat_init=list(a.etats_initiaux)[0]
        #récuperation sous forme de listes
        list_etats_finaux=list(a.etats_finaux)

        #deux liste de travaille , les etats a traiter et les etats accessible 
        a_traiter=[etat_init]
        accessible=[etat_init]
        deja_traiter=[]

        while a_traiter != [] :
            etat_actuel=a_traiter[0]
            for tr in a.transitions :
                if (tr.etat_de_depart == etat_actuel) and (tr.etat_d_arrive != etat_actuel) and not(tr.etat_d_arrive in deja_traiter):
                    if not(tr.etat_d_arrive in accessible):
                        accessible.append(tr.etat_d_arrive)
                    if not(tr.etat_d_arrive in a_traiter):
                        a_traiter.append(tr.etat_d_arrive)
            deja_traiter.append(etat_actuel)
            a_traiter.remove(etat_actuel)

        etat_a_supprimer=[]
        for etat in a.etats:
            if not(etat in accessible):
                etat_a_supprimer.append(etat)

        for e in etat_a_supprimer:
            a.retirerUnEtat(e)

        #suppression des etats non co-accessible
        #un etat est co-accessible ssi on peut acceder a un etat final partant de cet etat
    
        a_traiter=list_etats_finaux
        co_accessible=list_etats_finaux[:]
        deja_traiter=[]
        while a_traiter != []:
            etat_actuel=a_traiter[0]
            for tr in a.transitions:
                if(tr.etat_d_arrive == etat_actuel) and (tr.etat_de_depart != etat_actuel) and not(tr.etat_de_depart in deja_traiter):
                    if not(tr.etat_de_depart  in co_accessible):
                        co_accessible.append(tr.etat_de_depart)
                    if not(tr.etat_de_depart in a_traiter):
                        a_traiter.append(tr.etat_de_depart)  
            deja_traiter.append(etat_actuel)   
            a_traiter.remove(etat_actuel)

        etat_a_supprimer=[]
        for etat in a.etats:
            if not(etat in co_accessible):
                etat_a_supprimer.append(etat)
        for e in etat_a_supprimer:
            a.retirerUnEtat(e)  

        return a

    """ la déterminisation d'un automate fini """
    def determiniserAutomate(self):
        """ 
            le principe de l'algorithme 
            en trois etapes 
            1-création de l'etat initial
            2-boucle de creation des autre etats et des transitions
                2-1- marquage des etats ,on les ajoutant a une liste a traiter
                2-2-choisir un etat parmi ceux a traiter 
                2-3-pour chaque mot dans l'alphabet :construire les nouveau etats tenant compte des deux automate 
                    le deterministe et le non deterministe
                2-4-supprimer l'etat  quand vient de traiter de la liste des etats a traiter 
            3-construire les trasitions (je l'ai fait un peu avec la deuxieme etape)

        """
        #reduire d'abord l'automate
        self.reduireAutomate()
        #les composantes de l'automate actuel
        a=Automate(self.alphabet,self.etats,self.etats_initiaux,self.etats_finaux,self.transitions)
        etat_init=list(a.etats_initiaux)[0]
        list_alphabet=list(a.alphabet)
        list_etats=list(a.etats)
        list_etats_finaux=list(a.etats_finaux)
        list_transition=list(a.transitions)
        #defintion de la structure de l'automate deterministe
        
        etat_init_det=etat_init
        list_etats_det=[etat_init]
        list_etats_finaux_det=[]
        list_transition_det=[]
        ab=Automate(set(list_alphabet),set(list_etats_det),set([etat_init_det]),set(),set())

        a_traiter=[etat_init_det]
        while(a_traiter != []):
            etat_actuel=a_traiter[0]
            tmp=etat_actuel[:]
            
            for alpha in list_alphabet :
                
                e=[]

                for etat in list_etats :
                    if isinstance(etat_actuel,list):
                        for elt in etat_actuel:
                            for tr in list_transition:
                                if(tr.etat_de_depart == elt) and (tr.etat_d_arrive == etat) and (tr.mot ==alpha):
                                    e.append(etat)
                    else:
                        for tr in list_transition:
                            if (tr.etat_de_depart == etat_actuel) and (tr.mot == alpha) and (tr.etat_d_arrive == etat):
                                e.append(etat)
                
                if e != []:
                    if len(e) == 1 :
                        prem=e[0]
                        if not(prem in list_etats_det):
                            list_etats_det.append(prem)
                            a_traiter.append(prem)
                        
                        if isinstance(etat_actuel,list):
                            c=reglage_list([etat_actuel])
                            etat_actuel_1=c[0]
                            tr=Transition(etat_actuel_1,prem,alpha)
                        else:
                            tr=Transition(etat_actuel,prem,alpha)
                            
                    else:
                        if not(e in list_etats_det):
                            list_etats_det.append(e)
                            a_traiter.append(e)
                        
                        e_f=reglage_list([e])
                        if isinstance(etat_actuel,list):
                            c=reglage_list([etat_actuel])
                            etat_actuel_f=c[0]
                            tr=Transition(etat_actuel_f,e_f[0],alpha)
                        else:
                            tr=Transition(etat_actuel,e_f[0],alpha)

                    list_transition_det.append(tr)

            a_traiter.remove(tmp)

        #reglage des listes pour etre accepter par un set
        list_etats_det=reglage_list(list_etats_det)
        list_etats_finaux_det=reglage_list(list_etats_finaux_det)

        #construction de la liste des etats finaux
        for etat in list_etats_finaux:
            for e in list_etats_det:
                if etat[1] in e :
                    list_etats_finaux_det.append(e)        

        ab.etats=set(list_etats_det)
        ab.etats_finaux=set(list_etats_finaux_det)
        ab.transitions=set(list_transition_det)

        return ab
        
    """ rendre un automate complet """
    def complétionAutomate(self):
        """
            le fonctionnement de l'algorithme
            1-ajout d'un etat puit P
            2-en boucle sur P avec toute l'alphabet 
            3-en ajoute des transitions pour completer les vides
        """
        self.etats.add('p')
        for alpha in self.alphabet:
            tr=Transition('p','p',alpha)
            self.ajouterUneTransition(tr)

        for etat in self.etats:
            alpha_manquante=list(self.alphabet)
            for alpha in self.alphabet:
                for tr in self.transitions :
                    if (tr.etat_de_depart == etat) and (tr.mot == alpha):
                        alpha_manquante.remove(alpha)
            for alpha in alpha_manquante:
                tran=Transition(etat,'p',alpha)
                self.ajouterUneTransition(tran)    

    """ le complément de l'automate"""
    def complementAutomate(self):
        """
            le principe de l'algorithme
            1-s'assurer que l'automate est deterministe et complet
            2-les etats finaux deviennent plus finaux et les non finaux deviennent finaux  
        """
        self.reduireAutomate()
        self.determiniserAutomate()
        self.complétionAutomate()
        nouv_li_etats_finaux=[]
        for etat in self.etats:
            if not(etat in self.etats_finaux):
                nouv_li_etats_finaux.append(etat)
        self.etats_finaux=set(nouv_li_etats_finaux)

    """ le mirroire d'un automate """
    def mirroireAutomate(self):
        """
            le principe de l'algorithme 
            -rassembler les etats finaux en un seul etat final en ajoutant des transitions spontanées
            -l'etat final ajouté devient initial 
            -l'etat initial devient final 
            -toutes les transitions se change de sense
        """
        if(len(self.etats_finaux) >1):
            self.ajouterUnEtat('f')
            for etat in self.etats_finaux :
                tr=Transition(etat,'f','E')
                self.ajouterUneTransition(tr)

            self.etats_finaux=self.etats_initiaux
            self.etats_initiaux=set('f')
        else:
            final=self.etats_finaux
            self.etats_finaux=self.etats_initiaux
            self.etats_initiaux=final

        for tr in self.transitions:
            tr.etat_de_depart , tr.etat_d_arrive = tr.etat_d_arrive ,tr.etat_de_depart

    """reconnaissance des mots dans un automate déterministe"""
    def reconnaissanceMotAutomate(self,mot):
        """
            le principe de l'algorithme
            1-parcourir le mot caractere par caractere 
            2-pour chaque mot du mot en cherche l'existence d'une transition portant comme mot cette derniere 
            3-si c'est le cas en avance ,si non on se bloque
            4-quand on arrive a la longeure-1 du mot on se positionne pour verifier s'il existe une derniere transition 
            vers un etat final
            5-si on arrive a sortir d'un etat final alors le mot est accepté
            6-sinon le mot est rejeté 
        """
        reussi=False
        stop=False
        etat_courant=list(self.etats_initiaux)[0]
        cpt=0
        caractere_courant=mot[cpt]
        
        if len(mot) == 1 :
            for tr in self.transitions:
                if (tr.etat_de_depart == etat_courant)and(tr.mot == caractere_courant) and (tr.etat_d_arrive in self.etats_finaux):
                    reussi=True
                stop=True
                     
        
        while (cpt < len(mot))  and (stop == False) and (reussi == False):
            print(cpt)
            if cpt == (len(mot)-1) :
                if etat_courant in self.etats_finaux :
                    for tr in self.transitions :
                        if (tr.etat_de_depart == etat_courant)and(tr.mot == caractere_courant):
                            reussi=True
                    stop=True
                else:
                    reussi=False
                    stop=True
            else:
                trouve=False
                for tr in self.transitions :
                    if (tr.etat_de_depart == etat_courant)and(tr.mot == caractere_courant):
                        trouve=True
                        etat =tr.etat_d_arrive  
                        
                if(trouve == False):
                    stop=True
                else:
                    cpt=cpt +1
                    caractere_courant=mot[cpt]
                    etat_courant=etat
        return reussi
    
    """
        suppression des transitions spontanées
    """
    def suppEpsilonTransition(self):
        """
            principe de l'algorithme
            1-on initialise le nouveau automate avec toutes les ancinnes , y compris celles des epsilons
            qui seront progressivement supprimées.
            2-en utilisant une fermeture arrière pour simplifier l'algorithme
            3-Pour un état donné q, on considère toutes les transitions epsilon "entrantes"
            4-Chaque transition "sortante" de q est dupliquée : les transitions (p,ε,q) et (q,x,q') 
            entraînent la création de la transition (p,x,q')
            5-Toutes les transitions "sortantes" de q ayant été mises en relation avec (p,ε,q), 
            celle-ci peut être éliminée
            6-modification des etats initiaux et finaux suite a la suppression des transitions epsilon
        """
        liste_etat_intiaux=list(self.etats_initiaux)
        liste_etat_finaux=list(self.etats_finaux)
        liste_transitions=list(self.transitions)
       

        for etat in self.etats:
            for tr in self.transitions:
                if(tr.etat_d_arrive == etat) and (tr.mot == 'E'):
                    etat_depart=tr.etat_de_depart
                    for alpha in self.alphabet :
                        for tr2 in self.transitions:
                            if(tr2.etat_de_depart == etat) and (tr2.mot == alpha) :
                                trans=Transition(etat_depart,tr2.etat_d_arrive,tr2.mot)
                                liste_transitions.append(trans)
                    liste_transitions.remove(tr)
                    if etat in self.etats_finaux :
                        liste_etat_finaux.append(etat_depart)

                    if etat_depart in self.etats_initiaux:
                        liste_etat_intiaux.append(etat)
        
        self.etats_initiaux=set(liste_etat_intiaux)
        self.etats_finaux=set(liste_etat_finaux)
        self.transitions=set(liste_transitions)
        if 'E' in self.alphabet:
            self.alphabet.remove('E')

    """  simplifier un automate , enlever les transitions composées ie: longeure mot>1"""
    def simplifierAutomate(self):
        """
            principe de l'algorithme
            1-parcourire toutes les transitions et pour chaque transition
            2-si la transition possède un mot de longeure sup a 1 
            3- créer len(mot)-1 etat suplémentaire
            4-créer len(mot) de transitions 
        """

        list_transition_a_supprimer=[]
        
        liste_transitions=list(self.transitions)
        for tr in liste_transitions :
            
            if len(tr.mot) > 1 :
                
                list_transition_a_supprimer.append(tr)
                nb_etat_sup=len(tr.mot)-1
                nb_transitions=len(tr.mot)
                
                if (tr.etat_de_depart == tr.etat_d_arrive):
                    i=0
                    while i < nb_etat_sup :
                        etat_a_ajouter=tr.etat_de_depart+str(i) 
                        self.etats.add(etat_a_ajouter) 
                        i=i+1
                    depart_actuel=tr.etat_de_depart
                    arrivé_actuel=tr.etat_de_depart+"0"
                    j=0
                    while j < nb_transitions :
                        if(j < nb_transitions-1):
                            tran=Transition(depart_actuel,arrivé_actuel,tr.mot[j])
                            self.transitions.add(tran)
                            
                            depart_actuel=arrivé_actuel
                            if j == nb_transitions-2:
                                arrivé_actuel=arrivé_actuel[:2]+str(j)
                            else:
                                arrivé_actuel=arrivé_actuel[:2]+str(j+1)
                        else:
                            depart_actuel=arrivé_actuel
                            arrivé_actuel=tr.etat_de_depart
                            tran=Transition(depart_actuel,arrivé_actuel,tr.mot[j])
                            self.transitions.add(tran)
                            
                        j=j+1
                else:
                    i=0
                    while i < nb_etat_sup :
                        etat_a_ajouter=tr.etat_de_depart+tr.etat_d_arrive+"_"+str(i) 
                        self.etats.add(etat_a_ajouter) 
                        i=i+1
                    
                    depart_actuel=tr.etat_de_depart
                    arrivé_actuel=tr.etat_de_depart+tr.etat_d_arrive+"_0"
                    j=0
                    while j < nb_transitions :
                        if(j < nb_transitions-1):
                            tran=Transition(depart_actuel,arrivé_actuel,tr.mot[j])
                            print(tran)
                            self.transitions.add(tran)
                            
                            depart_actuel=arrivé_actuel
                            if j == nb_transitions-2:
                                arrivé_actuel=arrivé_actuel[:5]+str(j)
                            else:
                                arrivé_actuel=arrivé_actuel[:5]+str(j+1)
                        else:
                            depart_actuel=arrivé_actuel
                            arrivé_actuel=tr.etat_d_arrive
                            tran=Transition(depart_actuel,arrivé_actuel,tr.mot[j])
                            print(tran)
                            self.transitions.add(tran)
                        j=j+1
        for tr1 in list_transition_a_supprimer:
            self.transitions.remove(tr1)   

    




""" 
    la classe définissant une transition
    1-état de départ
    2-le mot 
    3-état d'arrivé

"""            
class Transition():

    def __init__(self,etat_de_depart,etat_d_arrive,mot):
        #l'etat de depart de la transition
        self.etat_de_depart=etat_de_depart
        #l'etat d'arrivé de la transition 
        self.etat_d_arrive=etat_d_arrive
        #le mot a lire pour passer de l'etat de depart a celui d'arrivé
        self.mot=mot
    
    def __str__(self):
        return("("+self.etat_de_depart+","+self.mot+","+self.etat_d_arrive+")")
    def __eq__(self, other):
        return (self.etat_de_depart == other.etat_de_depart)and(self.etat_d_arrive == other.etat_d_arrive)and(self.mot == other.mot)

    def __hash__(self):
        return hash((self.etat_de_depart,self.etat_d_arrive,self.mot))


""" 
    des fonctions d'utilités pour les structures de données et les algorithmes proposés
"""
def reglage_list(li):
    nouvelle_list=[]
    for elt in li:
        ret='s'
        if isinstance(elt,list):
            for e in elt:
                ret += e[1]
            nouvelle_list.append(ret)
        else:
            nouvelle_list.append(elt)

    return nouvelle_list

""" les fonctions pour l'affichage graphique de l'automate """
""" 
    en utilisant le format dot et une librairie de python 
    pour lire ce format et le convertire en png ou pdf 
    
"""
def to_dot(a, name="aaa"):
    #récuperation sous forme de listes
    list_etats=list(a.etats)
    list_etats_initiaux=list(a.etats_initiaux)
    list_etats_finaux=list(a.etats_finaux)
    list_transition=list(a.transitions)

    ret = "digraph " + name + " {\n    rankdir=\"LR\";\n\n"
    ret += "    // States (" + str(len(list_etats)) + ")\n"

    state_name = lambda s : "Q_" + str(list_etats.index(s))

    #Les etats 
    ret += "    node [shape = point ];     __Qi__ // Initial state\n" # l'etat initial
    for etat in list_etats :
        ret += "    "
        if etat in list_etats_finaux :
            ret += "node [shape=doublecircle]; "
        else:
            ret += "node [shape=circle];       "
        ret += state_name(etat) + " [label=" + etat + "];\n"

    #les transitions
    ret += "\n    // Transitions\n"
    for etat_init in list_etats_initiaux :
        ret += "    __Qi__ -> " + state_name(etat_init) + "; // Initial state arrow\n"
    for etat in list_etats :
        for tr in list_transition :
            if tr.etat_de_depart == etat :
                ret += "    " + state_name(etat) + " -> " + state_name(tr.etat_d_arrive) + " [label=" + tr.mot + "];\n"

    return ret + "}\n"

def to_png(a, filename=None, name="graphe"):

    if filename is None:
        filename = name + ".png"
 
    tmp_file = filename + ".tmp"
    with open(tmp_file, "w") as file:
        file.write(to_dot(a, name))
 
    subprocess.call(("dot -Tpng " + tmp_file + " -o " + filename).split(" "))
    #subprocess.call(("del " + tmp_file).split(" "))

"""les fonctions d'affichage de menu et affichage console """

def liste_choix():
    
    print("Les fonctionnalités disponible sont les suivantes :\n")
    print("         1-Chargement d'un automate (entrer le quintuplet).\n")
    print("         2-Affichage d'un automate sous format (.png).\n")
    print("         3-Réduction d'un automate.\n")
    print("         4-Déterminiser un automate.\n")
    print("         5-Completer un automate.\n")
    print("         6-Complément d'un automate.\n")
    print("         7-Mirroire d'un automate.\n")
    print("         8-Reconnaissance d'un mot dans un automate déterministe.\n")
    print("         9-Suppression des transitions spontanées.\n")
    print("         10-simplification d'un automate (les transitions composées).\n")
    print("         11-Quitter le programme")

def charger_automate():
    A=Automate(set(),set(),set(),set(),set())
    print("Veuillez saisire l'alphabet de l'automate comme une chaine de caractère.\n")
    alphabet=input()
    for a in alphabet:
        A.alphabet.add(a)

    print("Veuillez saisire le nombre d'etats de l'automate.\n")
    print("Les etats sont comme suit { s0, s1, s2 ,s3 ...} . \n")
    nbr_etat=int(input())
    i=0
    while i< nbr_etat:
        etat_a_ajouter="s"+str(i)
        A.etats.add(etat_a_ajouter)
        i=i+1

    print("Veuillez saisire le nom de l'etat initial {s1 , s2 ou Si} .\n")
    init_etat=input()
    A.etats_initiaux.add(init_etat)

    print("Veuillez saisire le nombre des etats finaux .\n")
    nbr_etat_finaux=int(input())

    j=0
    while j<nbr_etat_finaux :
        print("      L'etat final N°"+str(j+1))
        final=input()
        A.etats_finaux.add(final)
        j=j+1
        print("\n")

    print("Veuillez saisire le  nombre de transitions . \n")
    nbr_transition=int(input())
    k=0
    while k<nbr_transition :
        print("     La transition N°"+str(k+1))
        print("         -L'etat de départ : ")
        etat_depart=input()
        print("         -Le mot ou la lettre : ")
        mot=input()
        print("         -L'etat d'arrivé : ")
        etat_d_arrive=input()
        
        tr=Transition(etat_depart,etat_d_arrive,mot)
        A.transitions.add(tr)
        k=k+1
        print("\n")

    return A

""" le programme principale """
""" M______A______I_______N """

if __name__ == "__main__":
    
    print("*** Implémentation d'un automate d'etats finis ***\n")
    Quitter=False
    charger=False
    deterministe=False
    while not(Quitter):
        liste_choix()
        print("-Veuillez sélectionner un choix. \n")
        choix=input()
        
        os.system("cls")
        if(choix in ["1","2","3","4","5","6","7","8","9","10","11"]):

            if(choix == "11" ):
                Quitter=True
                break

            if(choix == "1"):
                charger=True
                A=charger_automate()
                os.system("cls")
                print("Voici l'automate chargé :\n")
                print(A)
            else:

                if(choix == "2") and (charger):
                    os.system("cls")
                    print("Veuillez saisire le nom du fichier (nom.png)\n")
                    filename=input()
                    to_png(A,filename)
                    os.system("cls")
                    liste_choix()
                elif not(charger):
                       print("Veuillez charger d'abord l'automate.\n")
                else:

                    if(choix == "3") and (charger):
                        os.system("cls")
                        A=A.reduireAutomate()
                        print("L'automate est reduit avec succès")
                        print(A)
                    elif not(charger):
                       print("Veuillez charger d'abord l'automate.\n")
                    else:
                        if(choix == "4") and (charger):
                            deterministe=True
                            os.system("cls")
                            A=A.determiniserAutomate()
                            print("l'automate déterministe est le suivant :\n")
                            print(A)
                        elif not(charger):
                            print("Veuillez charger d'abord l'automate.\n")
                        else:

                            if(choix == "5") and (charger):
                                A.complétionAutomate()
                                print("l'automate complet est le suivant :\n")
                                print(A)
                            elif not(charger):
                                print("Veuillez charger d'abord l'automate.\n")
                            else:
                                if(choix == "6") and (charger):
                                    A.complementAutomate()
                                    print("L'automate complement est le suivant: \n")
                                    print(A)
                                elif not(charger):
                                     print("Veuillez charger d'abord l'automate.\n")
                                else:
                                    if(choix == "7") and (charger):
                                        A.mirroireAutomate()
                                        print("Le mirroire de l'automate est le suivant: \n")
                                        print(A)
                                    elif not(charger):
                                        print("Veuillez charger d'abord l'automate.\n")
                                    else:
                                        if(choix == "8") and (charger) and (deterministe):
                                            print("Veuillez saisire le mot à reconnaitre")
                                            mot=input()
                                            accepte=A.reconnaissanceMotAutomate(mot)
                                            if accepte :
                                                print("Le mot "+ mot +" appartient au langage.\n")
                                            else:
                                                print("Le mot "+mot+" n'appartient pas au langage. \n")
                                        elif not(charger):
                                            print("Veuillez charger d'abord l'automate.\n")     
                                        else:

                                            if(choix == "9") and (charger):
                                                fin=False
                                                while not(fin):
                                                    trouve=False
                                                    for tr in A.transitions:
                                                        if tr.mot == 'E':
                                                            trouve=True

                                                    if(trouve):
                                                        A.suppEpsilonTransition()
                                                    else:
                                                        fin=True

                                                print("l'automate sans les transitions epsilon est le suivant \n")
                                                print(A)
                                            elif not(charger):
                                                print("Veuillez charger d'abord l'automate.\n")
                                            else:

                                                if(choix == "10") and (charger):
                                                    A.simplifierAutomate()
                                                    print("l'automate simplifié (sans les transitions avec mot composés) est le suivant: \n")
                                                    print(A)
                                                elif not(charger):
                                                    print("Veuillez charger d'abord l'automate.\n")
                                                else:
                                                    print("le choix sélectionner n'existe pas")
                                                    os.system("cls")
                                                    liste_choix()










