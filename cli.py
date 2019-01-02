import click
from movie import get_movie


@click.command()
@click.option('--title', prompt='Title', help='Title of the film')
@click.option('--country', default='ES', help='Country code.')
def cli(title, country):
	movie = get_movie(title, country, content_types=['movie'], monetization_types=['flatrate'])
	if len(movie['offers']) == 0:
		print("No subscription offers")
		return
	else:
		print("Subscription offers:")

	for offer in movie['offers']:
		print("  * {}".format(offer))


if __name__ == '__main__':
    cli()
