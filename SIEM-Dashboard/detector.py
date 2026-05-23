THREAT_KEYWORDS = [
    "failed login",
    "sql injection",
    "brute force",
    "malware",
    "unauthorized",
    "ddos",
    "xss attack"
]

def detect_threat(log):

    for keyword in THREAT_KEYWORDS:
        if keyword.lower() in log.lower():
            return True

    return False