# Universal Binary Golden Seed - Container Image
# Provides language-agnostic access to the golden seed in containerized environments

FROM alpine:3.23 AS builder
WORKDIR /build
COPY golden_seed_16.bin golden_seed_32.bin golden_seed.hex ./
RUN ls -lh

FROM scratch
# Seed files in root
COPY --from=builder /build/golden_seed_16.bin /golden_seed_16.bin
COPY --from=builder /build/golden_seed_32.bin /golden_seed_32.bin
COPY --from=builder /build/golden_seed.hex /golden_seed.hex

# Seed files in standard locations
COPY --from=builder /build/golden_seed_16.bin /usr/local/share/golden_seed/golden_seed_16.bin
COPY --from=builder /build/golden_seed_32.bin /usr/local/share/golden_seed/golden_seed_32.bin
COPY --from=builder /build/golden_seed.hex /usr/local/share/golden_seed/golden_seed.hex

# Include additional formats for accessibility
COPY golden_seed_16.json /usr/local/share/golden_seed/golden_seed_16.json
COPY golden_seed_32.json /usr/local/share/golden_seed/golden_seed_32.json
COPY golden_seed_16.b64 /usr/local/share/golden_seed/golden_seed_16.b64
COPY golden_seed_32.b64 /usr/local/share/golden_seed/golden_seed_32.b64
COPY golden_seed_16_be.bin /usr/local/share/golden_seed/golden_seed_16_be.bin
COPY golden_seed_32_be.bin /usr/local/share/golden_seed/golden_seed_32_be.bin

# Metadata labels
LABEL org.opencontainers.image.title="Golden Seed"
LABEL org.opencontainers.image.description="Universal Binary Golden Seed - Language-agnostic consensus seed (iφ)"
LABEL org.opencontainers.image.authors="beanapologist"
LABEL org.opencontainers.image.url="https://github.com/beanapologist/seed"
LABEL org.opencontainers.image.documentation="https://github.com/beanapologist/seed/blob/main/FORMATS.md"
LABEL org.opencontainers.image.source="https://github.com/beanapologist/seed"
LABEL org.opencontainers.image.version="1.0.0"

ENV GOLDEN_SEED_HOME="/usr/local/share/golden_seed"
ENV GOLDEN_SEED_16="${GOLDEN_SEED_HOME}/golden_seed_16.bin"
ENV GOLDEN_SEED_32="${GOLDEN_SEED_HOME}/golden_seed_32.bin"
