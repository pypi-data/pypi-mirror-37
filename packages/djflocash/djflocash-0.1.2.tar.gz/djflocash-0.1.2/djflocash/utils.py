import logging
import urllib.parse

import requests
from django.conf import settings


def get_ip_address(request):
    ip = ""
    try:
        info = dict(
            v.split("=")
            for v in request.META["HTTP_FORWARDED"].split(",")[0].split(";")
            if "=" in v
        )
        ip = info.get("for", "")
    except KeyError:
        pass
    if not ip:
        try:
            ip = request.META["HTTP_X_FORWARDED_FOR"].split(",")[0]
        except KeyError:
            pass
    if not ip:
        ip = request.META["REMOTE_ADDR"]
    return ip


def validate_notification_request(params, validate_url="/validateNotify.do"):  # request.POST.dict()
    data = dict(params)
    data["cmd"] = "notify-validate"
    url = urllib.parse.urljoin(settings.FLOCASH_BASE_URL, validate_url)
    try:
        response = requests.post(url, data)
        return response.status_code == 200 and response.text.lower() == "verified"
    except Exception as e:
        logging.error(
            "Exception while validation notification with trans_id: %s: %s",
            data.get("trans_id", '?'),
            e,
            extra={"params": params, "url": url},
        )
