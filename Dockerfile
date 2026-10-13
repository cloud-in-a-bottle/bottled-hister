# Upstream v0.20.0-root, including amd64 and arm64 builds and yt-dlp.
# Root inside the rootless app container can write the platform-owned data mount.
FROM ghcr.io/asciimoo/hister:v0.20.0-root@sha256:6fd478c0950237a24a364da149d29b4af362429a575f640083127de41edaf4c9

LABEL org.opencontainers.image.title="Hister for Cloud in a Bottle" \
      org.opencontainers.image.source="https://github.com/cloud-in-a-bottle/bottled-hister" \
      org.opencontainers.image.licenses="AGPL-3.0-or-later AND MIT"

RUN mkdir -p /usr/share/licenses/hister \
    && wget -qO /usr/share/licenses/hister/LICENSE \
       https://raw.githubusercontent.com/asciimoo/hister/v0.20.0/LICENSE
COPY LICENSE /usr/share/licenses/bottled-hister/LICENSE
COPY entrypoint.sh /usr/local/bin/bottled-hister

ENTRYPOINT ["/bin/sh", "/usr/local/bin/bottled-hister"]
CMD ["listen"]
