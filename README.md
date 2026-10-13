# Hister for Cloud in a Bottle

Packaging for [Hister](https://github.com/asciimoo/hister), a private full-text search engine for visited web pages and documents, on [Cloud in a Bottle](https://cloudinabottle.org).

## Deploy

```sh
bottle app deploy https://github.com/cloud-in-a-bottle/bottled-hister@andrew/package-hister --name hister --wait
```

The repository is private, so your instance needs GitHub access to clone it. Open Hister from the instance dashboard. The signed-in owner goes straight to the search interface, with no separate Hister account or setup wizard. Guests are redirected to Cloud in a Bottle sign-in. Only the upstream `/health` endpoint is public.

## Index your browsing history

Install the upstream [Firefox or Chrome extension](https://hister.org/docs/browser-extension). Set its server URL to `https://hister.<your-instance-domain>` (use your deployed app name if different). Sign in to Cloud in a Bottle in the same browser, then save the extension settings to synchronize the server cookies. Leave the Hister access-token field empty. The extension uses your Cloud in a Bottle session; sign in again and resave settings when the session expires.

You can also add content manually through Hister's Add page and import documents using the upstream CLI. For CLI or MCP clients, send a Cloud in a Bottle API token in the `Authorization: Bearer ...` header. Hister's `X-Access-Token` header alone does not authenticate with the platform. See the [upstream documentation](https://hister.org/docs) for queries, import formats, rules, previews, and integrations.

## Storage and configuration

The SQLite database, full-text indexes, rules, previews, and session key all live in `BOTTLE_APP_DATA_DIR`. They survive restarts and rebuilds and are included in the platform's app-data backups. This package requests access only to its own persistent data.

Optional Hister settings can be stored in `config.yml` in that directory. Restart the app after editing it. The wrapper always sets the public HTTPS URL, listener, data directory, and single-user authentication mode for Cloud in a Bottle. Optional semantic search remains disabled by default; configure an embeddings provider in the Hister configuration to enable it. The bundled upstream image includes yt-dlp for supported video extractors. Browser-based crawling needs a separate browser on the machine running the Hister CLI, as described in the upstream docs.

The container is based on the digest-pinned upstream Hister v0.20.0 image and supports Linux amd64 and arm64. It runs as container root inside Cloud in a Bottle's rootless isolation so it can write the platform's persistent-data mount, with no extra capabilities or published ports.

## Licenses

Original packaging files are [MIT licensed](LICENSE). Hister is AGPL-3.0-or-later; its full license and corresponding source are available at [the pinned v0.20.0 release](https://github.com/asciimoo/hister/tree/v0.20.0). The image includes the upstream license at `/usr/share/licenses/hister/LICENSE` and the packaging license at `/usr/share/licenses/bottled-hister/LICENSE`. Dependencies in the upstream image retain their respective licenses, including yt-dlp's upstream notices.
