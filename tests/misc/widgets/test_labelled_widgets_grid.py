# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest

from hamster_gtk.misc.widgets import LabelledWidgetsGrid


@pytest.mark.parametrize('no_fields', (True, False))
def test_init(preference_page_fields, no_fields):
    """Make sure instantiation works with and without fields provided."""
    if no_fields:
        grid = LabelledWidgetsGrid()
        assert grid._fields == {}
    else:
        grid = LabelledWidgetsGrid(preference_page_fields)
        assert grid._fields == preference_page_fields
    rows = len(grid.get_children()) / 2
    assert rows == len(grid._fields)


def test_get_values(labelled_widgets_grid, preference_page_fields, mocker):
    """Make sure widget fetches values for all its sub-widgets."""
    for key, (label, widget) in preference_page_fields.items():
        widget.get_config_value = mocker.MagicMock()
    labelled_widgets_grid.get_values()
    for key, (label, widget) in preference_page_fields.items():
        assert widget.get_config_value.called


def test_set_values(labelled_widgets_grid, preference_page_fields, mocker):
    """Make sure widget sets values for all its sub-widgets."""
    for key, (label, widget) in preference_page_fields.items():
        widget.set_config_value = mocker.MagicMock()
    labelled_widgets_grid.set_values(preference_page_fields)
    for key, (label, widget) in preference_page_fields.items():
        assert widget.set_config_value.called
