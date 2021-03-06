# This file is part of the CERN Indico plugins.
# Copyright (C) 2014 - 2019 CERN
#
# The CERN Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from __future__ import unicode_literals

from wtforms.fields.core import SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import URL

from indico.core.plugins import IndicoPluginBlueprint
from indico.web.forms.base import IndicoForm

from indico_search import SearchPluginBase
from indico_search_json import _
from indico_search_json.engine import JSONSearchEngine


class SettingsForm(IndicoForm):
    search_url = URLField(_('CERNsearch URL'), [URL()])
    display_mode = SelectField(_('Display mode'), choices=[('iframe', _('Embedded (IFrame)')),
                                                           ('redirect', _('External (Redirect)'))])


class JSONSearchPlugin(SearchPluginBase):
    """JSON Search

    Uses JSONSearch as Indico's search engine
    """
    configurable = True
    settings_form = SettingsForm
    default_settings = {
        'search_url': 'https://search.cern.ch/Pages/IndicoFrame.aspx',
        'display_mode': 'iframe'
    }
    engine_class = JSONSearchEngine

    def get_blueprints(self):
        return IndicoPluginBlueprint('search_json', 'indico_search_json')
