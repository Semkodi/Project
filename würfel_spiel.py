import random

print(' Willkommen zum Würfel- Duell! Du gegen den Computer.')

weitermachen = True

while weitermachen:
    spieler_wurf = random.randint(1,6)
    print(f'Du hast eine {spieler_wurf} gewürfelt')

    computer_wurf = random.randint(1,6)
    print(f'Der Computer hat eine {computer_wurf} gewürfelt. ')

    if spieler_wurf > computer_wurf:
        print('Du hast gewonnen ')
    elif spieler_wurf < computer_wurf:
        print('Der Computer hat gewonnen.')
    else:
        print('Unentschieden!')

    anwort = input('Nochmal würfeln (ja / nein):').strip().lower()
    if anwort != 'ja':
        weitermachen = False

print('Danke fürs Spielen:')

