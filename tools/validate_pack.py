#!/usr/bin/env python3
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
REQUIRED_SERVICES = ("discord", "telegram", "whatsapp", "youtube", "instagram", "tiktok")
REQUIRED_TRANSPORT = ("tls_fragment", "sni_split", "quic_udp443_fallback")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not MANIFEST.is_file():
        fail("manifest.json is missing")

    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"manifest.json is invalid JSON: {exc}")

    if data.get("schema") != 1:
        fail("schema must be 1")
    if data.get("pack_id") != "nfqws2-android-services":
        fail("unexpected pack_id")
    if not isinstance(data.get("version"), str) or not data["version"].strip():
        fail("version must be a non-empty string")
    if not isinstance(data.get("version_code"), int) or data["version_code"] < 1:
        fail("version_code must be an integer >= 1")
    if not isinstance(data.get("min_app_version_code"), int) or data["min_app_version_code"] < 1:
        fail("min_app_version_code must be an integer >= 1")
    if not isinstance(data.get("min_engine_tag"), str) or not data["min_engine_tag"].strip():
        fail("min_engine_tag must be a non-empty string")

    transport = data.get("transport")
    if not isinstance(transport, dict):
        fail("transport must be an object")
    for key in REQUIRED_TRANSPORT:
        if not isinstance(transport.get(key), bool):
            fail(f"transport.{key} must be boolean")

    services = data.get("services")
    if not isinstance(services, dict):
        fail("services must be an object")

    missing = [name for name in REQUIRED_SERVICES if name not in services]
    if missing:
        fail("missing services: " + ", ".join(missing))

    for name in REQUIRED_SERVICES:
        entry = services[name]
        if not isinstance(entry, dict):
            fail(f"services.{name} must be an object")
        if not isinstance(entry.get("enabled"), bool):
            fail(f"services.{name}.enabled must be boolean")
        lua_path = entry.get("lua")
        if not isinstance(lua_path, str) or not lua_path.endswith(".lua"):
            fail(f"services.{name}.lua must point to a .lua file")
        path = (ROOT / lua_path).resolve()
        try:
            path.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"services.{name}.lua escapes repository root")
        if not path.is_file():
            fail(f"services.{name}.lua does not exist: {lua_path}")
        text = path.read_text(encoding="utf-8")
        if "service" not in text or name not in text:
            fail(f"{lua_path} does not identify service {name}")

    print(f"Strategy Pack OK: {data['version']} (code {data['version_code']})")


if __name__ == "__main__":
    main()
