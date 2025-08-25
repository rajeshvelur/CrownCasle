import requests
import json
import time

# Function to calculate the hand value in blackjack style, with Ace as 1 or 11
# the cards value passed here is of this format ['4D', 'AH', 'AC']
def hand_total(cards):
    total = 0
    aces = 0

    # Step 1: Add up the cards
    for card in cards:
        value = card[:-1]   # everything except the suit

        if value in ['J', 'Q', 'K']:
            total = total + 10
        elif value == 'A':
            total = total + 11   # count Ace as 11 for now
            aces = aces + 1
        else:
            total = total + int(value)

    # Step 2: Adjust Aces if total is too high
    while total > 21 and aces > 0:
        total = total - 10   # turn one Ace from 11 into 1
        aces = aces - 1

    return total


# check if the site is up and running - by checking its status code = 200
response = requests.get("https://deckofcardsapi.com/")
if response.status_code != 200:
    raise Exception("Site may not be up; HTTP status code: " + str(response.status_code))
print("Site is up.")

# Step 3: Get a new deck
response = requests.get("https://deckofcardsapi.com/api/deck/new/")
response.raise_for_status()  # Raise an exception for bad status codes
deck = response.json()
deck_id = deck['deck_id']
print(f"New deck created with ID: {deck_id}")

# Step 4: Shuffle the deck use the deck_id we got from the above new deck creation
response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/shuffle/")
response.raise_for_status()
shuffle = response.json()
print(shuffle)
if not shuffle['success']:
    raise Exception("Deck shuffle failed.")
print("Deck shuffled.")


# Step 5: Deal three cards to each of two players
# Player 1 - Draws 3 cards
response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=3")
response.raise_for_status()
print(response)
player1_cards = response.json()['cards']
# print("Player 1 cards:", [card['code'] for card in player1_cards])
player1_codes = []
for card in player1_cards:
    player1_codes.append(card['code'])

print(player1_codes)

# Player 2 - Draws 3 cards
response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=3")
response.raise_for_status()
print(response.json())
player2_cards = response.json()['cards']
# print("Player 2 cards:", [card['code'] for card in player2_cards])
player2_codes = []
for card in player2_cards:
    player2_codes.append(card['code'])

print(player2_codes)


# get the total of all te cards each player has drawn
player1_value = hand_total(player1_codes)
player2_value = hand_total(player2_codes)

print(f"Player 1 value is --> {player1_value}", f"Player 2 value is --> {player2_value}")

# Decide winner
if player1_value > 21:
    print("Player 1 busts. Player 2 wins.")
elif player2_value > 21:
    print("Player 2 busts. Player 1 wins!")
elif player1_value > player2_value:
    print("Player 1 wins!")
elif player1_value < player2_value:
    print("Player 2 wins!")
else:
    print("It's a tie (Push).")