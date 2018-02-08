from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):
    if request.method == 'POST':
        url = request.POST.get('url') or 'https://semantic-ui.com/images/wireframe/image.png'
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': url }],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }

        try:
                response = AT.insert(data)
                # Notify on create
                messages.success(request, "New movie added: {}.".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning("Got an error adding a movie: {}".format(e))
    return redirect('/')


def edit(request, movie_id):
    if request.method == 'POST':

        url = request.POST.get('url') or 'https://semantic-ui.com/images/wireframe/image.png'

        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': url}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }

        try:
            response = AT.update(movie_id, data)

            # Notify on Update
            messages.success(request, "New movie updated: {}.".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error when updating a movie: {}'.format(e))
    return redirect('/')

def delete(request, movie_id):
    movie_name = AT.get(movie_id)["fields"].get('Name')

    try:
        response = AT.delete(movie_id)
    except Exception as e:
        messages.warning(request, 'Got an error when deleting a movie: {}'.format(e))

    #Notify on Delete
    messages.warning(request, 'Movie has been deleted: {}.'.format(movie_name))
    return redirect('/')
