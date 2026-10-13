# Verification

## Container smoke test

```sh
docker build -t bottled-hister:test .
python3 tests/smoke.py
```

The smoke test runs under the manifest's 512 MiB memory limit and one-CPU allocation. It verifies startup, the generated HTTPS and WebSocket URLs, single-user mode, document ingestion, full-text search, readable previews, and data surviving container replacement. Test containers and volumes are removed on completion or failure. Set `CONTAINER_ENGINE=podman` to use Podman instead of Docker.

GitHub Actions runs the same test on pushes and pull requests. The [verified CI run](https://github.com/cloud-in-a-bottle/bottled-hister/actions/runs/38432835235) passed on Linux amd64. The pinned upstream image index also contains Linux arm64, but the live tests below were run on amd64.

## Live Cloud in a Bottle test

Verified on 2026-10-13 using a freshly provisioned Hetzner instance running Cloud in a Bottle commit `6ea27634` and Hister v0.20.0. Verification used Playwright with the real upstream Chrome extension v0.31.0 built from the Hister v0.20.0 tag.

- The platform built and launched the package through its normal app-deployment API.
- The signed-in owner opened the web search UI without a Hister login or signup flow.
- Guests could not access the UI, configuration, browsing history, search API, or MCP. The health endpoint remained available.
- The upstream browser extension authenticated using platform session cookies.
- The extension also indexed a newly visited page using a custom platform-token Authorization header, with all browser cookies cleared. The resulting document appeared in the web search UI.
- MCP search returned the indexed document using platform bearer authentication.
- The indexed document survived platform rebuild/reload, with a different container ID confirming replacement.
- After the packaging repository became public, a second app deployed by cloning its public GitHub URL without GitHub credentials or a pre-uploaded checkout. Deploying as `hister-public` generated the correct app-specific HTTPS URL.

Measured memory after the live search and reload tests was approximately 11 MiB at idle for the small fixture index. The 512 MiB allocation also passed the CI indexing and persistence test; larger collections and optional embedding workloads may need a higher allocation.

The temporary test instance was torn down after verification. No personal instance was modified.

## Signed-in Chrome extension regression

The first live verification cleared browser cookies before testing the Authorization header. It missed the mixed-credential case where the owner is still signed in and the extension also sends a valid API bearer token.

On 2026-10-13, the official Chrome Web Store extension v0.31.0 reproduced failed uploads on a deployed router based on commit `367a5eaf`. The popup saved the correct server URL, but a newly visited fixture page was not indexed. The router's cookie-first owner-auth check rejected the extension POST despite its valid API token.

After applying the narrowly scoped auth backport `b04f9dbb`, the same browser test passed with the login cookie still present: the popup saved the server URL, the extension submitted a successful POST returning 201, and the newly visited page was indexed. The fixture document and temporary test session were removed afterward.

HTTP/WebSocket regression coverage checks valid, expired and absent cookies, along with invalid, expired and app-only bearer credentials. Extension validation should always include both a signed-in browser and the configured custom Authorization header.
