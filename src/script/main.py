import logging

from facebook_business import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

from src.script.services.facebook import get_new_leads_with_form_id
from src.script.services.keycrm import upload_leads
from src.config import load_config

logger = logging.getLogger(__name__)


def main():
    config = load_config()

    logging.basicConfig(
        level=logging.DEBUG if config.script.debug else logging.INFO,
        format=(
            "%(filename)s:%(lineno)d #%(levelname)-8s"
            "[%(asctime)s] - %(name)s - %(message)s"
        ),
    )

    facebook = config.facebook

    FacebookAdsApi.init(
        facebook.app_id,
        facebook.app_secret,
        facebook.access_token,
        debug=config.script.debug,
    )

    adaccount = AdAccount(facebook.adaccount_id)

    logger.info("Start get leads")

    leads = get_new_leads_with_form_id(adaccount, config.facebook.form_ids)

    logger.info("Uploading leads")

    upload_leads(leads[:-3], config.keycrm.api_token)

    logger.info("Finished")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
