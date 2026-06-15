"""
Python Card War Game
Author: Fatimah Sajjadali
Version: 1.0.0
Description:
A Python implementation of the classic card war game with special cards,
WAR battles, scoring, saving/loading game state using JSON, and a full
round-based game loop.
"""

import random # module that allows to shuffle and pick cards randomly
import json # module that allows to save the game and load it later

#creates a shuffled deck of cards
def deck_cards():
  suits = ['Clubs', 'Diamonds', 'Hearts','Spades']
  ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
  deck = []
  for suit in suits:
    for rank in ranks:
      card = f"{rank} of {suit}" # make a card
      deck.append(card) # add it to the deck
  deck.append('Joker 1')
  deck.append('Joker 2')
  random.shuffle(deck) #shufffles the deck
  return deck

# assign numeric values to each card for comparision
def cards_value(card):
  rank_values ={
      '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14, 'Joker':0
  }
  rank = card.split()[0] # get the first word of the card
  return rank_values.get(rank, 0)

# draws a card from the deck safely
def draw_cards(deck):
  try:
    return deck.pop(0)
  except IndexError:
    print("\n Deck is empty! No more cards to draw.")
    return None # signal that game should stop

# save game state
def save_game(player1_deck, player2_deck, player_names, rounds_played, player_scores, war_cards, rounds_limit):
  filename = input("Enter filename to save the game (exmaple- game1.json): ").strip().lower()
  saved_state = {"player1_deck": player1_deck, "player2_deck": player2_deck, "player_names": player_names, "rounds_played":rounds_played, "player_scores": player_scores, "war_cards": war_cards, "rounds_limit":rounds_limit}
  with open(filename, 'w') as file:
    json.dump(saved_state, file)
  print (f"Game saved successfully to '{filename}'!")

# Load game state
def load_game():
  filename = input("Enter filename to load the game (with .json extension): ").strip().lower()
  try:
    with open(filename, 'r') as file:
      saved_state = json.load(file)
    if not isinstance(saved_state, dict):
            print("Invalid save file.")
            return None
        
    print(f"Game loaded successfully from '{filename}'!")
    return saved_state

  except FileNotFoundError:
    print("Error: No file found!")
    return None

  except json.JSONDecodeError:
        print("Error: Save file is corrupted or not valid JSON.")
        return None

#Handle WAR situation
def handle_war(player1_deck, player2_deck, player_names, player_scores, war_cards):
  print("A WAR HAS BEEN DECLARED!")
  print("--------------------------")

  while True:
    input("Press Enter to start the WAR")

    if len(player1_deck) < 4: # check if player 1 has enough cards to play WAR
      print(f"{player_names[0]} doesn't have enough cards and can't continue WAR! {player_names[1]} wins all remaining cards!")
      player2_deck.extend(war_cards + player1_deck)
      player_scores['player 2'] += len(war_cards + player1_deck)
      player1_deck.clear()
      war_cards.clear()
      return True

    if len(player2_deck) < 4: # check if player 2 has enough cards to play WAR
      print(f"{player_names[1]} doesn't have enough cards and can't continue WAR! {player_names[0]} wins all remaining cards!")
      player1_deck.extend(war_cards + player2_deck)
      player_scores['player 1'] += len(war_cards + player2_deck)
      player2_deck.clear()
      war_cards.clear()
      return True

    input("\nFirst, each player places 3 cards face down...")
    for _ in range(3):
      war_cards.append(draw_cards(player1_deck))
      war_cards.append(draw_cards(player2_deck))

    input("\nNow each player draws their next card face up to decide the WAR!\n")
    player1_war_card = draw_cards(player1_deck)
    player2_war_card = draw_cards(player2_deck)
    war_cards.extend([player1_war_card, player2_war_card])

    print(f"{player_names[0]} reveals: {player1_war_card}")
    print(f"{player_names[1]} reveals: {player2_war_card}")

     #Special cards during war
    if player1_war_card == "Ace of Hearts": # bonus 5 points for player 1
      player_scores['player 1'] += 5
      print(f"SPECIAL CARD {player_names[0]} drew the Ace of Hearts during WAR and gets 5 bonus points!")
    if player2_war_card == "Ace of Hearts": # bonus 5 points for player 2
      player_scores['player 2'] += 5
      print(f"SPECIAL CARD {player_names[1]} drew the Ace of Hearts during WAR and gets 5 bonus points!")

    if "Joker" in player1_war_card or "Joker" in player2_war_card: # both players' scores are reset to zero
      player_scores['player 1'] = 0
      player_scores['player 2'] = 0
      print("OH NO! Joker was drawn during WAR! Both players' scores have been reset to 0")

    if player1_war_card == "King of Spades": # player 1 will steal points from player 2
      steal = min(3, player_scores['player 2'])
      player_scores['player 1'] += steal
      player_scores['player 2'] -= steal
      print(f"SPECIAL CARD!{player_names[0]} drew the King of Spades during WAR and stole {steal} points from {player_names[1]}!")
    if player2_war_card == "King of Spades": # player 2 will steal points from player 1
      steal = min(3, player_scores['player 1'])
      player_scores['player 2'] += steal
      player_scores['player 1'] -= steal
      print(f"SPECIAL CARD!{player_names[1]} drew the King of Spades during WAR and stole {steal} points from {player_names[0]}!")

    value1 = cards_value(player1_war_card)
    value2 = cards_value(player2_war_card)

    input("\nComparing WAR cards.....")

    if value1 > value2:
      print(f"{player_names[0]} wins the WAR and takes {len(war_cards)} cards, earning {len(war_cards)} points!")
      player1_deck.extend(war_cards)
      player_scores['player 1'] += len(war_cards)
      war_cards.clear()
      return True
    elif value2 > value1:
      print(f"{player_names[1]} wins the WAR and takes {len(war_cards)} cards, earning {len(war_cards)} points!")
      player2_deck.extend(war_cards)
      player_scores['player 2'] += len(war_cards)
      war_cards.clear()
      return True
    else:
      if len(player1_deck) < 4 or len(player2_deck) < 4:
        if len(player1_deck) < 4:
            player2_deck.extend(war_cards + player1_deck)
            player1_deck.clear()
            print("Player 1 does not have enough cards to continue WAR! Player 2 wins!")
        else:
            player1_deck.extend(war_cards + player2_deck)
            player2_deck.clear()
            print("Player 2 does not have enough cards to continue WAR! Player 1 wins!")
        war_cards.clear()
        return True
      print("WAR AGAIN! Lets see who wins!!!")
      war_cards.clear()
      return True 

# play a single round
def game_structure(player1_deck, player2_deck, player_names, player_scores, war_cards):

    input(f"Press Enter to draw {player_names[0]}'s card...")
    card1 = draw_cards(player1_deck)
    print(f"\n{player_names[0]} draws: {card1}\n")

    input(f"Press Enter to draw {player_names[1]}'s card...")
    card2 = draw_cards(player2_deck)
    print(f"\n{player_names[1]} draws: {card2}\n")

    # Joker check
    if card1.startswith("Joker") or card2.startswith("Joker"):
        player_scores['player 1'] = 0
        player_scores['player 2'] = 0
        print("\nOH NO! Joker was drawn! Both players' scores have been reset to 0\n")
        input("Press Enter to see the round results and scores...")
        print(f"\n Scores: \n {player_names[0]} - {player_scores['player 1']} \n {player_names[1]} - {player_scores['player 2']}")
        return True  # End round immediately, no points awarded, but continue game

  # Special cards
    if card1 == "Ace of Hearts":# 5 bonus points
        player_scores['player 1'] += 5
        print(f"\nSPECIAL CARD! {player_names[0]} drew the Ace of Hearts and gets 5 bonus points!\n")
    if card2 == "Ace of Hearts": # 5 bonus points
        player_scores['player 2'] += 5
        print(f"\nSPECIAL CARD! {player_names[1]} drew the Ace of Hearts and gets 5 bonus points!\n")

    if card1 == "King of Spades": #gets a points and steals points
        steal = min(3, player_scores['player 2'])
        player_scores['player 1'] += steal
        player_scores['player 2'] -= steal
        print(f"\nSPECIAL CARD! {player_names[0]} drew the King of Spades! {player_names[0]} gets a point and stole {steal} points from {player_names[1]}!\n")
    if card2 == "King of Spades": # gets a point and steals point
        steal = min(3, player_scores['player 1'])
        player_scores['player 2'] += steal
        player_scores['player 1'] -= steal
        print(f"\nSPECIAL CARD! {player_names[1]} drew the King of Spades! {player_names[1]} gets a point and stole {steal} points from {player_names[0]}!\n")

    input("Press Enter to see the round results and scores...\n")

    value1 = cards_value(card1)
    value2 = cards_value(card2)

    if value1 > value2:
        player1_deck.extend([card1, card2])
        player_scores['player 1'] += 1
        print(f"   {player_names[0]} wins the round and gets a point!")
    elif value2 > value1:
        player2_deck.extend([card1, card2])
        player_scores['player 2'] += 1
        print(f"   {player_names[1]} wins the round and gets a point!")
    else:
        print("ITS A TIE!")
        handle_war(player1_deck, player2_deck, player_names, player_scores, war_cards)

    print(f"\n Scores: \n {player_names[0]} - {player_scores['player 1']} \n {player_names[1]} - {player_scores['player 2']}")
    return True

# Main game loop
def game_final():
    print("===========================")
    print("WELCOME TO PYTHON CARD WAR!")
    print("===========================")

    player_names = []
    player1_deck = []
    player2_deck = []
    player_scores = {'player 1': 0, 'player 2': 0}
    war_cards = []
    rounds_played = 0
    rounds_limit = 0
    resume_game = False

    # load game option
    while True:
        load_choice = input("Do you want to load a saved game? (yes/no): ").strip().lower()
        if load_choice in ("yes", "no"):
            break
        print("Please type 'yes' or 'no'.")

    if load_choice == 'yes':
        state = load_game()
        if state:
            player1_deck = state.get('player1_deck',[])
            player2_deck = state.get('player2_deck',[])
            rounds_played = state.get('rounds_played',0)
            player_names = state.get('player_names', ["Player 1", "Player 2"])
            player_scores = state.get('player_scores', {'player 1': 0, 'player 2': 0})
            war_cards = state.get('war_cards', [])
            rounds_limit = state.get('rounds_limit', 0)

            print("\n--- Loaded Game Details ---")
            print(f"{player_names[0]} has {player_scores['player 1']} points and {len(player1_deck)} cards left.")
            print(f"{player_names[1]} has {player_scores['player 2']} points and {len(player2_deck)} cards left.")

            if war_cards:
                print(f"There are {len(war_cards)} cards in WAR pile.\n")
            else:
                print("No cards in WAR")

            print(f"Rounds limit set for this game was: {rounds_limit}")
            print(f"Rounds played: {rounds_played}")
            rounds_left = rounds_limit - rounds_played
            print(f"Rounds left to play: {max(rounds_left, 0)}")
      
            if rounds_limit > rounds_played:
                resume_choice = input("Do you want to resume the game? (yes/no): ").strip().lower()
                if resume_choice == 'yes':
                    resume_game = True
                    print("\nResuming the game.....\n")
                else:
                    new_game = input("Would you like to start a new game instead? (yes/no): ")
                    if new_game == 'yes':
                        print("\nStarting new game.....\n")
                        player_scores = {'player 1': 0, 'player 2': 0}
                        war_cards = []
                    else:
                        print("\nExiting the game...Goodbye!\n")
                        return
            else:
                print("Rounds limit reached in the game.\n")
                
                # Ask user if they want to start a new game
                choice = input("Would you like to start a new game? (yes/no): ").strip().lower()
                if choice == "yes":
                    print("\nStarting new game.....\n")
                    load_choice = 'no'   # force new game setup
                else:
                    print("\nExiting the game... Goodbye!\n")
                    return


        else:
            new_after_error = input("Saved game not found or invalid. Start a new game instead? (yes/no): ").strip().lower()
            if new_after_error == 'yes':
                print("\nStarting new game.....\n")
                load_choice = 'no'
                player_scores = {'player 1': 0, 'player 2': 0}
                war_cards = []
            else:
                print("\nExiting the game...Goodbye!\n")
                return

    # to resume saved and loaded file
    if resume_game:
        print(f"\nResuming the saved game. Rounds left to play: {rounds_limit - rounds_played}\n")
    else:
        deck = deck_cards()
        half = len(deck) // 2
        player1_deck = deck[:half]
        player2_deck = deck[half:]
        
        player_scores = {'player 1': 0, 'player 2': 0}
        war_cards = []

        player_names = [input("Enter Player 1 name: "), input("Enter Player 2 name: ")]
        rounds_played = 0
      
        while True:
            try:
                rounds_limit = int(input ("How many rounds would you like to play?: "))
                if rounds_limit <= 0:
                    print("Please enter a positive number of rounds.")
                else:
                    break
            except ValueError:
                print("Invalid Input! Please enter a valid number of rounds.")

    # Game rounds
    while rounds_played < rounds_limit:       
        print(f"\n--- Round {rounds_played + 1} ---")

        continue_game = input("Press Enter to play this round or type 'exit' to quit the game:").strip().lower()
        if continue_game == "exit":
            print("You chose to exit the game mid-way")
            save_choice = input("\n Would you like to save the game? (yes/no): ")
            if save_choice == 'yes':
                save_game(player1_deck, player2_deck, player_names, rounds_played, player_scores, war_cards, rounds_limit)
            else:
                print("Game not saved, exiting.")
            return

        if len(player1_deck) == 0 or len(player2_deck) == 0:
            print("One player is out of cards! Game over.")
            break

        round_result = game_structure(player1_deck, player2_deck, player_names, player_scores, war_cards)

        if not round_result:
            break

        rounds_played += 1

    print("====================================================")
    print ("GAME OVER!\n")
    print(f"{player_names[0]} has {player_scores['player 1']} points!")
    print(f"{player_names[1]} has {player_scores['player 2']} points!")
    print ("----------------------------------------------------")
  
    if player_scores['player 1'] > player_scores['player 2']:     
        print("<><><><><><><><><><><><><><><><><>")
        print(f"{player_names[0]} IS THE WINNER!")
        print("<><><><><><><><><><><><><><><><><>")
    elif player_scores['player 2'] > player_scores['player 1']:
        print("<><><><><><><><><><><><><><><><><>")
        print(f"{player_names[1]} IS THE WINNER!")
        print("<><><><><><><><><><><><><><><><><>")
    else:
        print("GAME ENDS IN TIE!")

    save_choice = input("Would you like to save the game? (yes/no): ").strip().lower()
    if save_choice == 'yes':
        save_game(player1_deck, player2_deck, player_names, rounds_played, player_scores, war_cards, rounds_limit)
    else:
        print("Game not saved.Exiting.....")


if __name__ == "__main__":
    while True:
        game_final()
        if input("Play again? ").strip().lower() != "yes":
            print("Thank you for playing PYTHON CARD WAR! Goodbye!")
            break
