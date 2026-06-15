# Python-Card-War-Game
A Python card war game with special cards, scoring, WAR battles, and save/load functionality.

A Python implementation of the classic card war game featuring special cards,
WAR battles, scoring, saving/loading game state, and a full round-based game loop.

## Key Features
- Fully shuffled deck with Jokers
- Special cards (Ace of Hearts, King of Spades, Joker effects)
- WAR battles with multi-card draws
- JSON save/load system
- Round limits and resume functionality
- Player names and score tracking
- Input validation and error handling
- Replay option

## How It Works
Each round:
1. Both players draw a card.
2. Special cards may trigger bonus points or penalties.
3. If cards tie → WAR begins.
4. Scores update automatically.
5. Game continues until round limit or a player runs out of cards.

Players can:
- Start a new game
- Load a saved game
- Resume a partially played game
- Save progress at any time

## Technologies Used
- Python
- `random` module (shuffling)
- `json` module (saving/loading)
- Console-based UI

## How to Run
1. Run the script:
   python Python-CardWarGame.py

2. Follow on-screen instructions to play.

## Screenshot
![Program Screenshot](card_game_screenshot.png)

## Project Structure
Python-Card-War-Game/
├── Python-CardWarGame.py   # Main game code  
├── README.md               # Documentation  
└── LICENSE                 # MIT license  

## Future Improvements
- Add GUI version using Tkinter or PyQt
- Add multiplayer online mode
- Add sound effects
- Add card graphics
- Add difficulty levels
- Add statistics tracking

## Contact
Created by Fatimah Sajjadali — feel free to reach out!

## License
This project is licensed under the MIT License.

