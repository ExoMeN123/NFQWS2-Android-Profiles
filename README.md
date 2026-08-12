# NFQWS2 Android Profiles

Public Strategy Pack channel for the NFQWS2 Android and Android TV no-root applications.

This repository is intentionally separate from the Android application source code and from the upstream `bol-van/zapret2` engine.

## Update channels

- **Engine channel:** upstream `bol-van/zapret2`, gated by Android compatibility builds.
- **Strategy channel:** this repository.

The Android applications download only the Strategy Pack manifest and supported strategy assets from this public repository. No GitHub token is embedded in the APK.

## Services

- Discord
- Telegram
- WhatsApp
- YouTube
- Instagram
- TikTok

## Safety / rollback

The apps keep a factory Strategy Pack inside the APK and retain the previous downloaded pack. If a remote strategy causes problems, users can roll back without reinstalling the application.

## Current backend

The current no-root Functional Preview consumes the transport flags in `manifest.json`:

- `tls_fragment`
- `sni_split`
- `quic_udp443_fallback`

The `lua` paths are reserved for the upcoming nfqws2/Lua bridge. They are not yet executed by Functional Preview 0.4.
