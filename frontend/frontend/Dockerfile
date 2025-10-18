# syntax=docker/dockerfile:1

# Build stage
FROM node:18-alpine AS builder
WORKDIR /app

# Configure backend URL at build time for Next.js rewrites
ARG BACKEND_URL="http://api:8000"
ENV BACKEND_URL=${BACKEND_URL}

# Install bun (optional if using bun locally)
RUN apk add --no-cache curl bash && \
    curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

# Install dependencies
COPY package.json bun.lock* package-lock.json* ./
RUN if [ -f bun.lock ]; then bun install; else npm ci; fi

# Copy source
COPY . .

# Build
RUN bun run build || npm run build

# Production stage
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NODE_OPTIONS=--dns-result-order=ipv4first
# Add non-root user
RUN addgroup -S nextjs && adduser -S nextjs -G nextjs

# Copy built app
COPY --from=builder /app/package.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

# Expose port
EXPOSE 3000

# Start Next.js
CMD ["node", "./node_modules/next/dist/bin/next", "start", "-p", "3000", "-H", "0.0.0.0"]