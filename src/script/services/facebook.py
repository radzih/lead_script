import time
import json
import logging

from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.lead import Lead

from src.domain.lead.dto.lead import LeadDTO

DELAY = 10

logger = logging.getLogger(__name__)


def get_campaigns(adaccount: AdAccount) -> list[Campaign]:
    campaigns: list[Campaign] = adaccount.get_campaigns(fields=["name"])
    return campaigns


def get_ads(campaign: Campaign) -> list[Ad]:
    ads: list[Ad] = campaign.get_ads()

    return ads


def get_all_ads(campaigns: list[Campaign]) -> list[Ad]:
    ads = []
    for i, campaign in enumerate(campaigns):
        time.sleep(DELAY)
        ads.extend(get_ads(campaign))

        logger.debug(f"Campaign {i}/{len(campaigns)}")

    return ads


def get_ad_leads(ad: Ad) -> list[Lead]:
    params = {
        "filtering": [
            {
                "field": "time_created",
                "operator": "GREATER_THAN",
                "value": get_last_update_time(),
            },
        ],
    }
    ad_leads: list[Lead] = ad.get_leads(
        fields=[
            "ad_name",
            "campaign_name",
            "adset_name",
            "form_id",
            "created_time",
            "field_data",
            "id",
            "platform",
        ],
        params=params,
    )
    return ad_leads


def get_all_ad_leads(ads: list[Ad]) -> list[Lead]:
    leads = []

    for i, ad in enumerate(ads):
        time.sleep(DELAY)
        leads.extend(get_ad_leads(ad))

        logger.debug(f"Ad {i}/{len(ads)}")

    return leads


def get_all_new_leads(adaccount: AdAccount) -> list[Lead]:
    campaigns = get_campaigns(adaccount)
    ads = get_all_ads(campaigns)
    leads = get_all_ad_leads(ads)
    return leads


def filter_leads_by_form_id(
    leads: list[Lead],
    form_ids: list[int],
) -> list[Lead]:
    filtered_leads = []

    for lead in leads:
        if lead._data.get("form_id") not in form_ids:
            continue
        filtered_leads.append(lead)

    return filtered_leads


def get_new_leads_with_form_id(
    adaccount: AdAccount,
    form_ids: list[int],
) -> list[LeadDTO]:
    leads = get_all_new_leads(adaccount)
    filtered_leads = filter_leads_by_form_id(leads, form_ids)

    save_last_update_time()

    logger.info(f"Find {len(filtered_leads)} new leads")

    return [LeadDTO(**lead._data) for lead in filtered_leads]


def save_last_update_time() -> None:
    with open("./src/script/time.json", "w") as file:
        json.dump(obj={"last_request_time": int(time.time())}, fp=file)


def get_last_update_time() -> int:
    with open("./src/script/time.json", "r") as file:
        data = json.load(file)
    return int(data["last_request_time"])
