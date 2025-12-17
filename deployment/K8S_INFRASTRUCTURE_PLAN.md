# Kubernetes Infrastructure Plan

**Simple Eiffel CI/CD and Dogfooding Strategy**

*Created: December 17, 2025*
*Status: PLANNING*

---

## Executive Summary

This document outlines the infrastructure strategy for deploying a Kubernetes cluster to dogfood `simple_k8s` and establish a CI/CD pipeline for the Simple Eiffel ecosystem. The goal is to prove the library works in production while solving the real problem of automated testing for 71+ libraries.

---

## Dogfooding Objective

**Primary Target**: Self-hosted CI/CD pipeline that uses Simple Eiffel libraries to build and test Simple Eiffel libraries.

```
┌─────────────────────────────────────────────────────────┐
│                   K8s Cluster                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Build Pod   │  │ Build Pod   │  │ Build Pod   │     │
│  │ (lib batch) │  │ (lib batch) │  │ (lib batch) │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │               │               │               │
│         └───────────────┼───────────────┘               │
│                         ▼                               │
│              ┌─────────────────────┐                    │
│              │  Coordinator Pod    │                    │
│              │  (simple_ci + k8s)  │                    │
│              └──────────┬──────────┘                    │
│                         │                               │
└─────────────────────────┼───────────────────────────────┘
                          ▼
               ┌─────────────────────┐
               │   simple_oracle     │
               │   (results DB)      │
               └─────────────────────┘
```

### Value Proposition

| Benefit | Description |
|---------|-------------|
| **Proves simple_k8s** | Real orchestration workload |
| **Proves simple_docker** | Real container builds |
| **Proves simple_ci** | Real pipeline coordination |
| **Solves real problem** | Currently no automated CI for 71 libs |
| **Visible credibility** | "Built with Simple Eiffel" badge |

### Secondary Target

Deploy a **simple_web showcase application** demonstrating the full stack:
- `simple_web` - HTTP server
- `simple_docker` - Containerized
- `simple_k8s` - Deployed with blue/green or canary
- `simple_telemetry` - Metrics collection

Candidate: **simple_pkg web registry** - search/browse packages online.

---

## Kubernetes Distribution: K3s vs K8s

### Comparison

| Aspect | K8s (full) | K3s |
|--------|-----------|-----|
| **What** | Full Kubernetes | Certified Kubernetes, stripped down |
| **Binary size** | 1GB+ | ~50MB single binary |
| **RAM overhead** | 2-4GB | 512MB-1GB |
| **Made by** | CNCF/Google | Rancher Labs |
| **API** | Standard | Identical - 100% compatible |
| **Use case** | Cloud/enterprise | Edge, IoT, dev, home labs |

### Recommendation

**K3s** for home/dedicated hardware - same API, less overhead.

**Docker Desktop Kubernetes** for initial development on Windows.

Both use identical REST API endpoints, so `simple_k8s` code works on either:

```eiffel
-- Works identically on K8s or K3s
create k8s.make_with_kubeconfig
k8s.list_pods ("default")
k8s.create_deployment (spec, "production")
```

---

## Hosting Options Analysis

### Option 1: Local Development (Phase 1 - Immediate)

**Docker Desktop Kubernetes** on Windows development machine.

| Aspect | Detail |
|--------|--------|
| **Cost** | Free |
| **Setup** | Settings → Kubernetes → Enable |
| **Performance** | Good (shares host resources) |
| **Availability** | Only when dev machine is on |
| **Use case** | Prove simple_k8s works |

**Enable:**
```bash
# In Docker Desktop: Settings → Kubernetes → Enable Kubernetes
kubectl get nodes  # Verify
```

### Option 2: Mac Mini M4 (Arriving Friday)

Use new Mac Mini as K3s host.

| Aspect | Detail |
|--------|--------|
| **Cost** | Already purchased |
| **Performance** | Excellent (M-series ARM) |
| **RAM** | 16-24GB (depending on config) |
| **Availability** | When not used for development |
| **Pros** | Powerful, low power, silent |
| **Cons** | Shared with dev work |

**Setup:**
```bash
# On Mac Mini
curl -sfL https://get.k3s.io | sh -
sudo kubectl get nodes
```

### Option 3: Dedicated Mini PC (Recommended for 24/7)

**Intel N100 Mini PC** - always-on CI infrastructure.

#### Hardware Recommendation

**Beelink Mini S12 Pro** - [Amazon Link](https://www.amazon.com/Beelink-Mini-S12-Pro-PC/dp/B0B818MRR5)

| Spec | Detail |
|------|--------|
| **CPU** | Intel N100 (4 cores, up to 3.4GHz, 12th Gen) |
| **RAM** | 16GB DDR4 3200MHz |
| **Storage** | 500GB NVMe SSD (upgradeable to 2TB) |
| **Network** | Gigabit Ethernet, WiFi 6 |
| **Display** | Dual HDMI 4K@60Hz |
| **Power** | ~10W typical, <25W max |
| **Size** | 4.5" x 4" x 1.5" |
| **Price** | ~$200-220 |

#### Why N100 Over Raspberry Pi

| Factor | N100 Mini PC | Raspberry Pi 5 (8GB) |
|--------|--------------|---------------------|
| **RAM** | 16GB | 8GB max |
| **Architecture** | x86_64 | ARM64 |
| **EiffelStudio** | Native, fast | Works, slower |
| **Price (ready)** | ~$200 | ~$150 (with accessories) |
| **K3s overhead** | Comfortable | Tight |
| **Reliability** | SSD, proven | SD card wear concerns |

#### Alternative N100 Options

| Model | Specs | Price |
|-------|-------|-------|
| Beelink Mini S12 Pro | N100, 16GB, 500GB | ~$210 |
| GMKtec G3 | N100, 16GB, 512GB | ~$200 |
| Trigkey G4 | N100, 16GB, 500GB | ~$190 |
| Beelink S12 Pro 1TB | N100, 16GB, 1TB | ~$240 |

### Option 4: Oracle Cloud Free Tier

Genuinely free forever cloud hosting.

| Spec | Detail |
|------|--------|
| **CPU** | 4 ARM Ampere cores |
| **RAM** | 24GB |
| **Storage** | 200GB |
| **Network** | 10TB/month egress |
| **Cost** | Free (forever) |
| **Availability** | 24/7 |

**Pros:** Production-like, no hardware to manage, accessible from anywhere.
**Cons:** ARM architecture (EiffelStudio works but cross-compile considerations).

### Option 5: Paid VPS (If Needed)

| Provider | Specs | Cost |
|----------|-------|------|
| Hetzner | 4 vCPU, 8GB RAM | ~€7/mo |
| DigitalOcean | 2 vCPU, 4GB RAM | $24/mo |
| Linode | 2 vCPU, 4GB RAM | $24/mo |

---

## Network Considerations

### Home Network Assets

- **Fiber Internet**: High bandwidth, low latency
- **Static IP or DDNS**: Required for external webhook access
- **Port Forwarding**: 6443 (K8s API), 80/443 (ingress)

### Security

| Concern | Mitigation |
|---------|------------|
| **Exposed K8s API** | Use kubeconfig with client certs, not public |
| **Webhook access** | GitHub webhook → home IP (or use tunnel) |
| **Firewall** | Only expose necessary ports |

### Alternative: Cloudflare Tunnel

Avoid port forwarding entirely:
```bash
cloudflared tunnel --url http://localhost:6443
```

---

## Recommended Phased Approach

### Phase 1: Prove simple_k8s (Now)

**Target:** Docker Desktop Kubernetes on Windows

**Goal:** Verify simple_k8s library works correctly

**Tasks:**
1. Enable Kubernetes in Docker Desktop
2. Build simple_k8s library
3. Run test suite against local cluster
4. Validate pod/deployment/service operations

### Phase 2: Local CI/CD (Post simple_k8s MVP)

**Target:** Mac Mini or N100 Mini PC

**Goal:** Automated nightly builds of all 71 libraries

**Tasks:**
1. Install K3s on dedicated hardware
2. Build EiffelStudio container image
3. Deploy coordinator pod (simple_ci)
4. Parallel build pods for library batches
5. Results → simple_oracle

### Phase 3: Production Deployment (Showcase)

**Target:** Same cluster or Oracle Cloud

**Goal:** Deploy simple_pkg web registry

**Tasks:**
1. Build simple_web application container
2. Deploy with blue/green strategy
3. Expose via ingress
4. Monitor with simple_telemetry

---

## Hardware Decision Matrix

| Scenario | Recommendation | Cost |
|----------|---------------|------|
| **Just prove simple_k8s works** | Docker Desktop | Free |
| **Occasional CI, shared machine** | Mac Mini with K3s | Already owned |
| **24/7 dedicated CI** | N100 Mini PC | ~$200 |
| **Production-like, cloud** | Oracle Cloud Free | Free |

### Larry's Situation

| Asset | Status |
|-------|--------|
| Windows dev machine | Available now |
| Mac Mini M4 | Arriving Friday |
| Fiber internet | High bandwidth available |
| Raspberry Pi (older) | Not recommended for this workload |

**Recommended Path:**

```
Now:     Docker Desktop K8s (prove simple_k8s works)
           ↓
Friday:  Mac Mini K3s (more power, still dev machine)
           ↓
Later:   N100 Mini PC (if 24/7 dedicated CI needed)
           or
         Oracle Cloud Free Tier (if prefer cloud)
```

---

## Bill of Materials (If Purchasing Dedicated Hardware)

### Minimal Setup: Beelink Mini S12 Pro

| Item | Source | Price |
|------|--------|-------|
| Beelink Mini S12 Pro (N100/16GB/500GB) | [Amazon](https://www.amazon.com/Beelink-Mini-S12-Pro-PC/dp/B0B818MRR5) | ~$210 |
| Ethernet cable (Cat6) | Amazon | ~$8 |
| **Total** | | **~$220** |

Power supply and HDMI included with unit. Keyboard/mouse/monitor only needed for initial setup, then headless via SSH.

### Optional Additions

| Item | Purpose | Price |
|------|---------|-------|
| USB-C SSD (1-2TB) | Backup storage | $80-150 |
| UPS (small) | Power protection | $50-80 |
| VESA mount | Behind monitor | Included |

---

## K3s Installation Reference

### On Ubuntu/Debian (N100 or Mac Mini)

```bash
# Install K3s (single node)
curl -sfL https://get.k3s.io | sh -

# Verify
sudo kubectl get nodes

# Get kubeconfig for remote access
sudo cat /etc/rancher/k3s/k3s.yaml
```

### On macOS (Mac Mini)

```bash
# Option 1: K3s via Multipass
brew install multipass
multipass launch --name k3s --memory 8G --disk 40G
multipass exec k3s -- bash -c "curl -sfL https://get.k3s.io | sh -"

# Option 2: K3s via Lima
brew install lima
limactl start --name=k3s template://k3s
```

### Remote Access Setup

```bash
# Copy kubeconfig to dev machine
scp user@k3s-host:/etc/rancher/k3s/k3s.yaml ~/.kube/config

# Edit server address in config
# Change: server: https://127.0.0.1:6443
# To:     server: https://<k3s-host-ip>:6443
```

---

## Success Criteria

| Milestone | Metric |
|-----------|--------|
| **simple_k8s MVP** | 44+ tests passing on Docker Desktop |
| **CI Pipeline MVP** | 5 libraries compiled in parallel pods |
| **Full CI** | All 71 libraries nightly build |
| **Showcase App** | simple_pkg registry deployed and accessible |
| **Self-Hosting Badge** | "Built and tested with Simple Eiffel on K8s" |

---

## Conclusion

The recommended approach is:

1. **Immediate**: Use Docker Desktop Kubernetes to develop and test simple_k8s
2. **Short-term**: Use Mac Mini M4 with K3s for more powerful local testing
3. **Medium-term**: Consider dedicated N100 Mini PC (~$200) if 24/7 CI is valuable
4. **Alternative**: Oracle Cloud Free Tier for cloud-based approach

The fiber internet connection makes home hosting viable. The Raspberry Pi is not recommended due to insufficient resources for EiffelStudio compilation workloads.

---

## References

- [K3s Documentation](https://docs.k3s.io/)
- [simple_k8s VISION](/d/prod/reference_docs/designs/SIMPLE_K8S_VISION.md)
- [simple_k8s Implementation Plan](/d/prod/reference_docs/plans/SIMPLE_K8S_IMPLEMENTATION_PLAN.md)
- [Beelink Mini S12 Pro - Amazon](https://www.amazon.com/Beelink-Mini-S12-Pro-PC/dp/B0B818MRR5)
- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
