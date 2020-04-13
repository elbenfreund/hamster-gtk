# -*- encoding: utf-8 -*-


# This file is part of 'hamster-gtk'.
#
# 'hamster-gtk' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 'hamster-gtk' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 'hamster-gtk'.  If not, see <http://www.gnu.org/licenses/>.

"""Unittests for RawFactCompletion."""

from __future__ import absolute_import, unicode_literals

from gi.repository import Gtk
from orderedset import OrderedSet

from hamster_gtk.misc.widgets.raw_fact_entry import RawFactCompletion


def test_init(app, mocker):
    """Test instantiation."""
    result = RawFactCompletion(app)
    assert result.get_model()
    assert result.get_text_column() == 0


def test__get_stores(raw_fact_completion, activity_factory, mocker):
    """Make sure the ``ListStore`` is populated to our expectations."""
    raw_fact_completion._get_activities = mocker.MagicMock(
        return_value=activity_factory.build_batch(5))
    raw_fact_completion._populate_stores(None)
    assert raw_fact_completion._get_activities.called
    for key, store in raw_fact_completion.segment_models.items():
        assert isinstance(store, Gtk.ListStore)
        assert len(store) == 5


def test__get_activities(app, raw_fact_completion, fact_factory, mocker):
    """Make sure that we fetch the right activities and remove duplicates."""
    # In reality we can not get duplicate facts but separate facts with the
    # same ``Activity`` but this will do just fine.
    fact_1, fact_2 = fact_factory.build_batch(2)
    app.controller.facts.get_all = mocker.MagicMock(
        return_value=[fact_1, fact_2, fact_1])
    result = raw_fact_completion._get_activities()
    assert result == OrderedSet([fact_1.activity, fact_2.activity])
