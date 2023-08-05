# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2017 Lance Edgar
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
Data models for tempmon
"""

from __future__ import unicode_literals, absolute_import

import datetime

import six
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from rattail.db.model import uuid_column
from rattail.db.model.core import ModelBase


Base = declarative_base(cls=ModelBase)


@six.python_2_unicode_compatible
class Client(Base):
    """
    Represents a tempmon client.
    """
    __tablename__ = 'client'
    __table_args__ = (
        sa.UniqueConstraint('config_key', name='client_uq_config_key'),
    )

    uuid = uuid_column()
    config_key = sa.Column(sa.String(length=50), nullable=False)
    hostname = sa.Column(sa.String(length=255), nullable=False)
    location = sa.Column(sa.String(length=255), nullable=True)

    disk_type = sa.Column(sa.Integer(), nullable=True, doc="""
    Integer code representing the type of hard disk used, if known.  The
    original motivation for this was to keep track of whether each client
    (aka. Raspberry Pi) was using a SD card or USB drive for the root disk.
    """)

    delay = sa.Column(sa.Integer(), nullable=True, doc="""
    Number of seconds to delay between reading / recording temperatures.  If
    not set, a default of 60 seconds will be assumed.
    """)

    notes = sa.Column(sa.Text(), nullable=True, doc="""
    Any arbitrary notes for the client.
    """)

    enabled = sa.Column(sa.Boolean(), nullable=False, default=False, doc="""
    Whether the client should be considered enabled (active).  If set, the
    client will be expected to take readings (but only for "enabled" probes)
    and the server will monitor them to ensure they are within the expected
    range etc.
    """)

    online = sa.Column(sa.Boolean(), nullable=False, default=False, doc="""
    Whether the client is known to be online currently.  When a client takes
    readings, it will mark itself as online.  If the server notices that the
    readings have stopped, it will mark the client as *not* online.
    """)

    archived = sa.Column(sa.Boolean(), nullable=False, default=False, doc="""
    Flag indicating this client is "archived".  This typically means that the
    client itself no longer exists but that the configuration for it should be
    retained, to be used as a reference later etc.  Note that "archiving" a
    client is different from "disabling" it; i.e. disabling is temporary and
    archiving is more for the long term.
    """)

    def __str__(self):
        return '{} ({})'.format(self.config_key, self.hostname)

    def enabled_probes(self):
        return [probe for probe in self.probes if probe.enabled]


@six.python_2_unicode_compatible
class Probe(Base):
    """
    Represents a probe connected to a tempmon client.
    """
    __tablename__ = 'probe'
    __table_args__ = (
        sa.ForeignKeyConstraint(['client_uuid'], ['client.uuid'], name='probe_fk_client'),
        sa.UniqueConstraint('config_key', name='probe_uq_config_key'),
    )

    uuid = uuid_column()
    client_uuid = sa.Column(sa.String(length=32), nullable=False)

    client = orm.relationship(
        Client,
        doc="""
        Reference to the tempmon client to which this probe is connected.
        """,
        backref=orm.backref(
            'probes',
            cascade='all, delete-orphan',
            doc="""
            List of probes connected to this client.
            """))

    config_key = sa.Column(sa.String(length=50), nullable=False)
    appliance_type = sa.Column(sa.Integer(), nullable=False)
    description = sa.Column(sa.String(length=255), nullable=False)
    device_path = sa.Column(sa.String(length=255), nullable=True)
    enabled = sa.Column(sa.Boolean(), nullable=False, default=True)

    good_temp_min = sa.Column(sa.Integer(), nullable=False)
    good_temp_max = sa.Column(sa.Integer(), nullable=False)
    critical_temp_min = sa.Column(sa.Integer(), nullable=False)
    critical_temp_max = sa.Column(sa.Integer(), nullable=False)

    therm_status_timeout = sa.Column(sa.Integer(), nullable=False, doc="""
    Number of minutes the temperature is allowed to be "high" before the first
    "high temp" email alert is sent.  This is typically meant to account for
    the length of the defrost cycle.  Note that this does *not* affect the
    "critical temp" emails; those are sent as soon as critical temp is reached.
    """)

    status_alert_timeout = sa.Column(sa.Integer(), nullable=False, doc="""
    Number of minutes between successive "high/critical temp" emails.  These
    alerts will continue to be sent until the temperature returns to normal
    range.
    """)

    notes = sa.Column(sa.Text(), nullable=True, doc="""
    Any arbitrary notes for the probe.
    """)

    status = sa.Column(sa.Integer(), nullable=True)
    status_changed = sa.Column(sa.DateTime(), nullable=True)
    status_alert_sent = sa.Column(sa.DateTime(), nullable=True)

    def __str__(self):
        return self.description


@six.python_2_unicode_compatible
class Reading(Base):
    """
    Represents a single temperature reading from a tempmon probe.
    """
    __tablename__ = 'reading'
    __table_args__ = (
        sa.ForeignKeyConstraint(['client_uuid'], ['client.uuid'], name='reading_fk_client'),
        sa.ForeignKeyConstraint(['probe_uuid'], ['probe.uuid'], name='reading_fk_probe'),
    )

    uuid = uuid_column()

    client_uuid = sa.Column(sa.String(length=32), nullable=False)
    client = orm.relationship(
        Client,
        doc="""
        Reference to the tempmon client which took this reading.
        """,
        backref=orm.backref(
            'readings',
            cascade='all, delete-orphan'))

    probe_uuid = sa.Column(sa.String(length=32), nullable=False)
    probe = orm.relationship(
        Probe,
        doc="""
        Reference to the tempmon probe which took this reading.
        """,
        backref=orm.backref(
            'readings',
            cascade='all, delete-orphan'))

    taken = sa.Column(sa.DateTime(), nullable=False, default=datetime.datetime.utcnow)
    degrees_f = sa.Column(sa.Numeric(precision=8, scale=4), nullable=False)

    def __str__(self):
        return str(self.degrees_f)
