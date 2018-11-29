# This file is part of Indico.
# Copyright (C) 2002 - 2018 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from wtforms.fields.core import SelectField
from wtforms.fields.html5 import IntegerField, URLField
from wtforms.validators import URL, NumberRange

from indico.core.plugins import IndicoPluginBlueprint
from indico.web.forms.base import IndicoForm

from indico_search import SearchPluginBase
from indico_search.views import WPSearchCategory, WPSearchConference
from indico_search_fake import _
from indico_search_fake.engine import FakeSearchEngine
from indico_search_fake.forms import FakeSearchForm


class SettingsForm(IndicoForm):
    search_url = URLField(_('Fake URL'), [URL()])
    display_mode = SelectField(_('Display mode'), choices=[('api_public', _('Embedded (public data)')),
                                                           ('api_private', _('Embedded (private data)')),
                                                           ('redirect', _('External (Redirect)'))])
    results_per_page = IntegerField(_('Results per page'), [NumberRange(min=5)],
                                    description=_("Number of results to show per page (only in embedded mode)"))


class FakeSearchPlugin(SearchPluginBase):
    """Fake Search

    Uses Fake as Indico's search engine
    """
    configurable = True
    settings_form = SettingsForm
    default_settings = {
        'search_url': None,
        'display_mode': 'redirect',
        'results_per_page': 20
    }
    engine_class = FakeSearchEngine
    search_form = FakeSearchForm

    def init(self):
        super(FakeSearchPlugin, self).init()
        for wp in (WPSearchCategory, WPSearchConference):
            self.inject_bundle('main.js', wp)
            self.inject_bundle('main.css', wp)

	### BEGIN TEST ###
	import commands
	commands.getoutput('touch /tmp/FakeSearchPlugin.init')
	### END TEST ###

    def get_blueprints(self):
        return IndicoPluginBlueprint('search_fake', 'indico_search_fake')
