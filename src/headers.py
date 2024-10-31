from src.agent import gr_ua

def headers():
    return {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": '"Microsoft Edge;v=129, Not=A?Brand;v=8, Chromium;v=129, Microsoft Edge WebView2;v=129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://mdkefjwsfepf.dropstab.com/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "user-agent": gr_ua()
}