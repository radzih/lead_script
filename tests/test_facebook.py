import json
import logging
import time

from facebook_business import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

from src.config import load_config
from src.script.services.facebook import get_all_new_leads

logger = logging.getLogger(__name__)


def test_get_all_new_leads():
    config = load_config()

    FacebookAdsApi.init(
        config.facebook.app_id,
        config.facebook.app_secret,
        config.facebook.access_token,
    )

    adaccount = AdAccount(config.facebook.adaccount_id)

    with open("./src/script/time.json", "w") as file:
        json.dump(
            obj={"last_request_time": int(time.time()) - 2592000},
            fp=file,
        )

    leads = get_all_new_leads(adaccount)

    logger.debug(leads[0])

    assert len(leads) > 0
