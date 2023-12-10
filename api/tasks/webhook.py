from urllib.parse import urlparse

from http.client import HTTPSConnection
from http.client import HTTPResponse

from datetime import datetime

from core.celery import celery_app
from config import (
    JITTER_MAX_RETRIES,
    JITTER_RETRY_BACKOFF,
    JITTER_RETRY_BACKOFF_MAX,
    JITTER_RETRY_JITTER,
)

from utils.helpers import get_status_string

import json


def make_wehbook_request(
    url: str, method: str, query: dict, payload: dict, headers: dict, *args, **kwargs
) -> dict:
    parsed_url = urlparse(url)

    host = parsed_url.netloc
    path = parsed_url.path

    end_point = (
        path + "?" + "&".join([f"{key}={value}" for key, value in query.items()])
    )

    conn = HTTPSConnection(host)

    # start time
    start_time = datetime.utcnow()

    # Perform DNS lookup
    conn.connect()
    dns_time = datetime.utcnow()

    if type(payload)() == {}:
        payload = json.dumps(payload)

    # Perform SSL handshake
    conn.request(method, end_point, payload, headers)
    ssl_time = datetime.utcnow()

    # getting HTTP Response
    response: HTTPResponse = conn.getresponse()

    data = response.read()
    response_status = response.status
    response_data = data.decode("utf-8")
    conn.close()

    end_time = datetime.utcnow()

    # Calculate times
    dns_duration = round((dns_time - start_time).microseconds / 1000, 2)
    ssl_duration = round((ssl_time - dns_time).microseconds / 1000, 2)
    request_duration = round((end_time - ssl_time).microseconds / 1000, 2)
    total_time = round(dns_duration + ssl_duration + request_duration, 2)

    return {
        "status": get_status_string(response_status),
        "http_status_code": response_status,
        "http_response_body": response_data,
        "request_ts": start_time,
        "dns_resolution_time": dns_duration,
        "ssl_handshake_time": ssl_duration,
        "request_time": request_duration,
        "total_time": total_time,
    }


@celery_app.task(
    autoretry_for=(Exception,),
    max_retries=JITTER_MAX_RETRIES,
    retry_backoff=JITTER_RETRY_BACKOFF,
    retry_backoff_max=JITTER_RETRY_BACKOFF_MAX,
    retry_jitter=JITTER_RETRY_JITTER,
)
def webhook_job(
    pt_name: str,
    url: str,
    method: str,
    query: dict,
    payload: dict,
    headers: dict,
    *args,
    **kwargs,
):
    tr_data = make_wehbook_request(url, method, query, payload, headers)
    print(tr_data)

    if tr_data["status"] != "success":
        raise Exception
