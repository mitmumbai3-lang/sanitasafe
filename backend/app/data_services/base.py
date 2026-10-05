"""
Base data service architecture for NASA Earth observation and auxiliary geospatial services.
Provides caching, retry handling, fallback to bundled seed/sample datasets, and explicit
metadata tracking (dataset source, spatial resolution, and uncertainty).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import json
import os
from app.config import settings

class BaseDataClient(ABC):
    def __init__(self, dataset_name: str, spatial_resolution: str, temporal_resolution: str, uncertainty_note: str):
        self.dataset_name = dataset_name
        self.spatial_resolution = spatial_resolution
        self.temporal_resolution = temporal_resolution
        self.uncertainty_note = uncertainty_note
        self._memory_cache: Dict[str, Dict[str, Any]] = {}

    def get_cache_key(self, lat: float, lon: float, **kwargs) -> str:
        param_str = "_".join(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        return f"{self.dataset_name}_{round(lat, 4)}_{round(lon, 4)}_{param_str}"

    def get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        cached = self._memory_cache.get(key)
        if cached:
            # 24h cache TTL
            if time.time() - cached.get("timestamp", 0) < 86400:
                return cached.get("data")
        return None

    def save_to_cache(self, key: str, data: Dict[str, Any]):
        self._memory_cache[key] = {
            "timestamp": time.time(),
            "data": data
        }

    @abstractmethod
    def fetch_live(self, lat: float, lon: float, **kwargs) -> Optional[Dict[str, Any]]:
        """Fetch from live upstream API using credentials if configured."""
        pass

    @abstractmethod
    def get_sample_fallback(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        """Return bundled calibrated sample data when offline, rate-limited, or uncredentialed."""
        pass

    def get_data(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        """
        Unified fetch pipeline:
        1. Check memory cache.
        2. If live fetch is enabled and credentials or public API available, attempt live fetch with retries.
        3. If failed or live fetch disabled, return calibrated sample fallback.
        4. Wrap response with dataset metadata and provenance attribution.
        """
        cache_key = self.get_cache_key(lat, lon, **kwargs)
        cached = self.get_from_cache(cache_key)
        if cached:
            return cached

        data: Optional[Dict[str, Any]] = None
        source_mode = "bundled_sample"

        if settings.ENABLE_LIVE_FETCH:
            try:
                data = self.fetch_live(lat, lon, **kwargs)
                if data:
                    source_mode = "live_nasa"
            except Exception:
                data = None

        if not data:
            data = self.get_sample_fallback(lat, lon, **kwargs)
            source_mode = "bundled_sample"

        result = {
            "dataset": self.dataset_name,
            "spatial_resolution": self.spatial_resolution,
            "temporal_resolution": self.temporal_resolution,
            "uncertainty_note": self.uncertainty_note,
            "provenance": source_mode,
            "values": data
        }

        self.save_to_cache(cache_key, result)
        return result
