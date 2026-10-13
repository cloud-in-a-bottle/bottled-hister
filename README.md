# Hister for Cloud in a Bottle

Packaging for [Hister](https://github.com/asciimoo/hister), a private full-text search engine for visited web pages and documents, on [Cloud in a Bottle](https://cloudinabottle.org).

## Deploy

```sh
bottle app deploy https://github.com/cloud-in-a-bottle/bottled-hister@andrew/package-hister --name hister --wait
```

Open Hister from the instance dashboard. The signed-in owner goes straight to the search interface, with no separate Hister account or setup wizard. Guests are redirected to Cloud in a Bottle sign-in. Only the upstream `/health` endpoint is public.

## Index your browsing history

Install the upstream [Firefox or Chrome extension](https://hister.org/docs/browser-extension). Set its server URL to `https://hister.<your-instance-domain>` (use your deployed app name if different). Create an API token in your Cloud in a Bottle dashboard, then add a custom header in the extension options: name `Authorization`, value `Bearer <your-platform-token>`. Leave the Hister access-token field empty and save the settings. Keep that platform token private: it grants access to your instance, not just Hister.

You can also add content manually through Hister's Add page. HTTP API and MCP clients authenticate using the same `Authorization: Bearer ...` platform-token header. For example, `bottle curl "https://hister.<your-instance-domain>/search?format=json&q=example"` sends your platform credentials automatically. The upstream Hister CLI uses `X-Access-Token`, which does not authenticate with the platform; use platform-authenticated HTTP requests for remote imports. See the [upstream documentation](https://hister.org/docs) for queries, API formats, rules, previews, and integrations.

## Storage and configuration

The SQLite database, full-text indexes, rules, previews, and session key all live in `BOTTLE_APP_DATA_DIR`. They survive restarts and rebuilds and are included in the platform's app-data backups. This package requests access only to its own persistent data.

Optional Hister settings can be stored in `config.yml` in that directory. Restart the app after editing it. The wrapper always sets the public HTTPS URL, listener, data directory, and single-user authentication mode for Cloud in a Bottle. Optional semantic search remains disabled by default; configure an embeddings provider in the Hister configuration to enable it. The bundled upstream image includes yt-dlp for supported video extractors. Browser-based crawling needs a separate browser on the machine running the Hister CLI, as described in the upstream docs.

The container is based on the digest-pinned upstream Hister v0.20.0 image and supports Linux amd64 and arm64. It runs as container root inside Cloud in a Bottle's rootless isolation so it can write the platform's persistent-data mount, with no extra capabilities or published ports.

See [TESTING.md](TESTING.md) for the container smoke test and live-platform verification results.

## Licenses

Original packaging files are [MIT licensed](LICENSE). Hister is AGPL-3.0-or-later; its full license and corresponding source are available at [the pinned v0.20.0 release](https://github.com/asciimoo/hister/tree/v0.20.0). The image includes the upstream license at `/usr/share/licenses/hister/LICENSE` and the packaging license at `/usr/share/licenses/bottled-hister/LICENSE`. Dependencies in the upstream image retain their respective licenses, including yt-dlp's upstream notices.
