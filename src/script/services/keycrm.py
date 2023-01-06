import logging

import requests

from src.domain.lead.dto.lead import LeadDTO

UPLOAD_LEAD_URL = "https://openapi.keycrm.app/v1/leads"

logger = logging.getLogger(__name__)


def upload_leads(leads: list[LeadDTO], api_token: str) -> None:
    for lead in leads:
        _upload_lead(lead, api_token)


def _upload_lead(lead: LeadDTO, api_token: str) -> None:
    body = {
        "utm_source": "Facebook",
        "utm_medium": lead.platform,
        "utm_campaign": lead.campaign_name,
        "utm_term": lead.adset_name,
        "utm_content": lead.ad_name,
        "source_id": 4,
        "manager_comment": "\n".join(
            field["name"] + "\n" + field["values"][0]
            for field in lead.field_data
            if field["name"] not in ["phone_number", "first_name"]
        ),
        "contact": {
            "phone": [
                field["values"][0]
                for field in lead.field_data
                if field["name"] == "phone_number"
            ][0],
            "full_name": [
                field["values"][0]
                for field in lead.field_data
                if field["name"] == "first_name"
            ][0],
        },
    }
    headers = {
        "Authorization": "Bearer " + api_token,
        "Content-Type": "application/json",
    }

    response = requests.post(url=UPLOAD_LEAD_URL, json=body, headers=headers)

    logger.debug(response.text)
