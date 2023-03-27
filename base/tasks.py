from __future__ import absolute_import, unicode_literals
from celery import task
from pymarketcap import Pymarketcap
from crypto_news_api import CryptoControlAPI
from django.template.loader import get_template
from django.core.mail import EmailMessage
from .models import CoinDetails, User, ExtendSignup, NewsDetails
from .crypto_news import *
import datetime


@task()
def update_crypto_coins_data():
    """
    update_crypto_coins_data: Update coins data to the database.
    """
    # Delete all previous data first to enter updated data
    CoinDetails.objects.all().delete()
    # Call get_coin_data function to get updated coins data
    filtered_coin_data = get_coin_data()

    for data in list(filtered_coin_data.values()):
        insert_object = CoinDetails()
        insert_object.name = data['name']
        insert_object.symbol = data['symbol']
        insert_object.price = data['price']
        insert_object.percent_change_1h = data['percent_change_1h']
        insert_object.percent_change_24h = data['percent_change_24h']
        insert_object.percent_change_7d = data['percent_change_7d']
        insert_object.volume_24h = data['volume_24h']
        insert_object.market_cap = data['market_cap']
        insert_object.save()


@task()
def send_email_update():
    """
    send_email_update: Send email update to the user on the basis of their coin preferences.
    """
    extend_signup_object = ExtendSignup.objects.all()
    for db_object in extend_signup_object:
        # Check whether coin_choices field is empty
        if db_object.coin_choices is not None:
            user_object = User.objects.get(id=db_object.user_id)

            username = user_object.username
            user_email = user_object.email.split()
            date_today = datetime.date.today().strftime("%d/%m/%Y")

            coin_choices_list = db_object.coin_choices.split(',')
            coin_details = list(CoinDetails.objects.filter(symbol__in=coin_choices_list))

            context = {
                'coin_details': coin_details,
                'date_today': date_today,
                'username': username,
            }

            subject = "Your coin updates"
            to = user_email
            from_email = 'ditmail612@gmail.com'

            message = get_template('templated_email/coin_update.html').render(context)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()


@task()
def news_update():
    """
    news_update: Update news for homepage
    """
    # Delete previous data to enter updated data
    NewsDetails.objects.all().delete()

    api = CryptoControlAPI(API_KEY)
    proxy_api = CryptoControlAPI(API_KEY, proxyURL)

    latest_news = api.getLatestNews()[:9]

    for data in latest_news:
        insert_object = NewsDetails()
        insert_object.url = data['url']
        insert_object.title = data['title']
        insert_object.description = data['description']
        insert_object.image_url = data['originalImageUrl']
        insert_object.published_at = data['publishedAt']
        insert_object.source_domain = data['sourceDomain']
        insert_object.save()


def get_coin_data():
    """
    get_coin_data : Get coin data by using CoinMarketCap API and filter those data
    :return filtered_coin_data_dict: dictionary
    """
    # CoinMarketCap object
    cmc_object = Pymarketcap(timeout=10)
    coin_data = cmc_object.ticker()['data']
    coin_data_list = list(coin_data.values())
    # Declare filtered_coin_data_dict dictionary variable
    filtered_coin_data_dict = dict()

    for data in coin_data_list:
        test_dict = dict()
        test_dict['name'] = data['name']
        test_dict['symbol'] = data['symbol']
        for quotes_data in data['quotes'].values():
            test_dict['price'] = quotes_data['price']
            test_dict['percent_change_1h'] = quotes_data['percent_change_1h']
            test_dict['percent_change_24h'] = quotes_data['percent_change_24h']
            test_dict['percent_change_7d'] = quotes_data['percent_change_7d']
            test_dict['volume_24h'] = quotes_data['volume_24h']
            test_dict['market_cap'] = quotes_data['market_cap']

        filtered_coin_data_dict.setdefault(data['symbol'], test_dict)

    return filtered_coin_data_dict
