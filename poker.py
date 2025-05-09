import random

# Kartenwerte und Farben
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {rank: i for i, rank in enumerate(RANKS, start=2)}

# Funktion zum Erstellen eines Decks
def create_deck():
    return [{'rank': rank, 'suit': suit} for suit in SUITS for rank in RANKS]

# Funktion zum Mischen des Decks
def shuffle_deck(deck):
    random.shuffle(deck)

# Funktion zum Bewerten der Hand
def evaluate_hand(hand):
    ranks = sorted([card['rank'] for card in hand], key=lambda x: RANK_VALUES[x])
    suits = [card['suit'] for card in hand]
    rank_counts = {rank: ranks.count(rank) for rank in ranks}

    # Prüfen auf Flush
    is_flush = len(set(suits)) == 1

    # Prüfen auf Straight
    is_straight = all(RANK_VALUES[ranks[i]] + 1 == RANK_VALUES[ranks[i + 1]] for i in range(len(ranks) - 1))

    # Prüfen auf andere Kombinationen
    if is_flush and is_straight:
        return "Straight Flush"
    elif 4 in rank_counts.values():
        return "Four of a Kind"
    elif sorted(rank_counts.values()) == [2, 3]:
        return "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight:
        return "Straight"
    elif 3 in rank_counts.values():
        return "Three of a Kind"
    elif list(rank_counts.values()).count(2) == 2:
        return "Two Pair"
    elif 2 in rank_counts.values():
        return "One Pair"
    else:
        return "High Card"

# Funktion zum Anzeigen der Hand
def display_hand(hand):
    return " ".join([f"{card['rank']}{card['suit']}" for card in hand])

# Hauptspiel-Funktion
def play_poker():
    print("Willkommen bei 5-Card-Draw Poker!")
    
    # Anzahl der Spieler festlegen
    num_players = int(input("Gib die Anzahl der Spieler ein (2-4): "))
    while num_players < 2 or num_players > 4:
        num_players = int(input("Ungültige Anzahl! Gib eine Zahl zwischen 2 und 4 ein: "))

    # Deck erstellen und mischen
    deck = create_deck()
    shuffle_deck(deck)

    # Karten austeilen
    players_hands = {f"Spieler {i+1}": [deck.pop() for _ in range(5)] for i in range(num_players)}

    # Hände anzeigen
    print("\n--- Erste Runde ---")
    for player, hand in players_hands.items():
        print(f"{player}: {display_hand(hand)}")

    # Spieler können Karten tauschen
    for player, hand in players_hands.items():
        print(f"\n{player}, deine aktuelle Hand: {display_hand(hand)}")
        discard_indices = input("Gib die Indizes der Karten ein, die du tauschen möchtest (0-4, getrennt durch Leerzeichen). Drücke Enter, um keine zu tauschen: ")
        
        if discard_indices.strip():
            discard_indices = [int(i) for i in discard_indices.split()]
            for index in discard_indices:
                hand[index] = deck.pop()

        print(f"Neue Hand von {player}: {display_hand(hand)}")

    # Hände bewerten und Gewinner ermitteln
    print("\n--- Ergebnisse ---")
    scores = {}
    for player, hand in players_hands.items():
        hand_rank = evaluate_hand(hand)
        scores[player] = (hand_rank, max(RANK_VALUES[card['rank']] for card in hand))
        print(f"{player}: {display_hand(hand)} -> {hand_rank}")

    # Gewinner bestimmen
    winner = max(scores.items(), key=lambda x: (x[1][0], x[1][1]))
    print(f"\nDer Gewinner ist {winner[0]} mit einer Hand: {winner[1][0]}!")

# Spiel starten
if __name__ == "__main__":
    play_poker()
