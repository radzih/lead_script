from datetime import datetime

from src.config import load_config
from src.script.services.keycrm import upload_leads
from src.domain.lead.dto.lead import LeadDTO


def test_upload():
    config = load_config()

    lead = LeadDTO(
        id=123,
        form_id=123,
        created_time=datetime.now(),
        field_data=[
            {"name": "яка площа посівів", "values": ["2 га "]},
            {"name": "яка культура", "values": ["тестова культура"]},
            {"name": "first_name", "values": ["test"]},
            {"name": "phone_number", "values": ["+380999999898"]},
        ],
        campaign_name="Test campaign",
        ad_name="test_ad_name",
        adset_name="test adset_name",
        platform="Facebook",
    )

    upload_leads(
        leads=[lead],
        api_token=config.keycrm.api_token,
    )
