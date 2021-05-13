from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import keyboard

game_choices = ["PowerBall", "Mega Millions", "MegaBucks", "Lotto America", "Lucky for Life", "Gimme 5"]
win_probs = [1/24.9, 1/24, 1/5.9, 1/9.6, 1/7.769, 1/9]
num_tickets = [0, 0, 0, 0, 0, 0]
ticket_cost = [2, 2, 2, 1, 2, 1]
ticket_value = [0, 0, 0, 0, 0, 0]
prob_win = 0
no_win = 0
yes_win = 0
total_cost = 0
life_second = 0
life_jack = 0

pow_URL = 'https://www.mainelottery.com/games/powerball.shtml'
mil_URL = 'https://www.mainelottery.com/games/megamillions.shtml'
bucks_URL = 'https://www.mainelottery.com/games/megabucksplus.shtml'
lotto_URL = 'https://www.mainelottery.com/games/lotto-america.shtml'
pow_page = requests.get(pow_URL)
mil_page = requests.get(mil_URL)
bucks_page = requests.get(bucks_URL)
lotto_page = requests.get(lotto_URL)

#function to find jackpot for the four jackpot-variable games
def find_jack(game_page):
    soup = BeautifulSoup(game_page.content, 'html.parser')
    results = soup.find(id='maincontent2')
    res = results.find_all('div', class_='windrawnums')
    for seg in res:
        cash = seg.find_all('span', string=lambda text: '$' in text.lower())
        if None in cash:
            continue
    list = [str(i) for i in str(cash) if i.isdigit()]
    jack = int("".join(list))
    return jack

def next():
    try:
        input("Press enter to continue")
    except SyntaxError:
        pass

mil_jack = find_jack(mil_page)
print('Mega Millions Jackpot is $', mil_jack)
pow_jack = find_jack(pow_page)
print('Powerball Jackpot is $', pow_jack)
bucks_jack = find_jack(bucks_page)
print('Megabucks Jackpot is $', bucks_jack)
lotto_jack = find_jack(lotto_page)
print('Lotto America Jackpot is $', lotto_jack)

next()
    #print(i, end='\n'*2)

print("Type in corresponding numbers for each game played. Then press enter:")
for i in range(len(game_choices)):
    print(i+1, ": ", game_choices[i])
game_indicator = input()

for i in range(len(game_choices)+1):
    if str(i) in game_indicator:
        print("Enter Number of ", game_choices[i-1], "Tickets Purchased: ")
        num_tickets[i-1] = int(input())
        no_win = (1-win_probs[i-1])**(num_tickets[i-1])
        yes_win = 1 - no_win
        if i == 5:
            print("You are playing Lucky for Life. Please type in your age and then press enter.")
            age = int(input())
            years_left = max(80-age,5)
            life_jack = years_left*365250
            life_second = years_left*25000
    prob_win = prob_win * no_win + yes_win
    total_cost = total_cost + ticket_cost[i-1]*num_tickets[i-1]
print("Probability of Winning on at least one ticket: ", round(prob_win*100, 2), "%")
next()
print("Total Spent: $", total_cost)
next()
#jackpots = [pow_jack, mil_jack, bucks_jack, lotto_jack, life_jack, 100000]
#jackpot_odds = [1/292201338, 1/302575350, 1/4496388, 1/25989600, 1/30821472, 1/575757]
odds = [
        [1/38,1/92,1/701,1/580,1/14494,1/36525,1/913129,1/11688054,1/292201338],
        [1/37,1/89,1/693,1/606,1/14547,1/38792,1/931001,1/12607306,1/302575350],
        [1/15.3,1/12.6,1/63,1/142.7,1/713.7,1/4996,1/24979.9,1/899277.6,1/4496388],
        [1/17,1/29,1/160,1/267,1/2404,1/12288,1/110594,1/2887733,1/25989600],
        [1/32,1/50,1/15,1/250,1/201,1/3413,1/8433,1/143356,1/1813028,1/30821472],
        [1/10,1/103,1/3387,1/575757]
        ]
prizes = [
          [4,4,7,7,100,100,50000,1000000,pow_jack],
          [2,4,10,10,200,500,10000,1000000,mil_jack],
          [2,2,5,7,25,150,1300,30000,bucks_jack],
          [2,2,5,5,20,100,1000,20000,lotto_jack],
          [4,6,3,25,20,150,200,5000,life_second,life_jack],
          [2,7,250,100000]
          ]
mult_prizes = []
mult_odds = []
mults = []

#generates actual value of each played game ticket,
def find_ticket_value(num_tickets):
    for i in range(len(num_tickets)):
        if num_tickets[i] > 0:
            game_odds = odds[i]
            game_prizes = prizes[i]
            indiv_value = sum(game_odds[j]*game_prizes[j] for j in range(len(game_odds)))
            ticket_value[i] = num_tickets[i]*indiv_value
    return ticket_value

find_ticket_value(num_tickets)
total_value = round(sum(ticket_value),2)
print("Your tickets have a total value of $", total_value)
next()
if total_value > total_cost:
    print("You are expected to gain $",round(total_value-total_cost,2), ". Due to a large jackpot, it is unlikely you will actually profit this amount.")
else:
    print("You are expected to lose $",round(total_cost-total_value,2), ". Did you know that if you make this purchase weekly, you're expected to be down at least $",round(52*(total_cost-total_value),2),"in just one year?")
#num_mega = input("Enter Number of Mega Millions Tickets Purchased: ")
#num_mega = int(num_mega)
#num_pow = input("Enter Number of PowerBall Tickets Purchased: ")
#num_pow = int(num_pow)

#prob_mega_win = 1 - (1 - yes_mega)**num_mega
#prob_pow_win = 1 - (1 - yes_pow)**num_pow
#print("Prob of Winning: ", prob_mega_win*100, "%")

#num_tickets = 1

# determine num_tickets needed to win something
#prob_win = 0
#while (prob_win < 0.99999):
#    yes = 1/24
#    prob_win = 1 - (1-yes)**num_mega
#    num_mega = num_mega + 1

#print("Prob of Winning: ", prob_win*100, "%")
#print("Num of Tickets:", num_mega-1)
