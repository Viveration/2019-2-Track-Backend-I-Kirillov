class TicTacToe:
    def __init__(self):
        coordinates = [i for i in range(1, 10)]
        self.player = 1
        self.coordinates = coordinates
        self.mark = ['X', 'O']
        self.field = [j + 1 for j in range(0, 9)]
        self.allovedCoordinates = coordinates

    def situationCheck(self):
        waysToWin = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
                                (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for row in waysToWin:
            if (self.field[row[0]] == self.field[row[1]] ==
                    self.field[row[2]]) and \
                    (self.field[row[0]] == 'O' or self.field[row[0]] == 'X'):
                winner = self.mark[self.player-1]
                print("The winner is: ", winner)
                return 0
        if len(self.allovedCoordinates) == 0:
            print("It's a tie!")
            return 0
        return 1

    def printField(self):
        print('-------')
        i = 0
        for element in self.field:
            print("|{}".format(element), end='')
            i += 1
            if i % 3 == 0:
                print('|')
                print('-------')

    def changePlayer(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def start(self):
        print("Welcome to the TicTacToe!")
        print("To start the game type 'start'")
        print("If you want to leave, just type something else")
        startOrNot = input()
        if startOrNot == 'start':
            self.player = 1
            print('Coordinates of the field:')
            self.printField()
            field = [' ' for i in range(0, 9)]
            self.field = field
            print("X first!")
            self.game()
        else:
            return

    def game(self):
        while 1:
            while 1:
                print("Enter coordinate: ", *self.allovedCoordinates)
                rawCoordinate = input()
                try:
                    coordinate = int(rawCoordinate)
                except ValueError:
                    coordinate = -1
                if coordinate in self.allovedCoordinates:
                    self.allovedCoordinates.remove(coordinate)
                    break
                print('Wrong coordinate!')
            self.field[coordinate-1] = self.mark[self.player-1]
            self.printField()
            check = self.situationCheck()
            if check == 0:
                return
            self.changePlayer()


if __name__ == '__main__':
    game = TicTacToe()
    game.start()
