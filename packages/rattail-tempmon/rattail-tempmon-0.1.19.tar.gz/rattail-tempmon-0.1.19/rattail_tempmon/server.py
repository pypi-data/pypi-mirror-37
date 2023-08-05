# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2018 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Tempmon server daemon
"""

from __future__ import unicode_literals, absolute_import

import time
import datetime
import logging

import six
import humanize
from sqlalchemy import orm
from sqlalchemy.exc import OperationalError

from rattail.db import Session, api
from rattail_tempmon.db import Session as TempmonSession, model as tempmon
from rattail.daemon import Daemon
from rattail.time import localtime, make_utc
from rattail.mail import send_email


log = logging.getLogger(__name__)


class TempmonServerDaemon(Daemon):
    """
    Linux daemon implementation of tempmon server.
    """
    timefmt = '%Y-%m-%d %H:%M:%S'

    def run(self):
        """
        Keeps an eye on tempmon readings and sends alerts as needed.
        """
        self.extra_emails = self.config.getlist('rattail.tempmon', 'extra_emails', default=[])
        delay = self.config.getint('rattail.tempmon', 'server.delay', default=60)
        self.failed_checks = 0

        while True:
            self.check_readings()
            time.sleep(delay)

    def check_readings(self):

        # log.debug("checking readings")
        self.now = make_utc()
        session = TempmonSession()

        try:
            clients = session.query(tempmon.Client)\
                             .filter(tempmon.Client.enabled == True)\
                             .filter(tempmon.Client.archived == False)
            for client in clients:
                self.check_readings_for_client(session, client)
            session.flush()

        except Exception as error:
            log_error = True
            self.failed_checks += 1
            session.rollback()

            # our goal here is to suppress logging when we see connection
            # errors which are due to a simple postgres restart.  but if they
            # keep coming then we'll go ahead and log them (sending email)
            if isinstance(error, OperationalError):

                # this first test works upon first DB restart, as well as the
                # first time after DB stop.  but in the case of DB stop,
                # subsequent errors will instead match the second test
                if error.connection_invalidated or (
                        'could not connect to server: Connection refused' in six.text_type(error)):

                    # only suppress logging for 3 failures, after that we let them go
                    # TODO: should make the max attempts configurable
                    if self.failed_checks < 4:
                        log_error = False
                        log.debug("database connection failure #%s: %s",
                                  self.failed_checks,
                                  six.text_type(error))

            # send error email unless we're suppressing it for now
            if log_error:
                log.exception("Failed to check client probe readings (but will keep trying)")

        else: # checks were successful
            self.failed_checks = 0
            session.commit()

        finally:
            session.close()

    def check_readings_for_client(self, session, client):
        """
        Check readings for all (enabled) probes for the given client.
        """
        # cutoff is calculated as the client delay (i.e. how often it takes
        # readings) plus one minute.  we "should" have a reading for each probe
        # within that time window.  if no readings are found we will consider
        # the client to be (possibly) offline.
        delay = client.delay or 60
        cutoff = self.now - datetime.timedelta(seconds=delay + 60)
        online = False
        for probe in client.enabled_probes():
            if self.check_readings_for_probe(session, probe, cutoff) and not online:
                online = True

        # if client was previously marked online, but we have no "new"
        # readings, then let's look closer to see if it's been long enough to
        # mark it offline
        if client.online and not online:

            # we consider client offline if it has failed to take readings for
            # 3 times in a row.  allow a one minute buffer for good measure.
            cutoff = self.now - datetime.timedelta(seconds=(delay * 3) + 60)
            reading = session.query(tempmon.Reading)\
                             .filter(tempmon.Reading.client == client)\
                             .filter(tempmon.Reading.taken >= cutoff)\
                             .first()
            if not reading:
                log.info("marking client as OFFLINE: {}".format(client))
                client.online = False
                send_email(self.config, 'tempmon_client_offline', {
                    'client': client,
                    'now': localtime(self.config, self.now, from_utc=True),
                })


    def check_readings_for_probe(self, session, probe, cutoff):
        """
        Check readings for the given probe, within the time window defined by
        the given cutoff.
        """
        # we really only care about the latest reading
        reading = session.query(tempmon.Reading)\
                         .filter(tempmon.Reading.probe == probe)\
                         .filter(tempmon.Reading.taken >= cutoff)\
                         .order_by(tempmon.Reading.taken.desc())\
                         .first()
        if reading:

            # is reading below critical min, or above critical max?
            if (reading.degrees_f <= probe.critical_temp_min or
                  reading.degrees_f >= probe.critical_temp_max):
                self.update_status(probe, self.enum.TEMPMON_PROBE_STATUS_CRITICAL_TEMP, reading)

            # is reading below "good" min?
            elif reading.degrees_f < probe.good_temp_min:
                self.update_status(probe, self.enum.TEMPMON_PROBE_STATUS_LOW_TEMP, reading)

            # is reading above "good" max?
            elif reading.degrees_f > probe.good_temp_max:
                self.update_status(probe, self.enum.TEMPMON_PROBE_STATUS_HIGH_TEMP, reading)

            else: # temp is good
                self.update_status(probe, self.enum.TEMPMON_PROBE_STATUS_GOOD_TEMP, reading)

            return True

        else: # no current readings for probe
            self.update_status(probe, self.enum.TEMPMON_PROBE_STATUS_ERROR)
            return False

    def update_status(self, probe, status, reading=None):
        data = {
            'probe': probe,
            'status': self.enum.TEMPMON_PROBE_STATUS[status],
            'reading': reading,
            'taken': localtime(self.config, reading.taken, from_utc=True) if reading else None,
            'now': localtime(self.config, self.now, from_utc=True),
        }

        prev_status = probe.status
        prev_alert_sent = probe.status_alert_sent
        if probe.status != status:
            probe.status = status
            probe.status_changed = self.now
            probe.status_alert_sent = None

            # send email when things go back to normal, after being bad
            if status == self.enum.TEMPMON_PROBE_STATUS_GOOD_TEMP and prev_alert_sent:
                send_email(self.config, 'tempmon_good_temp', data)
                probe.status_alert_sent = self.now

        # no (more) email if status is good
        if status == self.enum.TEMPMON_PROBE_STATUS_GOOD_TEMP:
            return

        # no email if we already sent one...until timeout is reached
        if probe.status_alert_sent:
            timeout = datetime.timedelta(minutes=probe.status_alert_timeout)
            if (self.now - probe.status_alert_sent) <= timeout:
                return

        # delay even the first email, until configured threshold is reached
        # unless we have a critical status
        if status != self.enum.TEMPMON_PROBE_STATUS_CRITICAL_TEMP:
            timeout = datetime.timedelta(minutes=probe.therm_status_timeout)
            if (self.now - probe.status_changed) <= timeout:
                return

        # determine URL for probe, if possible
        url = self.config.get('tailbone', 'url.tempmon.probe', default='#')
        data['probe_url'] = url.format(uuid=probe.uuid)

        since = localtime(self.config, probe.status_changed, from_utc=True)
        data['status_since'] = since.strftime('%I:%M %p')
        data['status_since_delta'] = humanize.naturaltime(self.now - probe.status_changed)

        # fetch last 90 minutes of readings
        session = orm.object_session(probe)
        recent_minutes = 90     # TODO: make configurable
        cutoff = self.now - datetime.timedelta(seconds=(60 * recent_minutes))
        readings = session.query(tempmon.Reading)\
                          .filter(tempmon.Reading.probe == probe)\
                          .filter(tempmon.Reading.taken >= cutoff)\
                          .order_by(tempmon.Reading.taken.desc())
        data['recent_minutes'] = recent_minutes
        data['recent_readings'] = readings
        data['pretty_time'] = lambda dt: localtime(self.config, dt, from_utc=True).strftime('%Y-%m-%d %I:%M %p')

        msgtypes = {
            self.enum.TEMPMON_PROBE_STATUS_LOW_TEMP             : 'tempmon_low_temp',
            self.enum.TEMPMON_PROBE_STATUS_HIGH_TEMP            : 'tempmon_high_temp',
            self.enum.TEMPMON_PROBE_STATUS_CRITICAL_TEMP        : 'tempmon_critical_temp',
            self.enum.TEMPMON_PROBE_STATUS_ERROR                : 'tempmon_error',
        }

        send_email(self.config, msgtypes[status], data)

        # maybe send more emails if config said so
        for msgtype in self.extra_emails:
            send_email(self.config, msgtype, data)

        probe.status_alert_sent = self.now


def make_daemon(config, pidfile=None):
    """
    Returns a tempmon server daemon instance.
    """
    if not pidfile:
        pidfile = config.get('rattail.tempmon', 'server.pid_path',
                             default='/var/run/rattail/tempmon-server.pid')
    return TempmonServerDaemon(pidfile, config=config)
