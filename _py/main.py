#*-* coding: UTF8 *-*
import sys
#sys.path.append('C:\\Users\\user\\Desktop\\almma\\lib')
sys.path.append('C:\\Users\\user\\Dysk Google\\Almma\\_py\\lib')
import pymysql
import lib.signin
import lib.menu
import lib.zapytania

almma = lib.signin.signin()

status = 0
while status == 0:
    lib.menu.showMainMenu(almma.getUG())
    choice = lib.menu.menuChoice()
    if choice == 1:
        lib.menu.menuAdmin()
    if choice == 2:
        lib.menu.menuShowGameTrees()
    if choice == 3:
        lib.menu.menuPlayers()
    if choice == 4:
        sys.exit()
