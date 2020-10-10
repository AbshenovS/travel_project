import random

from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views import View

from tours import data


class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      'index.html',
                      context={'title': data.title,
                               'subtitle': data.subtitle,
                               'description': data.description,
                               'departures': data.departures,
                               'tours': dict(random.sample(data.tours.items(), 6))}
                      )


class DepartureView(View):
    def get(self, request, departure, *args, **kwargs):
        if departure not in data.departures:
            return HttpResponseNotFound(f'Пока из {departure} нет туров')

        departure_tours = dict(filter(lambda tour: tour[1]['departure'] == departure, data.tours.items()))
        min_price = min([tour['price'] for tour in departure_tours.values()])
        max_price = max([tour['price'] for tour in departure_tours.values()])
        min_nights = min([tour['nights'] for tour in departure_tours.values()])
        max_nights = max([tour['nights'] for tour in departure_tours.values()])

        return render(request,
                      'departure.html',
                      context={'title': data.title,
                               'departure': departure,
                               'departures': data.departures,
                               'city': data.departures[departure].split()[1],
                               'tours': departure_tours,
                               'min_price': min_price,
                               'max_price': max_price,
                               'min_nights': min_nights,
                               'max_nights': max_nights,
                               'tour_nums': len(departure_tours)}
                      )


class TourView(View):
    def get(self, request, id, *args, **kwargs):
        if id not in data.tours:
            return HttpResponseNotFound('Такого тура нет')

        return render(request,
                      'tour.html',
                      context={'title': data.tours[id]['title'] + ' ' + data.tours[id]['stars'] + '★',
                               'tour': data.tours[id],
                               'city': data.departures[data.tours[id]['departure']].split()[1]}
                      )
