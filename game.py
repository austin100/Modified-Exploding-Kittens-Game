import random # For choosing random cards 
import time # For making the program run longer
import sys # To break out of program 

numgames = 1 
try: 
    with open('record.txt','r') as file:
        # print(file.read())
        lines = file.readlines()
        # print('Before stripping', lines)
        # print(lines[2:])

        # Remove first two lines 
        x = lines[2:]
        # print(x)
        
        cleanedlines = []
        # Remove all \n
        for line in x: 
            if line[-1] == '\n':
                cleanedlines.append(line.strip('\n'))

        # print('After stripping:', cleanedlines)

        gamelines = [] 
        for line in cleanedlines: 
            if line[0:5] == 'Game:':
                gamelines.append(line)
        
        # If there are no games in the record, set the first game to 1, else use the previous game round 
        if len(gamelines) == 0: 
            numgames = 1
        else: 
            # print('All games played:', gamelines)

            # Get last the last number of the last game 
            
            # print(gamelines[-1])
            # print(gamelines[-1].split(":")) # Creates a list of elements "Game" and #
            # print(gamelines[-1].split(":")[1])

            lastgame = int(gamelines[-1].split(":")[1])
            
            # print('LastGame:', lastgame)
            numgames = lastgame + 1 
    # print('Number games:', numgames)
except FileNotFoundError: # No record exists in folder --> Create new one 
        with open('record.txt','w') as file:
            file.write("Here is a record of all games played:\n")


class Game: 
    # Create variables upon making the class Game 
    def __init__(self):
        self.maindeck = [] # Create the main deck
        # Automatically given each player a Defuse card 
        self.playerdeck = {"Defuse": 1} # Create the player's deck
        self.botdeck = {"Defuse": 1} # Create the bot's deck
        self.playerturn = "" # Whose turn (player or bot) it is 
         
        self.totalturnsplayed = 0 

        self.gamenotwon = True 
    
    # Method of adding a new record to "record.txt" after a game is complete 
    def writetorecord(self, numgames=0, playerwon=None, playerlost=None):
        try:
            with open('record.txt', 'a') as file: 
                file.write(f"\nGame:{numgames}\nWinner:{playerwon}\nLoser:{playerlost}\n")
        except FileNotFoundError:
            print("File not found, or 'writetorecord' function does not work")

    # This function creates the player and bot decks. 
    # What it does is takes all cards in the game, and for each player (player or bot), gives them 7 cards
    # Thus each player has a total of 8 cards. When each player has 8 total cards in their deck, we take the remaining cards and set it as our main deck.
    # We also add in our Exploding Kitten card and randomly shuffle the deck.
    def create_decks(self):
        possiblecards = ["Defuse", "Shuffle","Shuffle", 
                         "See The Future(3x)", "See The Future(3x)", "See The Future(3x)", 
                         "Favor","Favor","Favor", 
                         "Skip", "Skip", "Skip", 
                         "Attack(2x)", "Attack(2x)", 
                         "TacoCat", "RainbowRalphingCat", "BeardCat", 
                         "TacoCat", "RainbowRalphingCat", "BeardCat", 
                         "TacoCat", "RainbowRalphingCat", "BeardCat", 
                         "TacoCat", "RainbowRalphingCat", "BeardCat",  
                         "Skip", "Skip", "Skip"] 
        # Give 7 cards to each player (Excluding the Defuse card already in each persons deck)
        while sum(self.playerdeck.values()) < 8:
            card = random.choice(possiblecards)
            if card in self.playerdeck:
                self.playerdeck[card] += 1 
            else:
                self.playerdeck[card] = 1
            possiblecards.remove(card)

        while sum(self.botdeck.values()) < 8:
            card = random.choice(possiblecards)
            if card in self.botdeck:
                self.botdeck[card] += 1 
            else:
                self.botdeck[card] = 1
            possiblecards.remove(card)
        
        # Testing that the decks are actually set 
        # print("Player deck set!: ", self.playerdeck)
        # print("Bot deck set!: ", self.botdeck)
        # # print(len(possiblecards))
        # # print("Remaining cards left:", possiblecards)

        self.maindeck = possiblecards
        # self.main = ["Defuse"] --> For testing

        self.maindeck += ["Exploding Kitten!"]

        # print("Deck before shuffling:", self.maindeck)

        random.shuffle(self.maindeck)
        # print("Created Main Deck:",self.maindeck)

    # this function determines which player goes first, based on 50% probability  
    def gamestart(self):
        if random.randint(1,2) == 1:
            self.playerturn = "Player"
        else:
            self.playerturn = "Bot" 

        # print(self.playerturn)

    # Shuffle card --> Randomly shuffles the deck 
    def shuffledeck(self,player):
        # print("Deck before shuffling:", self.maindeck)
        print(f"{player} Shuffled Deck!")
        random.shuffle(self.maindeck)

        # print("Deck after shuffling:", self.maindeck)

    # See the future
    # Grabs first three cards in the main deck list, and shows it in the file "See the future.txt"
    def seefuture(self):
        x = self.maindeck[0:3] # Grab the first three cards in the main deck list
        # print("First three cards:", x)
        output = "" # Create an output 
        with open("See the future.txt","w") as file: # Take each element in x and write it to the file 
            for card in x:
                output += card + "\n"
            file.write(output)
    
    # This function steals a card from the player's opponent, depending on the type of card played ("Favor", "Attack(2x)", "TacoCat", "RainbowRalphingCat", "BeardCat")
    def attackplayer(self,playerattacked, typeofattack):
        global numgames
        # If bot is being attacked, set their deck to be attacked and keep the other player's deck safe
        if playerattacked == "Bot":  # Bot is who we are stealing card   
            safeplayer = "Player" # Player is who is taking the cards
            safedeck = self.playerdeck
            attackdeck = self.botdeck 
        # If player is being attacked 
        if playerattacked == "Player": # Player is who we are stealing card
            safeplayer = "Bot"
            attackdeck = self.playerdeck 
            safedeck = self.botdeck  
       
        print(f"{safeplayer} plays '{typeofattack}' on {playerattacked}!")
        
        
        try:
            # Steal cards from other player 
            total_cards = sum(attackdeck.values())
            if total_cards == 0: # Check if opponent's deck is empty
                print(f"{playerattacked} has no cards left in their deck! Choose another card!")
                return 
            elif total_cards < 2 and typeofattack == "Attack(2x)": # If "Attack(2x)" card is played but opponent has less than 2 cards => Break 
                print(f"{playerattacked} has only one card left in their deck! Choose another card!")
                return
            
            # Steal card from other player
            # This picks a random card and lower's the amount by one 
            def stealacard(playerdeckattacked):
                card = (random.choice(list(attackdeck.keys()))) # Get a random card
                playerdeckattacked[card] -= 1  # For the opponent, lower card count by 1 
                if playerdeckattacked[card] == 0: # If the card count for that count reaches 0, delete it 
                    del playerdeckattacked[card]
                return card 
            
            # Depending on the card played is how many times the card is deducted from the safeplayer's deck (the one doing the stealing)
            if typeofattack in ["TacoCat", "RainbowRalphingCat", "BeardCat"]: # If cat cards played, lower count by 2 
                safedeck[typeofattack] -= 2 
            else: 
                safedeck[typeofattack] -= 1 # If played any other card ("Favor", "Attack(2x)"), lower count by 1 
            if safedeck[typeofattack] <= 0: # If there are no cards left after play, delete the key for it
                del safedeck[typeofattack]
             
            # Here, depending on the card played is how many times we steal a card 
            # If "Attack(2x)" is played, STEAL TWO CARDS; else just steal 1 card
            stolencards = []
            if typeofattack == "Favor":
                stolencards.append(stealacard(attackdeck))
            elif typeofattack == "TacoCat":
                stolencards.append(stealacard(attackdeck))
            elif typeofattack == "RainbowRalphingCat":
                stolencards.append(stealacard(attackdeck))
            elif typeofattack == "BeardCat":
                stolencards.append(stealacard(attackdeck))
            else:
                stolencards.append(stealacard(attackdeck))
                stolencards.append(stealacard(attackdeck))

            # print(stolencards)
        except:
            print("Theres an error in stealing cards from player")

        
        print(f"{safeplayer} took cards: {stolencards} from {playerattacked}!")

        # Based on each card stolen, we either create a new key or add to an existing card key for each card stolen  
        for card in stolencards:
            if card in safedeck:
                safedeck[card] += 1
            else:
                safedeck[card] = 1 
        
        
        
    # This function is for drawing a card from the main deck, based on whose doing the "drawing" (Player or Bot)
    # First, it takes the first card (index 0) and then checks to see if it is an exploding kitten
    # If it is, lower the amount of defuse cards in that player's deck
        # If that player has no defuse cards left, the other player wins 
    # If it isn't, add the card to the player's hand
    def drawacard(self, player):
        global numgames
        # Determine whose deck we are drawing for (player or bot)
        playerdeck = ""
        if player == "Player":
            playerdeck = self.playerdeck 
        else:
            playerdeck = self.botdeck 
        
        drawncard = self.maindeck[0] # Find what first card is in main deck
        self.maindeck.pop(0) # Remove first card in main deck 
        print(f"{player} drew card: {drawncard}")

        if drawncard == "Exploding Kitten!": 
            # Check if card is exploding kitten
            # If yes, check if player or bot (depending on turn) can defuse it 
            print(f"Exploding Kitten drawn! Minus 1 defuse card for {player}")
            if playerdeck.get("Defuse",0) > 0:
                playerdeck["Defuse"] -= 1 
                
                print("Exploding Kitten Placed Back in Deck.")
            
                self.maindeck.insert(random.randint(0,len(self.maindeck)),"Exploding Kitten!")
                # print("Main Deck:", self.maindeck)

                if playerdeck.get("Defuse",0) <= 0:
                    del playerdeck["Defuse"]
            else:
            # If cannot defuse it, end the game 
                self.gamenotwon = False
                
                # If the player who drew the card is "Player" and they explode, write to record
                if player == "Player":
                    print("Player had no defuse cards left!")
                    print("Game over! Player explodes and Bot wins!")
                    print("Total number of turns played in game:", str(self.totalturnsplayed))
                    

                    self.writetorecord(numgames,"Bot", "Player") # Write to the record
                else: 
                # Else write to Bot
                    print("Bot had no defuse cards left!")
                    print("Game over! Bot explodes and Player wins!")
                    print("Total number of turns played in game:", str(self.totalturnsplayed))
                     

                    self.writetorecord(numgames,"Player", "Bot") # Write to the record 
                
        else:
            # If drawncard is not an Exploding Kitten, create or add to a card key in the player's dictionary 
            if drawncard in playerdeck: 
                playerdeck[drawncard] += 1
            else: 
                playerdeck[drawncard] = 1 
        # Switch turns to the opposite player (I.e. if player draws card, now it is the bot's turn)
        if player == "Player":
            self.playerturn = "Bot"
        else:
            self.playerturn = "Player"
        print(f"{player} ends their turn")        

# Play the actual game                      
def playgame():
    # Create the game, decks (main, player, hand), and determine who goes first

    print('''Welcome to my modified version of Exploding Kittens! \n''')
    print('''You will play against a bot! \n''')
    print('''When it is your turn, play as many action cards as you want from your deck, and end your turn by drawing a card. \n''')
    print('''Cards lower your chances from getting an Exploding Kitten, which reduces the number of lives.\n\n''')

    time.sleep(3)
    # A loop to check if the player wants to play the game 
    while True: 
        try:  
            ready = input("Are you ready to face against the bot? (Type y/n): ")
            if ready == "y" or ready == "Y" or ready == "yes" or ready == "Yes": # Check for player response
                print("Game Start!") # Ready --> break 
                break 
            elif ready == "n" or ready == "N" or ready == "no" or ready == "No": # Check for player response
                print("User exited")
                sys.exit() # Not ready --> exit out of the game 
            else:
                print("Invalid input --> Type 'y' or 'n'") # Check to see if it is a valid input
        except: 
            return "Error somewhere"

    time.sleep(3)
    print('\n')

    game = Game() # create the game 
    # print("Main Deck:", game.maindeck)
    # print("Player Deck:",game.playerdeck)
    # print("Bot Deck:",game.botdeck)
    game.create_decks() # create the decks 
    # print("Main Deck:",game.maindeck)
    game.gamestart() # start the game by chosing the player that goes first 
    print("Game#:",numgames)
    # print("Your deck is:", game.playerdeck)
    # print("\n")

    print("Who starts first:",game.playerturn)

    try: 
        # Loop for game (On condition that either player (Bot or user) has not won yet)
        while game.gamenotwon:    
            
            print('\n' * 2)
            print("Player turn:",game.playerturn)

            # IF it is the player's turn 
            if game.playerturn == "Player":
                # Increase number of turns by 1 
                game.totalturnsplayed += 1 
                print("Turn #:",game.totalturnsplayed)

                
                # While it is the player's turn, the user can play any card they want 
                while game.playerturn == "Player":
                    

                    print("Your Deck:\n",game.playerdeck)

                    print("\n")

                    # print("\n")
                    # print("Player deck:", game.playerdeck)
                    # print("Bot deck", game.botdeck)
                    # print("\n")
                    
                    # Ask user what card they want to play 
                    cardselection = str(input('''What card do you want to play? \nTo play cards, type them exactly how they are shown in your deck \nIf you don't want to/ cannot play any cards, type 'Draw card': \n'''))
                    
                    # Defuse card -> Cannot play this card
                    if cardselection == "Defuse":
                        print(f"Cannot play card: {cardselection}; Choose another! \n")

                    # See the Future card
                    elif cardselection == "See The Future(3x)" or cardselection == "See The Future(3x) " or cardselection == "See the Future" or cardselection == "See the future": # If user selects this card 
                        if game.playerdeck.get("See The Future(3x)",0) >= 1: # Check if there are enough in the deck
                            print("See The Future! Check file 'See the future.txt' for the next 3 cards!")
                            game.seefuture() # Yes --> Allow player to see next three cards   
                            game.playerdeck["See The Future(3x)"] -= 1 # Lower card amount by 1
                            if game.playerdeck["See The Future(3x)"] == 0:
                                del game.playerdeck["See The Future(3x)"]
                        else:
                            print("Not enough See The Future cards! \n") # If not enough cards, remind player 

                    # Shuffle card
                    elif cardselection == "Shuffle" or cardselection == "Shuffle " or cardselection == "shuffle":
                        if game.playerdeck.get("Shuffle",0) >= 1: # Check if enough shuffle cards (1 min.)
                            game.shuffledeck("Player") # Yes --> shuffle deck
                            game.playerdeck["Shuffle"] -= 1 # Lower card amount by 1 
                            if game.playerdeck["Shuffle"] == 0:
                                del game.playerdeck["Shuffle"]
                        else:
                            print("Not enough Shuffle cards! \n") # If not enough shuffle cards, remind player 

                    # Skip card
                    elif cardselection == "Skip" or cardselection == "Skip " or cardselection == "skip":
                        if game.playerdeck.get("Skip",0) >= 1: # Check if enough skip cards (1 minimum)
                            print("Player Skips!")
                            game.playerdeck["Skip"] -= 1 
                            if game.playerdeck["Skip"] == 0: # Delete if card amount is 0 
                                del game.playerdeck["Skip"]
                            game.playerturn = "Bot" # Yes --> skip turn; Set turn to opponent (Bot)
                            break 
                        else:
                            print("Not enough Skip cards! \n") # If not enough skip cards, remind player 
                    
                    # Favor card
                    elif cardselection == "Favor" or cardselection == "Favor " or cardselection == "favor":
                        if game.playerdeck.get("Favor",0) >= 1: # Check if enough favor cards (1 minimum)
                            game.attackplayer("Bot", "Favor")  # Yes --> attack bot
                            # print("Attacking w/ Favor on bot works")
                        else: 
                            print("Not enough Favor cards! Try a different card! \n") # No --> remind player
                    
                    # TacoCat, RainbowRalphingCat, BeardCat
                    elif cardselection in ["TacoCat", "RainbowRalphingCat", "BeardCat"]:
                        if game.playerdeck.get(cardselection,0) >= 2: # Check if enough cat cards (2 minimum)
                            
                            game.attackplayer("Bot", cardselection) # Yes --> attack bot
                            # print("Attacking w/ cat cards works")
                        else: 
                            print(f"Not enough {cardselection}s (Need 2) \n") # No --> remind player

                    # Attack card --> Forces opponent to draw 2 cards 
                    elif cardselection == "Attack(2x)":
                        if game.playerdeck.get(cardselection,0) >= 1: # Check if enough attack cards (1 minimum)
                            game.attackplayer("Bot", "Attack(2x)")  # Yes --> attack bot
                        else:
                            print("Not enough Attack cards! \n")   # No --> remind player     

                    # If player decides to end their turn, end turn by drawing a card 
                    elif cardselection == "Draw card" or cardselection == "Draw card " or cardselection == "Draw cards": # Player draws a card from the deck and ends turn
                        # Draw cards
                        game.drawacard("Player")
                        break 
                    else:
                        print(f"Invalid card or command!")

                    time.sleep(3) 
                # When the player ends their turn with "Draw card" command, print out in the terminal that the player ends their turn 
                if cardselection != "Draw card" or cardselection == "Draw card " or cardselection == "Draw cards":
                    print(f"Player ends turn")  

            elif game.playerturn == "Bot":

                skipturn = False # For skipping turn 
                game.totalturnsplayed += 1 # Increase number of turns 
                print("Turn #:",game.totalturnsplayed)

                # For the Bot's "brain"/"strategy", the bot will try to skip their turn or steal a card from the Player
                while game.playerturn == "Bot":
                    # First determine if the bot has a skip card; If yes, PLAY IT 
                    if game.botdeck.get("Skip",0) >= 1:
                        print("Bot plays 'Skip'!")
                        game.botdeck["Skip"] -= 1
                        if game.botdeck["Skip"] == 0:
                            del game.botdeck["Skip"]
                        game.playerturn = "Player"
                        skipturn = True 
                        print(f"Bot ends turn") 
                        # print("Skip works")
                        break 
                        
                    # No skip card in deck --> Play an attack card if possible     
                    elif game.botdeck.get("Attack(2x)",0) >= 1: 
                        # print("Bot plays 'Attack(2x)'")
                        game.attackplayer("Player", "Attack(2x)")
                        game.playerturn = "Player"
                        # print("Attacking w/ Attack(2x) on player works")
                        break 
                    
                    # No skip or attack card in deck? --> Play favor card 
                    elif game.botdeck.get("Favor",0) >= 1: # Check if enough Favor cards
                        # print("Bot plays 'Favor'")
                        game.attackplayer("Player", "Favor")
                        game.playerturn = "Player"
                        # print("Attacking w/ Favor on player works")
                        break 
                    
                    # Cat cards --> Play if no "Skip", "Attack(2x)", or "Favor" cards available to play 
                    elif game.botdeck.get("TacoCat",0) >= 2: # Check if enough TacoCats
                        game.attackplayer("Player", "TacoCat") # Attack the player
                        game.playerturn = "Player" # After attacking, reset the player's turn to the user
                        # print("Attacking w/ TacoCat on player works")
                        break
                             
                    elif game.botdeck.get("RainbowRalphingCat",0) >= 2: # Check if enough RainbowRalphingCats
                        game.attackplayer("Player", "RainbowRalphingCat") # Attack the player
                        game.playerturn = "Player" # After attacking, reset the player's turn to the user
                        # print("Attacking w/ RainbowRalphingCat on player works")
                        break
                            
                    elif game.botdeck.get("BeardCat",0) >= 2: # Check if enough BeardCats
                        game.attackplayer("Player", "BeardCat")  # Attack the player
                        game.playerturn = "Player" # After attacking, reset the player's turn to the user
                        # print("Attacking w/ BeardCat on player works")
                        break
                    
                    # Shuffle deck to reduce chances of exploding kitten
                    # If the bot cannot steal any cards from player, it runs this
                    elif game.botdeck.get("Shuffle", 0) >= 1:
                        
                        game.shuffledeck("Bot")
                        game.botdeck["Shuffle"] -= 1
                        if game.botdeck["Shuffle"] == 0:
                            del game.botdeck["Shuffle"]
                        game.playerturn = "Player"
                        # print("Shuffle works")
                        break 

                    else: 
                        # print("\n")
                        # print("Player deck:", game.playerdeck)
                        # print("Bot deck", game.botdeck)
                        # print("\n")

                        # If the bot cannot play any more action cards, they automatically resort to drawing a card 
                        print("Bot cannot play any cards, drawing card!")

                        break  
                if skipturn == False: # If the bot did not skip their turn, they draw a card
                    game.drawacard("Bot")
                else:
                    skipturn = False # If the bot did skip their turn, reset the skipturn variable to False for the next time 
                # print(skipturn)
                         
                       
                # Cooldown for user to read terminal 
                time.sleep(3) 
                

    except Exception:
        return (f"Error Somewhere; {Exception}")
    else:
        return "Game works!"

# Initiate the game 
playgame()