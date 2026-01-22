# Projektförslag - DevSecOps Kurs

Nedan är förslag på "lagom stora" projektidéer som passar exakt in i kursupplägget (repo → CI/CD → container registry → Kubernetes → security gates → monitoring/alerts → incident response). Alla kan starta med er Flask-demo och sedan få ett tydligt "case" som driver kraven i Fas 2–4.

## 1) NordTech Status & Incident Dashboard

**Idé:** En enkel webbapp som visar systemstatus, senaste deploy, och en "incident feed" (mockad).

**Varför bra:** Lätt att bygga, ger naturliga SLI/SLO (latency, error rate), och passar chaos/incident-demo.

### Funktioner

- `/` visar version, miljö, "build id"
- `/health` + `/ready` (readiness) + `/metrics` (Prometheus)
- Endpoint som kan trigga fel (t.ex. `/?fail=1` eller `/chaos/cpu`) för incidentövningar

### Fas-koppling

- **Fas 2:** SBOM + dependency scan (Flask + ev. requests), Trivy gate
- **Fas 3:** Gatekeeper: non-root, limits, no latest, readOnlyRootFilesystem
- **Fas 4:** Alert på 5xx-rate och latency + runbook "App down / high error rate" + chaos-test

---

## 2) "Secure Notes" (minimal API + valfri UI)

**Idé:** Ett API för anteckningar med CRUD och enkel auth (t.ex. API-key i header).

**Varför bra:** Skapar tydliga säkerhetsfrågor (secrets, least privilege, scanning av dependencies).

### Funktioner

- `/notes` (GET/POST), `/notes/<id>` (GET/PUT/DELETE)
- API-key via Kubernetes Secret
- Rate limiting eller basic input validation (för att ha något att testa i CI)

### Fas-koppling

- **Fas 2:** dependency scanning (pip), SAST, secrets scanning i repo
- **Fas 3:** Policies för secrets, non-root, drop capabilities
- **Fas 4:** SLO på error rate + runbook "Auth failures / secret rotated"

---

## 3) "Order Processor" (Web + Worker) – microservices light

**Idé:** En liten front-API + en worker som behandlar jobb (kan vara en enkel queue via Redis eller bara "fake queue" med fil/SQLite om ni vill minimera).

**Varför bra:** Visar verklig DevOps/DevSecOps: flera images, flera deploys, mer policy- och monitor-nytta.

### Komponenter

- `api-service` (Flask)
- `worker-service` (Python script/Flask utan HTTP)
- Ev. Redis som tredje komponent (valfritt)

### Fas-koppling

- **Fas 2:** scanning av flera images + SBOM per komponent
- **Fas 3:** Gatekeeper policies per namespace + resurshantering
- **Fas 4:** SLIs för queue-lag/backlog + chaos-test: stoppa worker och visa alert/runbook

---

## 4) "Config Drift Detector" (SRE-fokuserat)

**Idé:** En app som läser konfig (env vars/configmap) och exponerar den. En "drift-simulator" ändrar config och ni upptäcker det via policy/monitoring.

**Varför bra:** Perfekt för shared responsibility model + drift/incident-fokus.

### Funktioner

- Exponera config hash/commit sha
- Larma om config ändras oväntat (eller om version mismatch mellan pods)

### Fas-koppling

- **Fas 3:** Gatekeeper för ConfigMap/Secret usage, forbid inline secrets
- **Fas 4:** Runbooks för "config drift", post-mortem på felaktig config

---

## 5) "File Upload Scanner" (security-first)

**Idé:** Minimal upload-endpoint som "skannar" filer (mock eller ClamAV/Trivy som bonus).

**Varför bra:** Säkerhetskontroller blir naturliga: SAST, dependency, container scan, runtime rules (Falco).

### Funktioner

- `/upload` (POST) lagrar temporärt
- Policy: begränsa filstorlek/typ
- Simulerad sårbarhet för att visa pipeline FAIL (t.ex. medvetet osäker dependency i en branch)

### Fas-koppling

- **Fas 2:** Trivy + dependency gate blir tydligt motiverad
- **Fas 4:** Alert på ovanligt många uploads / CPU spike + chaos-test

---

## Rekommenderad nivå för kursen (för att hinna vecka 2–11)

Om ni vill maximera chans till VG utan att riskera komplexitet:

**Bäst balans:** (1) Status & Incident Dashboard eller (2) Secure Notes

**Om ni vill sticka ut:** (3) Order Processor (men kräver mer disciplin i teamet)

---

## Förslag på fördelning i teamet (4–5 personer)

- **Person A:** GitHub repo, branch protection, Actions baseline (Fas 1)
- **Person B:** Docker + registry + Cosign/SBOM (Fas 1–2)
- **Person C:** Security scans (Trivy, dependency, SAST), gates (Fas 2)
- **Person D:** K8s manifests + Gatekeeper policies (Fas 3)
- **Person E (om 5 pers):** Monitoring/alerting + runbooks/post-mortem (Fas 4–5)

---

## "VG-vänliga" OPA Gatekeeper policies (minst 5)

1. Blockera `:latest`
2. Kräv `runAsNonRoot: true`
3. Kräv resource requests/limits
4. Blockera `privileged`/`hostPath`/`hostNetwork`
5. Kräv `readOnlyRootFilesystem: true`

**Plus:** require image signature/attestations om ni vill avancera
