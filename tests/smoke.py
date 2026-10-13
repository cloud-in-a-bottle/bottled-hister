import json
import os
import subprocess
import time
import urllib.error
import urllib.request
import uuid


ENGINE = os.environ.get("CONTAINER_ENGINE", "docker")
IMAGE = os.environ.get("HISTER_TEST_IMAGE", "bottled-hister:test")
NAME = "hister-smoke-" + uuid.uuid4().hex[:12]
VOLUME = NAME + "-data"


def engine(*args):
    return subprocess.check_output([ENGINE, *args], text=True).strip()


def start():
    engine(
        "run", "-d", "--name", NAME, "--memory", "512m", "--cpus", "1",
        "-p", "127.0.0.1::4433", "-v", VOLUME + ":/data",
        "-e", "BOTTLE_APP_DATA_DIR=/data",
        "-e", "BOTTLE_APP_NAME=hister",
        "-e", "BOTTLE_ZONE_DOMAIN=example.com", IMAGE,
    )
    port = engine("port", NAME, "4433/tcp").rsplit(":", 1)[1]
    base = "http://127.0.0.1:" + port
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(base + "/health", timeout=2) as response:
                if response.status == 200:
                    return base
        except (urllib.error.URLError, TimeoutError):
            time.sleep(1)
    raise RuntimeError("Hister did not become healthy\n" + engine("logs", NAME))


def request(base, path, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(base + path, data=body, headers={
        "Content-Type": "application/json", "Origin": "hister://",
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
        return json.loads(raw) if raw else response.status


try:
    engine("volume", "create", VOLUME)
    base = start()
    config = request(base, "/api/config")
    assert config["baseUrl"] == "https://hister.example.com", config
    assert config["wsUrl"] == "wss://hister.example.com/search", config
    assert config["authMode"] == "none" and config["canWrite"], config
    assert not config["public"] and not config["semanticEnabled"], config
    assert request(base, "/api/add", {
        "url": "https://example.org/hister-smoke",
        "title": "Persistent bottle document",
        "text": "A unique bottlepersistcheck document for full text search.",
        "html": "<p>A unique bottlepersistcheck document for full text search.</p>",
    }) == 201

    def verify_document():
        result = request(base, "/search?format=json&q=bottlepersistcheck")
        assert any(d["url"] == "https://example.org/hister-smoke" for d in result["documents"]), result
        preview = request(base, "/api/preview?url=https%3A%2F%2Fexample.org%2Fhister-smoke")
        assert "bottlepersistcheck" in preview["content"], preview

    verify_document()
    engine("stop", NAME)
    engine("rm", NAME)
    base = start()
    verify_document()
    print("PASS: startup, HTTPS URLs, single-user mode, ingest, search, previews, persistent data")
except BaseException:
    subprocess.run([ENGINE, "logs", NAME], check=False)
    raise
finally:
    subprocess.run([ENGINE, "rm", "-f", NAME], check=False)
    subprocess.run([ENGINE, "volume", "rm", VOLUME], check=False)
