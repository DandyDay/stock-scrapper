from django.shortcuts import render

import yfinance as yf
from datetime import date

from .models import StockCategory

today = date.today()
today = today.strftime("%Y-%m-%d")

YTD_dict_percent = {}
YTD_dict = {}
WER_dict_percent = {}
WER_dict = {}
DFH_dict = {}
DFH_dict_percent = {}


def YTD(data):
    today = data[-1]
    firstday = data['2021-01-04']
    diff = round(today-firstday, 2)
    percent = round(diff/firstday*100, 1)
    return (diff, percent)


def WeeklyEarningRate(data):
    today = data[-1]
    firstday = data[-8]
    diff = round(today-firstday, 2)
    percent = round(diff/firstday*100, 1)
    return (diff, percent)


def DeclineFromHighest(data):
    today = data['Close'][-1]
    price_max = 0
    for i in data['High'][-366:-1]:
        if price_max < i:
            price_max = i
    diff = round(today-price_max, 2)
    percent = round(diff/price_max*100, 1)
    return (diff, percent)


for category in StockCategory.objects.all():
    for stock in category.stock_set.all():
        data = yf.download(stock.stock_quote, start='2020-01-01')
        YTD_dict[stock.stock_quote], \
            YTD_dict_percent[stock.stock_quote] = YTD(data['Close'])
        WER_dict[stock.stock_quote], \
            WER_dict_percent[stock.stock_quote] = WeeklyEarningRate(data['Close'])
        DFH_dict[stock.stock_quote], \
            DFH_dict_percent[stock.stock_quote] = DeclineFromHighest(data)


def ytd(request):
    stock_category_list = StockCategory.objects.all()
    context = {'stock_category_list': stock_category_list,
               'YTD_dict_percent': YTD_dict_percent,
               'today': today}
    return render(request, 'finance/ytd.html', context)


def wer(request):
    stock_category_list = StockCategory.objects.all()
    context = {'stock_category_list': stock_category_list,
               'WER_dict_percent': WER_dict_percent,
               'today': today}
    return render(request, 'finance/wer.html', context)


def dfh(request):
    stock_category_list = StockCategory.objects.all()
    context = {'stock_category_list': stock_category_list,
               'DFH_dict_percent': DFH_dict_percent,
               'today': today}
    return render(request, 'finance/dfh.html', context)


def index(request):
    return render(request, 'finance/index.html')
