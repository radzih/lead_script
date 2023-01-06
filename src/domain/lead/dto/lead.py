from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class LeadDTO:
    id: int
    form_id: int
    created_time: datetime
    field_data: list[dict[str, Any]]
    campaign_name: str
    ad_name: str
    adset_name: str
    platform: str
