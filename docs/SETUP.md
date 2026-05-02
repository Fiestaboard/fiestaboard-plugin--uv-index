# UV Index Setup Guide

Display the current UV index and sun protection advice using Open-Meteo.

## Overview

The UV Index plugin queries the Open-Meteo Air Quality API for current UV index data at a configured latitude/longitude. It calculates sun-protection advice (SPF recommendation, shade needed) from the UV value. No API key required.

- API reference: https://open-meteo.com/en/docs/air-quality-api

### Prerequisites

No API key required. Configure your latitude/longitude.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **UV Index**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `uv_index` plugin variables:
   ```
   {{{ uv_index.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `uv_index.uv_index` | Current UV index value | `7.2` |
| `uv_index.risk_level` | UV risk level (Low/Moderate/High/Very High/Extreme) | `High` |
| `uv_index.protection` | Recommended protection (e.g. SPF 30+) | `SPF 30+, seek shade` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `latitude` | Latitude | Location latitude (decimal degrees). | `40.7128` |
| `longitude` | Longitude | Location longitude (decimal degrees). | `-74.006` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to refresh UV data. | `1800` |

## Troubleshooting

- **UV always 0** — check your latitude/longitude settings.
- **Network error** — verify connectivity to `air-quality-api.open-meteo.com`.

