FROM node:24-bookworm-slim@sha256:dc26ae92c9fb15cf6b1d63e20f0944b2efe0f115b20e00be48fb23fceb061c54 AS installer

WORKDIR /juice-shop
COPY . /juice-shop

RUN npm install --global typescript@6.0.3 @cyclonedx/cyclonedx-npm@4.2.1 \
    && npm install --omit=dev \
    && npm dedupe --omit=dev \
    && npm run sbom \
    && rm -rf frontend/node_modules frontend/.angular frontend/src/assets \
    && mkdir -p logs \
    && chown -R 65532:0 logs \
    && chgrp -R 0 ftp/ frontend/dist/ logs/ data/ i18n/ \
    && chmod -R g=u ftp/ frontend/dist/ logs/ data/ i18n/ \
    && rm -f ftp/legal.md i18n/*.json \
    && npm cache clean --force

FROM gcr.io/distroless/nodejs24-debian13:latest@sha256:24bc0fe0225c7518f202a822587dad74fe143b96326b81fe5cc08c1df8bed03e

ARG BUILD_DATE
ARG VCS_REF
ARG VCS_URL
LABEL org.opencontainers.image.title="OWASP Juice Shop — hardened interview target" \
      org.opencontainers.image.description="Intentionally vulnerable training application; not for production or public exposure" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source=$VCS_URL \
      org.opencontainers.image.revision=$VCS_REF \
      org.opencontainers.image.created=$BUILD_DATE

ENV NODE_ENV=production
WORKDIR /juice-shop
COPY --from=installer /juice-shop /juice-shop
USER 65532:0
EXPOSE 3000
CMD ["/juice-shop/build/app.js"]
