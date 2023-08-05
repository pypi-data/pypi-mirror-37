import pygass as pya
from pygass import constants as st


pya.ANALYTICS_URL = "https://www.google-analytics.com/debug/collect"
st.ANALYTICS_CODE = "UA-10000000-1"
CLIENT_ID = 1337


def valid_state(response):
    return response["hitParsingResult"][-1]["valid"]


def valid_url(response):
    return response["hitParsingResult"][-1]["hit"]


def valid_message(response):
    return response["parserMessage"][-1]["description"]


def test_add_ip_user_agent():
    results = pya.proxy_server({})
    assert results["uip"] is None
    assert results["ua"] is None

    results = pya.proxy_server({}, ip="127.0.0.1")
    assert results["uip"] == "127.0.0.1"
    assert results["ua"] is None

    results = pya.proxy_server({}, user_agent="Test Agent")
    assert results["uip"] is None
    assert results["ua"] == "Test Agent"

    results = pya.proxy_server({}, ip="127.0.0.1", user_agent="Test Agent")
    assert results["uip"] == "127.0.0.1"
    assert results["ua"] == "Test Agent"


def test_pageview():
    result = pya.track_pageview(CLIENT_ID, "/test/client/pageview")
    assert valid_state(result) is True
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=pageview&dp=%2Ftest%2Fclient%2Fpageview"


def test_pageview_proxy_server():
    result = pya.track_pageview(
        client_id=CLIENT_ID,
        page="/test/client/pageview",
        ip="111.111.111.111",
        user_agent="Test Agent",
    )
    assert valid_state(result) is True
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=pageview&dp=%2Ftest%2Fclient%2Fpageview&uip=111.111.111.111&ua=Test+Agent?_anon_uip=111.111.111.0"


def test_event():
    result = pya.track_event(CLIENT_ID, action="start", category="click")
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_state(result) is True
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=event&ec=click&ea=start"


def test_event_proxy_server():
    result = pya.track_event(
        CLIENT_ID,
        action="start",
        category="click",
        ip="111.111.111.111",
        user_agent="Test Agent",
    )
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_state(result) is True
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=event&ec=click&ea=start&uip=111.111.111.111&ua=Test+Agent?_anon_uip=111.111.111.0"


def test_transaction():
    result = pya.track_transaction(CLIENT_ID, transaction_id=1)
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_state(result) is True
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=transaction&ti=1"


def test_transaction_proxy_server():
    result = pya.track_transaction(
        CLIENT_ID,
        transaction_id=1,
        ip="111.111.111.111",
        user_agent="Test Agent",
    )
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_state(result) is True
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=transaction&ti=1&uip=111.111.111.111&ua=Test+Agent?_anon_uip=111.111.111.0"


def test_item():
    result = pya.track_item(CLIENT_ID, transaction_id=1, name="item 1")
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_state(result) is True
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=item&ti=1&in=item+1&iq=1"


def test_item_proxy_server():
    result = pya.track_item(
        CLIENT_ID,
        transaction_id=1,
        name="item 1",
        ip="111.111.111.111",
        user_agent="Test Agent",
    )
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_state(result) is True
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=item&ti=1&in=item+1&iq=1&uip=111.111.111.111&ua=Test+Agent?_anon_uip=111.111.111.0"


def test_social():
    result = pya.track_social(
        CLIENT_ID, action="like", network="facebook", target="/home"
    )
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_state(result) is True
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=social&sa=like&sn=facebook&st=%2Fhome"


def test_social_proxy_server():
    result = pya.track_social(
        CLIENT_ID,
        action="like",
        network="facebook",
        target="/home",
        ip="111.111.111.111",
        user_agent="Test Agent",
    )
    assert valid_message(result) == "Found 1 hit in the request."
    assert valid_state(result) is True
    assert valid_url(
        result
    ) == "/debug/collect?v=1&tid=UA-10000000-1&cid=1337&t=social&sa=like&sn=facebook&st=%2Fhome&uip=111.111.111.111&ua=Test+Agent?_anon_uip=111.111.111.0"
