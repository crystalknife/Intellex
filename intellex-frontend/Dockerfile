# Intellex Frontend
#
# Three stages: install deps, build, then a lean runtime that only
# copies the standalone server + static assets Next.js traces
# automatically -- never the full node_modules tree.

FROM node:22-slim AS deps
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci


FROM node:22-slim AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY frontend ./

# NEXT_PUBLIC_* variables are inlined into the client bundle at build
# time, not read at container runtime -- so this has to be a build ARG,
# not a docker-compose `environment:` entry. It must be the URL the
# *browser* can reach (e.g. http://localhost:8000 for local Compose, or
# your real public backend URL in any actual deployment) -- never the
# internal Docker service hostname, which only resolves inside the
# Docker network and means nothing to a browser on the host/internet.
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build


FROM node:22-slim AS runner
WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
