from os import system
import mysql.connector

database = mysql.connector.connect(host='host',
                                         database=' database_name',
                                         user='user name_phpmyadmin',
                                         password='password phpmyadmin')

cursor = database.cursor()   
def check_res(res):
    if (res.lower() == "yes" or  res.lower() =='y' or res.lower() =='yeah'):
        return 1
    else:
        return 0
    
def output_matrice(matrice):
        for x in enumerate(matrice):
            print('╔════╦════╦════╗'if x[0]==0 else '╠════╬════╬════╣' if x[0]!=3  else '═════╩════╩════')
            for xx in enumerate(x[1]):
               print('║ ',xx[1],'║'if xx[0]==2 else '',end='')
            print('\n',end='')
        print('╚════╩════╩════╝')

def get_data_bdd(match_n):
         print('\n————————————')
         global cursor,database
         cursor.execute(f'SELECT * FROM  datagame WHERE datagame.n_match LIKE {int(match_n)}')
         data_fetchall = cursor.fetchall() 
         print("Match N° ",data_fetchall[0][0],'\n————————————————')
         print("Player WON : ",data_fetchall[0][1],'\n—————————————————————')
         print("Player WON Signe : ",data_fetchall[0][2],'\n—————————————————————')
         output_matrice(eval(data_fetchall[0][3]))          

class Morpion:
    def __init__(self,**Data):
        self.__PLAYER1 = [Data["Pl1_Name"],Data["Pl1_Signe"],[[0,0,0],[0,0,0],[0,0,0]]] #False
        self.__PLAYER2 = [Data["Pl2_Name"],Data["Pl2_Signe"],[[0,0,0],[0,0,0],[0,0,0]]] #True
        self.matrice_game = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.turn = False
        
 
    def ask_position(self):
        while True:
            x = input("Position X ? :")
            y = input("Position Y ? :")
            if (x.isnumeric() and y.isnumeric()):
                x,y  = int(x),int(y)
                if (y< self.matrice_game.__len__() or x < self.matrice_game[0].__len__()):
                    if self.matrice_game[y][x] == ' ':
                        return y,x

    def calc_row(self,matrice)->int:
        for x in range(matrice.__len__()):
            if ((matrice[x][0]+matrice[x][1]+ matrice[x][2])==3):
                return 1
            elif x >= 2:
             return 0
    
    def calc_column(self,matrice)->int:
        for x in range(matrice.__len__()):
            if ((matrice[0][x]+ matrice[1][x]+ matrice[2][x])==3):
                return 1
            elif x >= 2:
             return 0
	    

    def calc_diagonal(self,matrice)->int:
        if((matrice[0][0] + matrice[1][1] + matrice[2][2] == 3) or (matrice[0][2] + matrice[1][1] + matrice[2][0]) == 3):
            return 1
        return 0

    def calc_matrice(self,matrice)->int:
        if(self.calc_row(matrice) or self.calc_column(matrice) or self.calc_diagonal(matrice)):
            return 1
        else:
          return 0

    def who_won(self):
        self.turn.append(self.matrice_game)
        return self.turn

    def run(self):
        self.__PLAYER2[2] = [[0,0,0],[0,0,0],[0,0,0]]
        self.__PLAYER1[2] = [[0,0,0],[0,0,0],[0,0,0]]
        self.matrice_game = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.turn = False
        while True :
            if self.turn:
                print('\n',self.__PLAYER1[0],' turn')
                pos = self.ask_position()
                self.__PLAYER1[2][pos[0]][pos[1]] = 1
                self.matrice_game[pos[0]][pos[1]] = self.__PLAYER1[1]
            elif not self.turn:
                print('\n',self.__PLAYER2[0],' turn')
                pos = self.ask_position()
                self.__PLAYER2[2][pos[0]][pos[1]] = 1
                self.matrice_game[pos[0]][pos[1]] = self.__PLAYER2[1]

            system('clear')
            output_matrice(self.matrice_game)
            self.turn = not self.turn
            if self.calc_matrice(self.__PLAYER1[2]):
                self.turn = self.__PLAYER1
                break
            elif self.calc_matrice(self.__PLAYER2[2]):
                self.turn = self.__PLAYER2
                break
        return self
match=0   
data_won={}
play = check_res(input("Do you want play to the morpion game ? "))
if (play):
    while True:
        print("Match N° ",match,'\n')
        pl1_data = input("Player 1 Name ?/Signe : ").split('/')
        pl2_data = input("Player 2 Name ?/Signe : ").split('/')
        Game = Morpion(Pl1_Name=pl1_data[0],Pl1_Signe=pl1_data[1],Pl2_Name=pl2_data[0],Pl2_Signe=pl2_data[1]).run()
        restart = input("Do you want play the morpion game ? :")
        data_won[match] = Game.who_won()
        if check_res(restart):
            system('clear')
            match+=1
            continue;
        else:
            break
        
if (play and check_res(input("Do you want write games al data to DB yes/no ? "))):
    for x in data_won:
            cursor.execute(f'INSERT INTO datagame(datagame.n_match,datagame.player_won,datagame.player_won_signe,datagame.party_game_data) VALUES({int(x)},"{data_won[x][0]}","{data_won[x][1]}","{data_won[x][3]}")')
            database.commit()


if check_res(input("Do you want get all data from DB yes/no ? ")):
    cursor.execute("SELECT COUNT(*) FROM datagame")
    for x in range(cursor.fetchall()[0][0]):
         get_data_bdd(x)

if check_res(input("Do you want get the specific N° match ? yes/no ")):
    try:
         get_data_bdd(int(input("Number of the match ? : ")))
    except:
        raise "Error to get match number to DB"

