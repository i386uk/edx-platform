"""
Credentials Configuration
"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType, PluginURLs, PluginSettings


class CredentialsConfig(AppConfig):
    """
    Configuration class for credentials Django app
    """
    name = 'openedx.core.djangoapps.credentials'
    verbose_name = _("Credentials")

    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: u'credentials',
                PluginURLs.REGEX: u'api/credentials/',
                PluginURLs.RELATIVE_PATH: u'urls',
            }
        },
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.AWS: {PluginSettings.RELATIVE_PATH: u'settings.aws'},
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: u'settings.common'},
            }
        }
    }

    def ready(self):
        # Register the signals handled by bookmarks.
        from . import signals
