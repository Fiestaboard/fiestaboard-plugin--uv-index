"""Display the current UV index and sun protection advice using Open-Meteo."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
USER_AGENT = "FiestaBoard UV Index Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--uv-index)"


class UvIndexPlugin(PluginBase):
    """UV Index plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "uv_index"

    def fetch_data(self) -> PluginResult:
        try:
            lat = float(self.config.get("latitude") or 40.7128)
            lon = float(self.config.get("longitude") or -74.0060)

            response = requests.get(
                API_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "hourly": "uv_index",
                    "forecast_days": 1,
                },
                headers={"User-Agent": USER_AGENT},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            import datetime
            hourly = data.get("hourly", {})
            times = hourly.get("time", [])
            uvs = hourly.get("uv_index", [])

            # Find the UV for the current or nearest hour
            now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:00")
            uv_value = 0.0
            for i, t in enumerate(times):
                if t >= now:
                    uv_value = float(uvs[i] if i < len(uvs) else 0)
                    break

            # Risk level
            if uv_value < 3:
                risk_level = "Low"
                protection = "No protection needed"
            elif uv_value < 6:
                risk_level = "Moderate"
                protection = "SPF 15+, hat"
            elif uv_value < 8:
                risk_level = "High"
                protection = "SPF 30+, seek shade"
            elif uv_value < 11:
                risk_level = "Very High"
                protection = "SPF 50+, limit time"
            else:
                risk_level = "Extreme"
                protection = "Avoid midday sun"

            return PluginResult(
                available=True,
                data={
                    "uv_index": round(uv_value, 1),
                    "risk_level": risk_level,
                    "protection": protection,
                },
            )
        except Exception as e:
            logger.exception("Error fetching UV index")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        return []

    def cleanup(self) -> None:
        pass
