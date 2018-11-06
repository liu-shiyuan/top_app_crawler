# -*- coding:utf-8 -*-


class IOSGameCategory:
    CATEGORY_ALL = '6014'
    CATEGORY_ACTION = '7001'
    CATEGORY_ADVENTURE = '7002'
    CATEGORY_ARCADE = '7003'
    CATEGORY_BOARD = '7004'
    CATEGORY_CARD = '7005'
    CATEGORY_CASINO = '7006'
    CATEGORY_DICE = '7007'
    CATEGORY_EDUCATION = '7008'
    CATEGORY_FAMILY = '7009'
    CATEGORY_KIDS = '7010'
    CATEGORY_MUSIC = '7011'
    CATEGORY_PUZZLE = '7012'
    CATEGORY_RACING = '7013'
    CATEGORY_ROLE_PLAYING = '7014'
    CATEGORY_SIMULATION = '7015'
    CATEGORY_SPORTS = '7016'
    CATEGORY_STRATEGY = '7017'
    CATEGORY_TRIVIA = '7018'
    CATEGORY_WORD = '7019'


ios_game_category_names = [
    {
        "display": "Games",
        "code": IOSGameCategory.CATEGORY_ALL
    },
    {
        "display": "Action",
        "code": IOSGameCategory.CATEGORY_ACTION
    },
    {
        "display": "Adventure",
        "code": IOSGameCategory.CATEGORY_ADVENTURE
    },
    {
        "display": "Arcade",
        "code": IOSGameCategory.CATEGORY_ARCADE
    },
    {
        "display": "Board",
        "code": IOSGameCategory.CATEGORY_BOARD
    },
    {
        "display": "Card",
        "code": IOSGameCategory.CATEGORY_CARD
    },
    {
        "display": "Casino",
        "code": IOSGameCategory.CATEGORY_CASINO
    },
    {
        "display": "Dice",
        "code": IOSGameCategory.CATEGORY_DICE
    },
    {
        "display": "Education",
        "code": IOSGameCategory.CATEGORY_EDUCATION
    },
    {
        "display": "Family",
        "code": IOSGameCategory.CATEGORY_FAMILY
    },
    {
        "display": "Kids",
        "code": IOSGameCategory.CATEGORY_KIDS
    },
    {
        "display": "Music",
        "code": IOSGameCategory.CATEGORY_MUSIC
    },
    {
        "display": "Puzzle",
        "code": IOSGameCategory.CATEGORY_PUZZLE
    },
    {
        "display": "Racing",
        "code": IOSGameCategory.CATEGORY_RACING
    },
    {
        "display": "Role Playing",
        "code": IOSGameCategory.CATEGORY_ROLE_PLAYING
    },
    {
        "display": "Simulation",
        "code": IOSGameCategory.CATEGORY_SIMULATION
    },
    {
        "display": "Sports",
        "code": IOSGameCategory.CATEGORY_SPORTS
    },
    {
        "display": "Strategy",
        "code": IOSGameCategory.CATEGORY_STRATEGY
    },
    {
        "display": "Trivia",
        "code": IOSGameCategory.CATEGORY_TRIVIA
    },
    {
        "display": "Word",
        "code": IOSGameCategory.CATEGORY_WORD
    }
]


class AndroidGameCategory:
    CATEGORY_ALL = '2'
    CATEGORY_ACTION = '38'
    CATEGORY_ADVENTURE = '39'
    CATEGORY_ARCADE = '41'
    CATEGORY_BOARD = '42'
    CATEGORY_CARD = '43'
    CATEGORY_CASINO = '44'
    CATEGORY_CASUAL = '6'
    CATEGORY_EDUCATIONAL = '46'
    CATEGORY_FAMILY = '47'
    CATEGORY_LIVE_WALLPAPER = '7'
    CATEGORY_MUSIC = '48'
    CATEGORY_PUZZLE = '49'
    CATEGORY_RACING = '8'
    CATEGORY_ROLE_PLAYING = '51'
    CATEGORY_SIMULATION = '52'
    CATEGORY_SPORTS = '9'
    CATEGORY_STRATEGY = '54'
    CATEGORY_TRIVIA = '55'
    CATEGORY_WIDGETS = '10'
    CATEGORY_WORD = '40'
    CATEGORY_ARCADE_AND_ACTION = '3'
    CATEGORY_BRAIN_AND_PUZZLE = '4'
    CATEGORY_CARDS_AND_CASINO = '5'


android_game_category_names = [
    {
        "display": "Games",
        "code": AndroidGameCategory.CATEGORY_ALL
    },
    {
        "display": "Action",
        "code": AndroidGameCategory.CATEGORY_ACTION
    },
    {
        "display": "Adventure",
        "code": AndroidGameCategory.CATEGORY_ADVENTURE
    },
    {
        "display": "Arcade",
        "code": AndroidGameCategory.CATEGORY_ARCADE
    },
    {
        "display": "Board",
        "code": AndroidGameCategory.CATEGORY_BOARD
    },
    {
        "display": "Card",
        "code": AndroidGameCategory.CATEGORY_CARD
    },
    {
        "display": "Casino",
        "code": AndroidGameCategory.CATEGORY_CASINO
    },
    {
        "display": "Casual",
        "code": AndroidGameCategory.CATEGORY_CASUAL
    },
    {
        "display": "Educational",
        "code": AndroidGameCategory.CATEGORY_EDUCATIONAL
    },
    {
        "display": "Family",
        "code": AndroidGameCategory.CATEGORY_FAMILY
    },
    {
        "display": "Live Wallpaper",
        "code": AndroidGameCategory.CATEGORY_LIVE_WALLPAPER
    },
    {
        "display": "Music",
        "code": AndroidGameCategory.CATEGORY_MUSIC
    },
    {
        "display": "Puzzle",
        "code": AndroidGameCategory.CATEGORY_PUZZLE
    },
    {
        "display": "Racing",
        "code": AndroidGameCategory.CATEGORY_RACING
    },
    {
        "display": "Role Playing",
        "code": AndroidGameCategory.CATEGORY_ROLE_PLAYING
    },
    {
        "display": "Simulation",
        "code": AndroidGameCategory.CATEGORY_SIMULATION
    },
    {
        "display": "Sports",
        "code": AndroidGameCategory.CATEGORY_SPORTS
    },
    {
        "display": "Strategy",
        "code": AndroidGameCategory.CATEGORY_STRATEGY
    },
    {
        "display": "Trivia",
        "code": AndroidGameCategory.CATEGORY_TRIVIA
    },
    {
        "display": "Widgets",
        "code": AndroidGameCategory.CATEGORY_WIDGETS
    },
    {
        "display": "Word",
        "code": AndroidGameCategory.CATEGORY_WORD
    },
    {
        "display": "Arcade & Action",
        "code": AndroidGameCategory.CATEGORY_ARCADE_AND_ACTION
    },
    {
        "display": "Brain & Puzzle",
        "code": AndroidGameCategory.CATEGORY_BRAIN_AND_PUZZLE
    },
    {
        "display": "Cards & Casino",
        "code": AndroidGameCategory.CATEGORY_CARDS_AND_CASINO
    }
]

game_category_names = ios_game_category_names + android_game_category_names


if __name__ == '__main__':
    print(game_category_names)
    print(len(game_category_names))
