import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import urllib
from webhelpers.html import literal
from ckan.common import _
from ckanext.extensionstheme.update import _update_Readme
try:
    from ckan.common import config
except ImportError:
    from pylons import config


_VALID_GRAVATAR_DEFAULTS = ['404', 'mm', 'identicon', 'monsterid',
                            'wavatar', 'retro']

def recent_datasets(num=4):
    """Return a list of recent datasets."""
    sorted_datasets = []
    datasets = toolkit.get_action('current_package_list_with_resources')({},{'limit': num})
    if datasets:
        sorted_datasets = sorted(datasets, key=lambda k: k['metadata_modified'], reverse=True)
    return sorted_datasets[:num]


def popular_datasets(num=4):
    """Return a list of popular datasets."""
    datasets = []
    search = toolkit.get_action('package_search')({},{'rows': num, 'sort': 'views_recent desc'})
    if search.get('results'):
        datasets = search.get('results')
    return datasets[:num]


def dataset_count():
    """Return a count of all datasets"""
    count = 0
    result = toolkit.get_action('package_search')({}, {'rows': 1})
    if result.get('count'):
        count = result.get('count')
    return count


def groups(num=12):
    """Return a list of groups"""
    groups = toolkit.get_action('group_list')({}, {'all_fields': True, 'sort': 'packages'})
    return groups[:num]


def showcases(num=24):
    """Return a list of showcases"""
    sorted_showcases = []
    try:
        showcases = toolkit.get_action('ckanext_showcase_list')({},{})
        sorted_showcases = sorted(showcases, key=lambda k: k.get('metadata_modified'), reverse=True)
    except:
        print "[ckanext-extensionstheme] Error in retrieving list of showcases"
    return sorted_showcases[:num]


def get_package_metadata(package):
    """Return the metadata of a dataset"""
    result = {}
    try:
        result = toolkit.get_action('package_show')(None, {'id': package.get('name'), 'include_tracking': True})
    except:
        print "[ckanext-extensionstheme] Error in retrieving dataset metadata for " + str(package)
    return result


def accessibile_gravatar(email_hash, size=100, default=None):
    if default is None:
        default = config.get('ckan.gravatar_default', 'identicon')

    if default not in _VALID_GRAVATAR_DEFAULTS:
        # treat the default as a url
        default = urllib.quote(default, safe='')

    return literal('''<img src="//gravatar.com/avatar/%s?s=%d&amp;d=%s"
        class="gravatar" width="%s" height="%s" alt="your avatar" />'''
                   % (email_hash, size, default, size, size)
                   )

def accessibile_linked_gravatar(email_hash, size=100, default=None):
    return literal(
        '<a href="https://gravatar.com/" target="_blank" ' +
        'title="%s" alt="avatar">' % _('Update your avatar at gravatar.com') +
        '%s</a>' % accessibile_gravatar(email_hash, size, default)
    )

def get_group_alias():
    return str(config.get('ckan.group_alias', 'Group'))

def get_organization_alias():
    return str(config.get('ckan.organization_alias', 'Organization'))


def get_plus_icon():
    if toolkit.check_ckan_version(min_version='2.7'):
        return 'plus-square'
    return 'plus-sign-alt'


def get_logo(pkg):
    resource = pkg['resources']
    url =''
    for res in resource:
        if res['format'].upper() == 'PNG'\
        or res['format'].upper() == 'JPG'\
        or res['format'].upper() == 'JPEG':
            url = res['url']
    return url


class ExtensionsThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'extensionstheme')

    # ITemplateHelpers

    def get_helpers(self):
        """Register extensionstheme_* helper functions"""

        return {'extensionstheme_recent_datasets': recent_datasets,
                'extensionstheme_popular_datasets': popular_datasets,
                'extensionstheme_dataset_count': dataset_count,
                'extensionstheme_get_groups': groups,
                'extensionstheme_get_showcases': showcases,
                'extensionstheme_get_package_metadata': get_package_metadata,
                'extensionstheme_gravatar': accessibile_gravatar,
                'extensionstheme_linked_gravatar': accessibile_linked_gravatar,
                'extensionstheme_group_alias': get_group_alias,
                'extensionstheme_organization_alias': get_organization_alias,
                'extensionstheme_get_plus_icon': get_plus_icon,
                'extensionstheme_getLOGO': get_logo,
                'extensionstheme_update_Readme': _update_Readme,
               }
