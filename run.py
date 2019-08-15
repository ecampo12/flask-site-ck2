from flask import Flask, render_template, request, jsonify, url_for
import datetime
from bs4 import BeautifulSoup
import requests


def get_game_des(site):
    # requests html from site
    source = requests.get(site).text
    soup = BeautifulSoup(source, 'html.parser')

    # finds div that holds game descriptions
    game_des = soup.find('div', id='game_area_description')
    # removes other elements in div, leaving only the game description
    game_des.h2.extract()
    game_des.find('h2', class_="bb_tag").extract()
    game_des.ul.extract()
    game_des = game_des.text

    # splits game description into lines for easy formatting
    lines = game_des.split('						 ')
    return lines

    # for x in lines:
    #     print(x)


def on_sale(site, element, checker):
    source = requests.get(site).text
    soup = BeautifulSoup(source, 'html.parser')

    try:
        sales = soup.find(element, class_=checker)
    except Exception as e:
        sales = None
    return sales



now = datetime.datetime.now()
app = Flask(__name__)

#CK2 PAGE STARTS HERE#
@app.route("/")
@app.route("/home")
def ck2_home():
    des = get_game_des('https://store.steampowered.com/app/203770/Crusader_Kings_II/')
    return render_template('/index.html', title='Home', des=des)


@app.route("/buyers_guide")
def buyers_guide():
    # table = on_sale('https://isthereanydeal.com/game/crusaderkingsii/info/',
    #                 'table', 't-st3 priceTable')
    # table = 'Test'
    return render_template('/buyers_guide.html', title="Buyer's Guide", year=now.year)


@app.route("/start_guide")
def start_guide():

    return render_template('/start_guide.html', title='Beginners Guide')


@app.route("/your_character")
def your_character():
    return render_template('/your_character.html', title='Your Character')


@app.route("/expansion")
def war():
    return render_template('/war.html', title='Expansion')


@app.route("/about")
def ck2_about():
    return render_template('/ck2_about.html', title='About')


@app.route("/background_process")
def background_process():
    lang = request.args.get('proglang')
    steam = on_sale('https://store.steampowered.com/app/203770/Crusader_Kings_II/',
                    'div', 'discount_pct')
    if steam == None:
        message = 'No Sale on Steam!'
    else:
        message = 'Sale on Steam!!'

    indiegala = on_sale(
        'https://www.indiegala.com/store/product/crusader-kings-ii/203770', 'div', 'price-discount')
    if indiegala == None:
        message = message + '''
        No sale on indiegala!!'''
    else:
        message = message + '''
        Sale on indiegala!!'''

    DLGamer = on_sale('https://www.dlgamer.com/us/games/buy-crusader-kings-2-14092',
                      'span', 'product-sheet-percent')
    if DLGamer == None:
        message = message + '''
        No sale on DlGamer!'''
    else:
        message = message + "\nSale on DLGamer!!"

    GamesPlante = on_sale(
        'https://us.gamesplanet.com/game/crusader-kings-ii-steam-key--1857-1?ref=itad', 'span', 'price_saving false')
    if GamesPlante == None:
        message = message + "No sale on GamesPlanet!!"
    else:
        message = message + "\nSale on GamesPlanet!!!"
    # table = on_sale('https://isthereanydeal.com/game/crusaderkingsii/info/',
    #                 'table', 't-st3 priceTable')
    if str(lang).lower() == 'yes':
        return jsonify(result=message)

#CK2 PAGE ENDS HERE#


if __name__ == '__main__':
    app.run(debug=True)
