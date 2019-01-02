# -*- coding: utf-8 -*-
import json
import csv
import time
from justwatch import JustWatch


def get_tmdb_id(movie):
	for score in movie['scoring']:
		if score['provider_type'] == 'tmdb:id':
			return score['value']


def get_provider_by_id(provider_id, providers):
	for provider in providers:
		if provider['id'] == provider_id:
			return provider

	return None


def get_offers(movie, country, provider_details, monetization_types):
	offers = []
	if 'offers' not in movie:
		return offers

	for offer in movie['offers']:
		if len(monetization_types) > 0 and offer['monetization_type'] not in monetization_types:
			continue

		if offer['country'] == country:
			provider = get_provider_by_id(offer['provider_id'], provider_details)
			if provider:
				offers.append(provider['slug'])

	return list(set(offers))


def get_movie(title, country, content_types=['movie'], monetization_types=['flatrate']):
	just_watch = JustWatch(country=country)

	provider_details = just_watch.get_providers()

	results = just_watch.search_for_item(query=title, content_types=content_types)
	if len(results['items']) == 0:
		return

	first_movie = results['items'][0]

	return {
		'title': first_movie['title'],
		'id': get_tmdb_id(first_movie),
		'offers': get_offers(first_movie, country, provider_details, monetization_types)
	}
