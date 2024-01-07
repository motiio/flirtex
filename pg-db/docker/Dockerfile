FROM postgres:16-bullseye

LABEL maintainer="PostGIS Project - https://postgis.net" \
      org.opencontainers.image.description="PostGIS 3.4.1+dfsg-1.pgdg110+1 spatial database extension with PostgreSQL 16 bullseye" \
      org.opencontainers.image.source="https://github.com/postgis/docker-postgis"

ENV POSTGIS_MAJOR 3
ENV POSTGIS_VERSION 3.4.1+dfsg-1.pgdg110+1

RUN apt-get update \
      && apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
      && apt-get install -y --no-install-recommends \
           # ca-certificates: for accessing remote raster files;
           #   fix: https://github.com/postgis/docker-postgis/issues/307
           ca-certificates \
           \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts \
      && rm -rf /var/lib/apt/lists/*

COPY ../init/conf/pg_hba.conf /

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ../init/sh/initdb-postgis.sh /docker-entrypoint-initdb.d/10_postgis.sh

COPY ../init/sh/copy-pg-hba.sh /docker-entrypoint-initdb.d/11_pg_hba.sh
COPY ../init/sh/initdb-schemas.sh /docker-entrypoint-initdb.d/12_initdb-schemas.sh

COPY ../init/sh/update-postgis.sh /usr/local/bin

