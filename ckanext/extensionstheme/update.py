import csv, json
import os
import urllib, urllib2
import pypandoc
import datetime
from collections import OrderedDict

import ckan.model as model
from ckan.plugins import toolkit as tk

c = tk.c
check_access = tk.check_access
get_action = tk.get_action
abort = tk.abort
NotFound = tk.ObjectNotFound
NotAuthorized = tk.NotAuthorized


def getContext():
    context = {
        'model': model,
        'session': model.Session,
        'user': c.user or c.author,
        'auth_user_obj': c.userobj
    }
    return context


def _setDatasetDict(dataset_id, mdNotes):
    dataset_dict = {
        "id": dataset_id,
        "notes": mdNotes
    }
    return dataset_dict


def isOutDate(lastUpdate):
    if datetime.datetime.now() - lastUpdate > datetime.timedelta(days = 7):
        return True
    else:
        return False


def _update_Readme(dataset_id):
    context = getContext()
    Tformat = "%Y-%m-%dT%H:%M:%S.%f"
    msg = ""
    try:
        dataset = get_action('package_show')(context, {"id": dataset_id})
    except NotFound:
        abort(404, _('Package not found'))
    except NotAuthorized:
        abort(401, _('Unauthorized to read package'))

    if isOutDate(datetime.datetime.strptime(dataset['metadata_modified'],Tformat)):
        # patch package with readme description
        link = dataset['url']
        readme = _get_readme(link)
        dataset_dict = _setDatasetDict(dataset_id, readme)
        try:
            res = get_action('package_patch')(context, dataset_dict)
        except NotFound:
            abort(404, _('Package not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to edit package'))
        msg = "Last Update: " + unicode(datetime.datetime.now())
    else:
        msg = "Last Update: " + dataset['metadata_modified']
    return msg


def _get_readme(link):
    exts = [ '.md', '.markdown', '.rst', '' ]
    urlbase = link.replace('github.com', 'raw.githubusercontent.com')
    for ext in exts:
        url = urlbase + '/master/README' + ext
        urlfo = urllib.urlopen(url)
        if urlfo.getcode() == 404:
            # try lowercase readme
            url = urlbase + 'readme' + ext
            urlfo = urllib.urlopen(url)
        if urlfo.getcode() == 200:
            readme = urlfo.read()
            # {% is reserved for liquid templates
            readme = readme.replace('{% ', '{%raw%}{% {%endraw%}')
            readme = readme.replace(' %}', '{%raw%} %}{%endraw%}')
            if ext == '.rst':
                readme = pypandoc.convert_text(readme, to='markdown_github', format = 'rst' )
            else:
                readme = pypandoc.convert_text(readme, to='markdown_github', format = 'markdown_github' )
            return readme
