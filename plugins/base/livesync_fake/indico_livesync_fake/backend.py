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

from wtforms.fields.html5 import URLField
from wtforms.validators import URL, DataRequired

from indico_livesync import AgentForm, LiveSyncBackendBase, MARCXMLUploader
from indico_livesync_fake import _
from indico_livesync_fake.connector import FakeConnector


class FakeAgentForm(AgentForm):
    server_url = URLField(_('URL'), [DataRequired(), URL(require_tld=False)],
                          description=_("The URL of the Fake instance"))


class FakeUploaderError(Exception):
    pass


class FakeUploader(MARCXMLUploader):
    def __init__(self, *args, **kwargs):
        super(FakeUploader, self).__init__(*args, **kwargs)
        url = self.backend.agent.settings.get('server_url')
        self.connector = FakeConnector(url)

    def upload_xml(self, xml):

        ### BEGIN TEST ###
        import commands
        commands.getoutput('touch /tmp/upload_xml')
        ### END TEST ###

        result = self.connector.upload_marcxml(xml, '-ir').read()
        if not isinstance(result, long) and not result.startswith('[INFO]'):
            raise FakeUploaderError(result.strip())


class FakeLiveSyncBackend(LiveSyncBackendBase):
    """Fake

    This backend uploads data to Fake.
    """
    ### BEGIN TEST ###
    import commands
    commands.getoutput('touch /tmp/fakelivesynchbackend')
    ### END TEST ###

    uploader = FakeUploader
    form = FakeAgentForm
