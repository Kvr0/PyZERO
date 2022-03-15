
from enum import Enum
import random

from numpy import number


class Card:
    '''
    ゲームで使用するカード
    '''
    class Color(Enum):
        Red = 0xff0000
        LightBlue = 0x00ffff
        Green = 0x00ff00
        Brown = 0x8b4513
        Blue = 0x4169e1
        Yellow = 0xffff00
        Purple = 0xff00ff

        def __init__(self,color:int) -> None:
            super().__init__()
            self.color = color

    allColor = [Color.Red,Color.LightBlue,Color.Green,Color.Brown,Color.Blue,Color.Yellow,Color.Purple]

    def __init__(self, color:Color, number:int) -> None:
        self.color = color
        self.number = number

    def __str__(self) -> str:
        r = (self.color.color & 0xff0000) >> 16
        g = (self.color.color & 0x00ff00) >> 8
        b = (self.color.color & 0x0000ff)
        return f'\033[38;2;{r};{g};{b}m{self.number}\033[0m'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.color == other.color & self.number == other.number

class Deck(object):
    '''
    デッキ
    '''
    def __init__(self) -> None:
        super().__init__()
        self.cards:list[Card] = []
        for c in range(7):
            for n in range(8):
                self.cards.append(Card(Card.allColor[c],n+1))

    def __str__(self) -> str:
        return str(self.cards)

    def __repr__(self) -> str:
        return self.__str__()

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self,num=1) -> list[Card]:
        ret = []
        for i in range(num):
            ret.append(self.cards.pop())
        return ret

class Hand(object):
    '''
    手札
    '''
    def __init__(self,cards:list[Card]) -> None:
        self.cards:list[Card] = cards

    def __str__(self) -> str:
        return str(self.cards)

    def __repr__(self) -> str:
        return self.__str__()

class Field(object):
    '''
    場
    '''
    def __init__(self,cards:list[Card]) -> None:
        self.cards:list[Card] = cards

    def __str__(self) -> str:
        return str(self.cards)

    def __repr__(self) -> str:
        return self.__str__()


class Player(object):
    '''
    プレイヤー
    '''
    def __init__(self,hand:Hand) -> None:
        self.hand = hand

    def __str__(self) -> str:
        return str(self.hand)

    def __repr__(self) -> str:
        return self.__str__()


    def getScore(self) -> int:
        hand_buf = self.hand
        # Color
        for i in range(7):
            if sum(1 for card in hand_buf.cards if Card.allColor[i] == card.color) >= 5:
                hand_buf.cards = [c for c in hand_buf.cards if c.color != Card.allColor[i]]
        # Number
        for i in range(8):
            if sum(1 for card in hand_buf.cards if i+1 == card.number) >= 5:
                hand_buf.cards = [c for c in hand_buf.cards if c.number != i+1]
        # Score
        score = sum(set([c.number for c in hand_buf.cards]))
        return score

class Game:
    def __init__(self,player_num:int) -> None:
        self.deck = Deck()
        self.deck.shuffle()
        self.player:list[Player] = [Player(Hand(self.deck.draw(9))) for _ in range(player_num)]
        self.field = Field(self.deck.draw(5))
    
    def __str__(self) -> str:
        return f'(P:{self.player},F:{self.field})'

    def __repr__(self) -> str:
        return self.__str__()


game = Game(2)
print(game)