# -*- coding:UTF8 -*-
import pymysql
import condb
import os
import menu

def qNumberInCat(connectionPar):
    os.system("cls") 
    conn = connectionPar
    c=conn.cursor()    
    c.execute("select count(*) as 'liczba zawodników', category.name_cat as 'Kategoria' from category_has_player join category on category_has_player.category_id_cat = category.id_cat group by category_id_cat;")
    print("############### ILOŚĆ ZAWODNIKÓW W KATEGORIACH #######################")
    j = 1
    for i in c.fetchall():
        print("["+ str(j) +"] Kategoria:", i[1], i[0],"zawodników.")
        j += 1
    print(" ")
    print("[ 1 ] Pokaż rozbicie na wagi")
    print("[ 2 ] Powrót")
    
def qPlayersInWeightCat(connectionPar):
    os.system("cls")
    print("############### ZAWODNICY W KATEGORIACH W ROZBICIU NA WAGI #######################")
    conn = connectionPar
    c=conn.cursor()
    categories ={1:"Junior", 2:"PK", 3:"OFS", 4:"FC", 5:"Kadet", 6:"Młodzieżowiec", 7:"NoGi Białe", 8:"NoGi Kolor"}
    for i in range(1,8):
        c.execute("select count(*) as 'Liczba zawodników', weight_cat.value_weight as waga from category_has_player as c join player as p on c.player_id_p = p.id_p join weight_cat on p.id_weight = weight_cat.id_weight where c.category_id_cat =" + str(i) + " group by weight_cat.value_weight;")
        print("=======  " + categories[i] + "  ===========" )
        print("waga \t Liczba zawodników")
        for j in c.fetchall():
            print(j[1], "\t" , j[0])
    print ('===========================================')
    print ("Aby powrócić wciśnij wciśnij dowolną cyfrę")

def qShowAllTournaments(connectionPar):
    os.system('cls')
    print("################ ZAWODY #################")
    conn = connectionPar
    c=conn.cursor()
    c.execute('select t.name_tourn, t.city_tourn, t.date_tourn, r.rank, t.tourn_is_active from tournament as t join rank as r on t.rank_tourn = r.id_rank order by t.date_tourn desc')
    j = 1
    for i in c.fetchall():
        print("[",j,"] Nazwa: ", i[0], "   Miasto: ", i[1], "   Data: ", i[2], "   Ranga: ", i[3], "   Aktywny: ", i[4])
        j +=1
    print("")
    print("[ 1 ] Zamknij zawody ")
    print("[ 2 ] Powrót")

def qshowCategories(connectionPar):
    c=connectionPar.cursor()
    c.execute("select * from category")
    res = c.fetchall()
    for i in res:
        print("[",i[0],"] ",i[1])

def qshowWeights(connectionPar):
    c=connectionPar.cursor()
    c.execute("select * from weight_cat")
    res = c.fetchall()
    for i in res:
        print("[",i[0],"] ",i[1])    

def aCloseTournament(connectionPar):
    choicemCT = str(input("Wpisz dokładną nazwę zawodów które chesz zamknąć"))
    c=connectionPar.cursor()
    try:
        c.execute("UPDATE `almma`.`tournament` SET `tourn_is_active`='0' WHERE `name_tourn`='"+str(choicemCT)+"';")
        connectionPar.commit()
        print("Zamknięto zawody! Nie możesz już ich edytować.")
    except:
        connectionPar.rollback()
    input("Naciśnij przycisk aby powrócić")
    
def iCreateTournament(connectionPar):
    name = str(input("Podaj nazwę zawodów: "))
    city = str(input("Wpisz miasto: "))            
    date = str(input("Wpisz datę w formacie RRRR-MM-DD: "))
    rank = int(input("Podaj rangę zawodów. 1 dla ALMMA, 2 dla Mistrzostw Polski, 3 dla Pucharu Polski: "))
    c=connectionPar.cursor()
    try:
        c.execute("INSERT INTO `almma`.`tournament` (`name_tourn`, `city_tourn`, `date_tourn`, `rank_tourn`) VALUES ('"+str(name)+"', '"+str(city)+"', '"+str(date)+"', '"+str(rank)+"');")
        print("Zawody zdefiniowano poprawne.")
    except:
        connectionPar.rollback()
        print("Dodawanie nieudane. Sprawdź wpisywane dane.")
    input("Wciśnij dowolny przycisk aby powrócić do menu zarządzania zawodami")


def iDraw(connectionPar):
    id_gt = (1,9,13,5,3,11,15,7,2,10,14,6,4,12,16,8)
    c = connectionPar.cursor()
    c2 = connectionPar.cursor()
    c3 = connectionPar.cursor()
    try:
        for category in range(1,9):
            for weight_cat in range(1,9):
                c2.execute("SET FOREIGN_KEY_CHECKS = 0")
                c.execute("select id_p from player as p join category_has_player as c on p.id_p = c.player_id_p where c.category_id_cat = "+str(category)+" and p.id_weight = "+str(weight_cat)+" and p.verified != 0 order by id_club;")
                players = c.fetchall()
                j = 0
                for i in players:
                    c2.execute("INSERT INTO `almma`.`game_tree` (`id_p`, `id_gt`) VALUES ( "+str(i[0])+", "+str(id_gt[j])+" );")
                    c2.execute("UPDATE `almma`.`player` SET `hashed`='1' WHERE `id_p`='"+str(i[0])+"';")
                    j += 1
        print("Rozpisywanie drzewek wykonane!")
    except:
        print("error") 
    input("Wciśnij dowolny klawisz aby kontynuować.")

def iCreateFights(connetionPar):
    c = connectionPar.cursor()
    c2 = connectionPar.cursor()
    try:
        for category in range(1,9):
            for weight_cat in range(1,9):
                c2.execute("SET FOREIGN_KEY_CHECKS = 0")
                c.execute("select id_p from player as p join category_has_player as c on p.id_p = c.player_id_p where c.category_id_cat = "+str(category)+" and p.id_weight = "+str(weight_cat)+" order by id_club;")
                players = c.fetchall()
                j = 0
                for i in players:
                    c2.execute("INSERT INTO `almma`.`game_tree` (`id_p`, `id_gt`) VALUES ( "+str(i[0])+", "+str(id_gt[j])+" );")
                    j += 1
    except:
        print("error") 
    

def qShowGameTrees(connectionPar, category, weight_cat):
    c=connectionPar.cursor()
    c2=connectionPar.cursor()
    c.execute("select name_cat from category where id_cat ="+str(category))
    c2.execute('select value_weight from weight_cat where id_weight ='+str(weight_cat))
    cat = c.fetchone()
    weight = c2.fetchone()
    print("===== Listę walk dla", cat[0], weight[0], "========")
    print()
    
    

def qFindPlayer(connectionPar):
    os.system('cls')
    c=connectionPar.cursor()   
    print("Podaj dane zawodnika któreg chcesz znaleźć. Aby pominąć dane pole wciśnij ENTER.")
    id = str(input("ID: "))
    if id != "":
            c.execute("select p.id_p, p.name_p, p.last_name_p, w.value_weight, c.name_club,(SELECT count(category_id_cat) FROM almma.category_has_player where player_id_p = p.id_p) as 'Liczba formuł' from player as p join club as c on p.id_club=c.id_club join weight_cat as w on p.id_weight=w.id_weight where p.id_p = '"+str(id)+"' ;")
    else:
        name = str(input("Imię: "))
        secondName = str(input("Nazwisko: "))    
        if name == "":
            c.execute("select p.id_p, p.name_p, p.last_name_p, w.value_weight, c.name_club,(SELECT count(category_id_cat) FROM almma.category_has_player where player_id_p = p.id_p) as 'Liczba formuł' from player as p join club as c on p.id_club=c.id_club join weight_cat as w on p.id_weight=w.id_weight where p.last_name_p = '"+str(secondName)+"' ;")
        elif secondName == "":
            c.execute("select p.id_p, p.name_p, p.last_name_p, w.value_weight, c.name_club, (SELECT count(category_id_cat) FROM almma.category_has_player where player_id_p = p.id_p) as 'Liczba formuł'  from player as p join club as c on p.id_club=c.id_club join weight_cat as w on p.id_weight=w.id_weight where p.name_p = '"+str(name)+"' ;")
        elif name == "" and secondName == "":
            print("Nie wpisałeś danych! ")
        else:
            c.execute("select p.id_p, p.name_p, p.last_name_p, w.value_weight, c.name_club, (SELECT count(category_id_cat) FROM almma.category_has_player where player_id_p = p.id_p) as 'Liczba formuł'  from player as p join club as c on p.id_club=c.id_club join weight_cat as w on p.id_weight=w.id_weight where p.name_p = '"+str(name)+"' and p.last_name_p = '"+str(secondName)+"' ;")
        
    result = c.fetchall()
    print("|%3s|%15s|%25s|%5s|%30s|%12s|" %("ID", "Imię", "Nazwisko", "Waga", "Klub","Liczba Formuł"))
    print("-"*95)
    for i in result:
        print("|%3s|%15s|%25s|%5s|%30s|%12s|" % (i[0], i[1], i[2], i[3],i[4],i[5]))
    input("Wciśnij klawisz ENTER jeżeli skończyłeś przeglądać")
    
def qEditedPlayer(connectionPar, id):
    c=connectionPar.cursor()
    c.execute("select p.id_p, p.name_p, p.last_name_p, w.value_weight, c.name_club,(SELECT count(category_id_cat) FROM almma.category_has_player where player_id_p = p.id_p) as 'Liczba formuł' from player as p join club as c on p.id_club=c.id_club join weight_cat as w on p.id_weight=w.id_weight where p.id_p = "+str(id)+" ;")
    result = c.fetchall()
    print()
    for i in result:
        print("ID: "+str(i[0])+"\t "+str(i[1]) +" "+str(i[2])+ "\t waga: "+str(i[3])+ " klub: "+str(i[4])+"\t walczy w "+str(i[5])+" kategoriach")
        #print("|%3s|%15s|%25s|%5s|%30s|%12s|" % (i[0], i[1], i[2], i[3],i[4],i[5]))
    print()
    
def uChangePlayerName(connectionPar, id):
    newName = str(input("Podaj nowe imię:"))
    c=connectionPar.cursor()
    c.execute("UPDATE player SET name_p ='"+newName+"' WHERE `id_p`='"+str(id)+"' ")
    print("Imię zaktualizowane")
    
def uChangePlayerLastName(connectionPar, id):
    newLastName = str(input("Podaj nowe nazwisko:"))
    c=connectionPar.cursor()
    c.execute("UPDATE player SET last_name_p ='"+newLastName+"' WHERE `id_p`='"+str(id)+"' ")
    print("Nazwisko zaktualizowane")
    
def uChangeWeightCategory(connectionPar, id):
    c=connectionPar.cursor()
    c2 = connectionPar.cursor()
    c.execute("SELECT * FROM almma.weight_cat;")
    print("Z poniższej listy wybierz ID kategorii do której chcesz przypisać zawodnika.")
    print()
    print("|%3s|%4s|" % ("ID", "Waga"))
    print("-"*7)
    categories = c.fetchall()
    for i in categories:
        print("|%3s|%4s|" % (i[0], i[1]))
    status = 0
    while status != 1:
            choice = int(input("Nowa kagegoria: "))
            if 9< choice < 1:
                print("Niewłaściwy wybór. Jeszcze raz.")
            else:
                break
    c2.execute("UPDATE player SET id_weight="+str(choice)+" WHERE id_p="+str(id)+";")
    print("Edycja zakończona")

def qShowPlayerCategories(connectionPar, id):
    print()
    #id = input("Podaj ID zawodnika: ")
    qEditedPlayer(connectionPar, id)
    c=connectionPar.cursor()
    c.execute("SELECT a.player_id_p, c.name_cat FROM almma.category_has_player as a join almma.category as c on a.category_id_cat=c.id_cat where a.player_id_p ="+str(id)+";")
    result = c.fetchall()
    print("|%12s|%30s|" % ("ID zzawodnika", "Formuły")) 
    for i in result:
        print("|%12s|%30s|" % (i[0], i[1])) 
    print()
    return id
    
def iAddPlayerCategory(connectionPar, id):
    os.system('cls')
    print("######### Dodawanie zawodnika do kategorii ##########")
    c=connectionPar.cursor()
    c2=connectionPar.cursor()
    qShowPlayerCategories(connectionPar, id)
    c.execute("select * from category;")
    kategorie = c.fetchall()
    print("|%12s|%20s|" % ("ID kategorii", "Nazwa kategorii"))
    for i in kategorie:
        print("|%12s|%20s|" % (i[0], i[1])) 
    kat = None
    while True:
        kat = int(input("Wpisz ID kategorii do której checesz dodać zawodnika: "))
        if kat<1 or kat>8:
            print("Wpisałeś niepoprawną kategorię")
        else:
            break;
    try:
        c2.execute("INSERT INTO `almma`.`category_has_player` (`player_id_p`, `category_id_cat`) VALUES ('"+str(id)+"', '"+str(kat)+"');")
        print("Kategoria dodana prawidłowo!") 
    except:
        print("Zawodnik walczy już w tej kategorii! Spróbój ponownie.")
    

def uDelPlayerCategory(connectionPar, id):
    qEditedPlayer(connectionPar, id)
    c=connectionPar.cursor()
    c2=connectionPar.cursor()
    c3=connectionPar.cursor()
    c3.execute("SELECT category_id_cat FROM almma.category_has_player where player_id_p = "+str(id)+";")
    pc = c3.fetchall()
    PlayerCategory = []
    for i in pc:
        PlayerCategory.append(str(i[0]))  
    c.execute("select ch.category_id_cat, c.name_cat  from category_has_player as ch join category as c on ch.category_id_cat = c.id_cat where ch.player_id_p = "+str(id)+";")
    result = c.fetchall()
    print("Zawodnik walczy w formułach:")
    print("|%12s|%20s|" % ("ID kategorii", "Nazwa Kategorii")) 
    for i in result:
        print("|%12s|%30s|" % (i[0], i[1])) 
    print()
    while True:
        kat = int(input("Wpisz ID kategorii z której chcesz usunąć zawodnika"))
        if str(kat) not in PlayerCategory:
            print("Nieprawidłowy wybór. Zawodnik nie walczy w tej kategorii!")
            print()
        else:
            break
    try:            
        c2.execute("DELETE FROM `almma`.`category_has_player` WHERE `player_id_p`='"+str(id)+"' and`category_id_cat`='"+str(kat)+"';")
        print("Zawodnik usunięty z podanej kategorii!")
    except Exception:
        print("Usunięcie nie udane.")

def qShowAllWeightsCategories():
    c = menu.setConnection().cursor()
    c.execute("select * from weight_cat;")
    weights = c.fetchall()
    print("|%12s|%10s|" % ("ID kategorii", "Waga (w kg)"))
    print("-"*25)
    for i in weights:
        print("|%12s|%10s|" % (i[0], i[1]))
        
def qShowAllClubs():
    c = menu.setConnection().cursor()
    c.execute("select * from club;")
    clubs = c.fetchall()
    print("|%12s|%30s|" % ("ID klubu", "Nazwa klubu"))
    print("-"*38)
    ClubsIDList = []
    for i in clubs:
        print("|%12s|%10s|" % (i[0], i[1])) 
        ClubsIDList.append(str(i[0]))
    return ClubsIDList

def iAddNewPlayer(connectionPar):
    os.system('cls')
    c = connectionPar.cursor()
    c2 = connectionPar.cursor()
    print("###### Dodawanie nowego zawodnika ######")
    name = ""
    lastName = ""
    weight = ""
    club = ""
    while True:
        if name == "":
            name = str(input("Wpisz imie:"))
        else:
            break
        
    while True:
        if lastName == "":
            lastName = str(input("Wpisz nazwisko:"))
        else:
            break    

    qShowAllWeightsCategories()
    while True:
        if weight == "":
            weight = str(input("Wpisz ID kategorii wagowej z tabeli powyżej:"))
        elif int(weight) < 0 and int(weight) > 8:
            weight = str(input("Niepoprawna wartość! Wpisz ID kategorii wagowej z tabeli powyżej:"))
        else:
            break    
    print()
    listIDClubs = qShowAllClubs()
    while True:
        if club == "":
            club = str(input("Wpisz ID klubu z tabeli powyżej:"))
        elif club not in listIDClubs:
            club = str(input("Niepoprawna wartość! Wpisz ID kategorii wagowej z tabeli powyżej:"))
        else:
            break    
    print(name, lastName, weight, club)
    c2.execute("INSERT INTO `almma`.`player` (`name_p`, `last_name_p`, `id_weight`, `id_club`) VALUES ('"+str(name)+"', '"+str(lastName)+"', '"+str(weight)+"', '"+str(club)+"');")
    c.execute("select id_p from player where name_p = '"+str(name)+"' and last_name_p = '"+str(lastName)+"' and id_weight = '"+str(weight)+"' and id_club = '"+str(club)+"';")
    getID = c.fetchone()
    id = getID[0]
    
    print("Dopisz zawodnika do kategorii.")
    iAddPlayerCategory(connectionPar, id)
    print("Zawodnik dodany prawidłowo!")