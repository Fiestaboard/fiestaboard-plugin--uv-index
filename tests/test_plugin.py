"""Tests for the uv_index plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.uv_index import UvIndexPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "uv_index",
    "name": "UV Index",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "latitude": {
                "type": "number",
                "title": "Latitude",
                "description": "Location latitude (decimal degrees).",
                "default": 40.7128,
                "minimum": -90,
                "maximum": 90
            },
            "longitude": {
                "type": "number",
                "title": "Longitude",
                "description": "Location longitude (decimal degrees).",
                "default": -74.006,
                "minimum": -180,
                "maximum": 180
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to refresh UV data.",
                "default": 1800,
                "minimum": 900
            }
        },
        "required": []
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
{
    "latitude": 40.7128,
    "longitude": -74.006,
    "hourly": {
        "time": [
            "2026-05-01T12:00",
            "2026-05-01T13:00",
            "2026-05-01T14:00"
        ],
        "uv_index": [
            5.5,
            7.2,
            6.8
        ]
    }
}
""")


@pytest.fixture
def plugin():
    return UvIndexPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = UvIndexPlugin(MANIFEST)
    p.config = json.loads("""
{
    "latitude": 40.7128,
    "longitude": -74.006
}
""")
    return p


class TestUvIndexPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "uv_index"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    @patch("plugins.uv_index.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "uv_index" in result.data, "missing variable: uv_index"
        assert "risk_level" in result.data, "missing variable: risk_level"
        assert "protection" in result.data, "missing variable: protection"

    @patch("plugins.uv_index.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.uv_index.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

