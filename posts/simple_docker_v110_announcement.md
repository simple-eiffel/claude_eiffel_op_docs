# Announcing simple_docker v1.1.0 — Docker Container Management for Eiffel

**December 15, 2025**

We're excited to announce **simple_docker**, a new addition to the Simple Eiffel ecosystem that brings programmatic Docker container management to Eiffel applications.

## What is simple_docker?

simple_docker enables Eiffel developers to build, run, and manage Docker containers directly from Eiffel code—no shell commands required. It communicates with the Docker Engine API through Windows named pipes, providing full Design by Contract guarantees.

```eiffel
create client.make

if client.ping then
    create spec.make ("alpine:latest")
    spec.set_name ("my-app")
        .add_port (80, 8080)
        .add_env ("DEBUG", "true")
        .set_memory_limit (512 * 1024 * 1024)
        .set_restart_policy ("unless-stopped").do_nothing

    if attached client.run_container (spec) as c then
        print ("Container running: " + c.short_id + "%N")
    end
end
```

## Features

| Category | Capabilities |
|----------|--------------|
| **Containers** | Create, start, stop, pause, restart, kill, remove, logs, wait, exec |
| **Images** | List, pull, inspect, exists, remove |
| **Networks** | Create, list, connect, disconnect, remove, prune |
| **Volumes** | Create, list, remove with driver configuration |
| **Dockerfile Builder** | Fluent API for generating Dockerfiles with multi-stage support |

## Technical Highlights

- **4,291 lines** of Eiffel source code across 9 classes
- **38 tests passing** including 10 "cookbook verification" tests that dogfood our documentation examples
- **Resilient IPC** with rescue/retry logic—automatically retries on transient connection failures
- **Strong contracts** with preconditions, postconditions, and invariants on all operations
- **IUARC 5-document standard** documentation (Overview, User Guide, API Reference, Architecture, Cookbook)

## API Classes

| Class | Purpose |
|-------|---------|
| `DOCKER_CLIENT` | Main facade for all Docker operations |
| `DOCKER_CONTAINER` | Container representation with state tracking |
| `DOCKER_IMAGE` | Image representation with tags and metadata |
| `DOCKER_NETWORK` | Network operations and queries |
| `DOCKER_VOLUME` | Volume management with driver support |
| `CONTAINER_SPEC` | Fluent builder for container configuration |
| `DOCKERFILE_BUILDER` | Programmatic Dockerfile generation |
| `CONTAINER_STATE` | State constants and transition queries |
| `DOCKER_ERROR` | Error classification with retry detection |

## Example: Multi-stage Dockerfile Generation

```eiffel
create builder.make_multi_stage

builder.from_image_as ("golang:1.21", "builder")
    .run ("go build -o /app main.go")
    .new_stage
    .from_image ("alpine:latest")
    .copy_from ("builder", "/app", "/app")
    .expose (8080)
    .cmd (<<"./app">>).do_nothing

print (builder.build)
-- Outputs valid multi-stage Dockerfile
```

## Dependencies

- **simple_ipc** (v2.0.0+) — Named pipe communication
- **simple_json** — JSON parsing
- **simple_file** — File operations
- **simple_logger** — Logging support

## Getting Started

```bash
# Clone
git clone https://github.com/simple-eiffel/simple_docker.git

# Set environment
export SIMPLE_DOCKER=/path/to/simple_docker

# Add to your ECF
<library name="simple_docker" location="$SIMPLE_DOCKER/simple_docker.ecf"/>
```

---

## Progress & Roadmap

### Completed (v1.0 - v1.1)

| Phase | Feature | Status |
|-------|---------|--------|
| **P1** | Core container operations (create, start, stop, remove, logs) | Done |
| **P1** | Image management (list, pull, exists, remove) | Done |
| **P1** | Fluent builder API (`CONTAINER_SPEC`) | Done |
| **P1** | Error handling with `DOCKER_ERROR` | Done |
| **P2** | `DOCKERFILE_BUILDER` - Fluent Dockerfile generation | Done |
| **P2** | `DOCKER_NETWORK` - Network operations | Done |
| **P2** | `DOCKER_VOLUME` - Volume operations | Done |
| **P2** | Exec operations in containers | Done |
| **P2** | Resilient IPC with rescue/retry | Done |
| **P4** | IUARC 5-document standard documentation | Done |
| **P5** | 38 tests including cookbook verification | Done |

### Tomorrow: Phase 3 - Performance Optimization

| Task | Description |
|------|-------------|
| Streaming log support | Real-time log streaming instead of batch fetch |
| Connection pooling | Reuse IPC connections across operations |
| Timeout handling | Configurable timeouts for long-running operations |
| Efficient tar context | Optimize `build_image` with simple_archive |

### Coming Soon: Phase 6 - Production Hardening

| Feature | Description |
|---------|-------------|
| `COMPOSE_BUILDER` | Fluent API for docker-compose.yaml generation |
| `DOCKER_REGISTRY_AUTH` | Private registry authentication |
| `EIFFEL_CONTAINER_TEMPLATES` | Pre-built templates for Eiffel apps |
| Unix socket support | Linux/macOS via simple_ipc cross-platform |
| Image building | `build_image` with tar context from simple_archive |

### Finish Line Criteria

| Metric | Target | Current |
|--------|--------|---------|
| Test coverage | 50+ tests | 38 |
| All P1-P6 features | Complete | P1-P2, P4-P5 Done |
| Cross-platform | Windows + Linux | Windows Done |
| Documentation | IUARC 5-doc | Done |
| Production apps | 1+ real deployment | Pending |

---

## Links

- **GitHub**: https://github.com/simple-eiffel/simple_docker
- **Documentation**: https://simple-eiffel.github.io/simple_docker/
- **Ecosystem**: https://github.com/simple-eiffel (71 libraries)

---

simple_docker is part of the **Simple Eiffel** ecosystem—a collection of 71 libraries bringing modern development capabilities to Eiffel with Design by Contract at the core.

*Built with Claude Code*

---

Want to get involved? Check out the [GitHub repo](https://github.com/simple-eiffel/simple_docker) or reach out to discuss use cases!
