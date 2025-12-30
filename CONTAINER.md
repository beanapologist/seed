# Container Registry Support

The Universal Binary Golden Seed is available as an OCI container image via GitHub Container Registry (GHCR).

## Quick Start

### Pull the Image
```bash
docker pull ghcr.io/beanapologist/seed:latest
docker pull ghcr.io/beanapologist/seed:v1.0.0
```

### Run the Container
```bash
# Interactive shell to explore seed files
docker run -it --rm ghcr.io/beanapologist/seed:latest sh

# Copy seed files to host
docker run --rm -v $(pwd):/output ghcr.io/beanapologist/seed:latest \
  cp /golden_seed_16.bin /output/

# Mount and use in another container
docker run -v seed-data:/data ghcr.io/beanapologist/seed:latest
docker run -v seed-data:/seed myapp:latest
```

## Available Tags

| Tag | Description |
|-----|-------------|
| `latest` | Latest release (always points to main branch) |
| `v1.0.0` | Semantic version tag (corresponds to GitHub releases) |
| `main` | Latest from main branch |
| `sha-<hash>` | Specific commit SHA |

## Image Contents

### Seed Files Locations

Files are available at two standard locations:

**Root directory** (minimal image size):
```
/golden_seed_16.bin
/golden_seed_32.bin
/golden_seed.hex
```

**Standard location** (all formats):
```
/usr/local/share/golden_seed/
├── golden_seed_16.bin
├── golden_seed_32.bin
├── golden_seed_16_be.bin
├── golden_seed_32_be.bin
├── golden_seed.hex
├── golden_seed_16.json
├── golden_seed_32.json
├── golden_seed_16.b64
└── golden_seed_32.b64
```

### Environment Variables

```bash
GOLDEN_SEED_HOME="/usr/local/share/golden_seed"
GOLDEN_SEED_16="/usr/local/share/golden_seed/golden_seed_16.bin"
GOLDEN_SEED_32="/usr/local/share/golden_seed/golden_seed_32.bin"
```

## Use Cases

### 1. Consensus Application
```dockerfile
FROM ghcr.io/beanapologist/seed:latest as seed
FROM myapp:latest

COPY --from=seed /golden_seed_32.bin /app/seed/golden_seed_32.bin
```

### 2. Multi-Stage Build
```dockerfile
FROM ghcr.io/beanapologist/seed:v1.0.0 as seed-provider
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y my-consensus-tool
COPY --from=seed-provider /usr/local/share/golden_seed /opt/seed

ENTRYPOINT ["my-consensus-tool", "--seed", "/opt/seed/golden_seed_32.bin"]
```

### 3. Volume Mount
```bash
docker run \
  -v seed-volume:/seed:ro \
  -e SEED_PATH=/seed/golden_seed_16.bin \
  myapp:latest
```

### 4. Kubernetes InitContainer
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: consensus-node
spec:
  initContainers:
    - name: seed-loader
      image: ghcr.io/beanapologist/seed:v1.0.0
      command: ['cp', '-r', '/usr/local/share/golden_seed', '/seed']
      volumeMounts:
        - name: seed-storage
          mountPath: /seed
  containers:
    - name: consensus
      image: consensus-node:latest
      volumeMounts:
        - name: seed-storage
          mountPath: /mnt/seed
          readOnly: true
      env:
        - name: GOLDEN_SEED_PATH
          value: /mnt/seed/golden_seed_16.bin
  volumes:
    - name: seed-storage
      emptyDir: {}
```

## Image Specifications

### Architecture Support
- `linux/amd64` - x86-64 systems
- `linux/arm64` - ARM64 systems (Raspberry Pi 4+, Apple Silicon)
- `linux/arm/v7` - 32-bit ARM systems

### Image Details
```
Base Image: scratch (minimal)
Size: ~600 bytes (binary seed files only)
OS: None (scratch image, data only)
Architecture: Multi-platform builds
```

### OCI Compliance
The image includes standard OCI labels:
- `org.opencontainers.image.title`
- `org.opencontainers.image.description`
- `org.opencontainers.image.version`
- `org.opencontainers.image.source`
- `org.opencontainers.image.url`

## Security

### Image Scanning
The container is automatically scanned for vulnerabilities:
- SBOM (Software Bill of Materials) generated for each build
- Only contains seed files - no dependencies or executables
- Minimal attack surface (scratch base image)

### Verification
```bash
# Verify image contents
docker inspect ghcr.io/beanapologist/seed:v1.0.0

# Check labels
docker inspect ghcr.io/beanapologist/seed:v1.0.0 | jq '.[0].Config.Labels'

# Verify file checksums
docker run --rm ghcr.io/beanapologist/seed:v1.0.0 \
  sha256sum /golden_seed_16.bin
# Should output: 87f829d95b15b08db9e5d84ff06665d077b267cfc39a5fa13a9e002b3e4239c5
```

## Build Locally

### Building the Image
```bash
docker build -t golden-seed:local .
```

### Building for Multiple Platforms
```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t golden-seed:latest \
  .
```

### Build Arguments (if needed)
Currently, the Dockerfile doesn't require build arguments. All seed files are copied from the repository.

## CI/CD Integration

The container is automatically built and pushed on:
- **Push to main branch**: Tagged as `latest`
- **Release tags (v*)**: Pushed with semantic version tag
- **Pull requests**: Built but not pushed (testing only)

### GitHub Actions Workflow
See `.github/workflows/build-container.yml` for the complete build workflow.

## Accessing Private Images (if needed)

For private use, authenticate with GitHub:
```bash
# Using personal access token
docker login ghcr.io -u USERNAME -p TOKEN

# Using GitHub CLI
gh auth token | docker login ghcr.io -u USERNAME --password-stdin
```

## Troubleshooting

### Image Pull Fails
```bash
# Ensure you're logged in
docker login ghcr.io

# Check image availability
docker image ls | grep ghcr.io

# Pull with verbose output
docker pull --verbose ghcr.io/beanapologist/seed:latest
```

### Wrong Architecture
```bash
# Check your system architecture
uname -m
docker version | grep -i architecture

# Pull specific architecture
docker pull --platform linux/arm64 ghcr.io/beanapologist/seed:latest
```

### File Not Found in Container
```bash
# Inspect container structure
docker run --rm ghcr.io/beanapologist/seed:latest ls -la /
docker run --rm ghcr.io/beanapologist/seed:latest ls -la /usr/local/share/golden_seed
```

## Related Documentation

- [FORMATS.md](FORMATS.md) - All available seed formats
- [golden_seed_README.md](golden_seed_README.md) - Seed specification
- [SECURITY.md](SECURITY.md) - Security policy
- [GitHub Container Registry Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

## License

The container image is provided under the same license as the main repository.

---

**Last Updated**: December 30, 2025  
**Supported Platforms**: linux/amd64, linux/arm64, linux/arm/v7  
**Base Image**: scratch (minimal)  
**Registry**: ghcr.io/beanapologist/seed
