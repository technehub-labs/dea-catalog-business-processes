# Changelog

All notable changes to this repository are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows
`docs/versioning.md`.

## [Unreleased]

### CR-BP-133: Change-Request Register Truth Pass

Mechanical register-integrity pass (the CR-BP-113 §e repair class): 3 surviving CR-BP-90 duplicate rows removed + 1 CR-BP-102 duplicate; BP-90 status corrected to Superseded (matching the file and the CR-BP-116 withdrawal); CR-BP-EXT-23 status corrected to Accepted (matching the file); 26 post-merge "(this PR)" markers flipped to Accepted; CR-BP-03/03C Status-line format normalized (colon variant was invisible to the open-change-requests counter, which conservatively counted both open — the count drops by 2 on regeneration). The un-landed 112/113/114 drafts from the October 13 handoff are confirmed never-in-repo (untracked-clone artifacts; removed locally). No entity, schema, gate, or CI changes.


### CR-BP-GS-1: Governance Sweep (GOV-002 Owner Ratification + GOV-003 Role-Based Derivation)

The GOV-002/GOV-003 governance sweep closing the completeness programme's final open items (the CE-RL carve-out population). GOV-002: one Process Owner role per domain (7 roles) covers all 194 L1 PGs + L2 BPs -- every owner block flips status proposed -> confirmed with provenance.type manual. GOV-003: the 145 BPs' actors/stakeholders are derived from each record's own parent cell charter vocabulary (charter-named roles only; the domain design authority fallback for architectural-vocabulary cells), with per-record refinement the standing review item. Post-sweep: gate [50] reports 0 blocking, 0 advisory across all 3,723 records -- the catalogue is 100% complete on its ratified profiles, ahead of the 2026-12-31 EXT-24 review window. Follow-up: reconcile the EXT-24 ownership register's awaiting_owner_confirmation dispositions to the confirmed roles. D-004 clean.

### CR-BP-CE-RL: Completeness Gate Posture Flip and Programme Closure

The final slice of the completeness programme. Gate [50] Completeness Profiles flips advisory -> BLOCKING in the conformance_result.py registry (--advisory -> --strict): the blocking profile is 0 across all 3,723 records, so CI now fails on newly introduced schema-profile defects (required fields emptied, prohibited fields added, non-vocabulary Task responsibilities) — the 43-blocking-defect class cannot re-enter silently. The 290 knowledge-dependent CE-L2-006 actors/stakeholders candidates remain advisory via the explicit time-bound carve-out pending the GOV-002/GOV-003 sweep (EXT-24 register review due 2026-12-31; the EXT-23 exception lifecycle applies if the window lapses). The S16 CR-number pattern is extended additively to admit the CE-RL / CE-REC-N tranche names. The MECE cross-level relationship validator remains a separate follow-on CR per the umbrella §4. D-004 clean.

### CR-BP-CE-REC-1: Umbrella CR Level-Numbering Reconciliation

Reconciles the umbrella CR-BP-CE-0 (re-landed in draft form by PR #205) to the canonical L0..L4 level model the gate and the landed tranches follow: draft L1 Process Context -> L0, L2 Process Group -> L1, L3 Business Process -> L2, L4 Activity/Task -> L3/L4; stale population counts (140/560/2,800) -> live (145/580/2,900); the stale catalog-conformance.yml workflow reference -> the actual conformance_result.py gate registry (gate [50]). No normative profile content changes; labels, internal rule references, and counts only. The §6 tranche sequence restated as the landed CRs with their PR numbers. D-004 clean.

### CR-BP-CE-L4: Custodian Vocabulary Normalization + the CE-L0-003 Repair

The Activity/Task-level tranche of the completeness programme (CR-BP-CE-0 §6). Normalizes the 580 intake-phase Task records' `responsibility` from `designated intake custodian` to the controlled-vocabulary `intake custodian` (580 CE-L4-002 resolved; the stray modifier traced to three generator sources, all corrected: decompose_l4.py, enrich_l4_governance_and_existence.py, enrich_l4_party_and_relationship.py). Repairs the one CE-L0-003 finding (pc-sd-improve-ft9k5f gains a third charter-derived scope.excludes entry). Post-tranche: gate [50] advisory 871 -> 290; the remaining findings are the deliberately-deferred CE-L2-006 actors/stakeholders candidates (the CR-BP-CE-RL input per §5/D-004). D-004 clean.

### CR-BP-CE-L1: Process Group Owner Candidates Tranche (the 49 L1 records)

The second level tranche of the completeness programme ratified under CR-BP-CE-0 §6. Lands the L1 adopted field `owner` on all 49 ProcessGroup records as status: proposed candidates per the §5 provenance policy: value `awaiting_owner_confirmation` mirroring the EXT-24 ownership register disposition (Process Domain Reviewer GOV-003 confirms; review due 2026-12-31); no owner name is invented. Additive schema extension: `process-group.schema.json` gains an OPTIONAL `owner` property (value/status/provenance/review_due/decision_right; status admits proposed -> confirmed, the transition being GOV-003's decision right). One-shot migration `scripts/remediate_ce_l1.py` retained as the governance record. Post-tranche: gate [50] CE-L1 profile at 0 findings (49 CE-L1-005 resolved); programme total 1,210 -> 1,161 advisory. No other field touched; the catalogue remains 3,723 records. D-004 clean.

### CR-BP-CE-L2: Business Process Adopted-Fields Tranche (the 145 L2 records)

The third level tranche of the completeness programme ratified under CR-BP-CE-0 §6. Lands `process_classification` (canonical block derived from each record's own legacy `process_type`; status active, type migration) resolving 145 CE-L2-002, and the EXT-24 ownership-register `owner` candidate (awaiting_owner_confirmation, status proposed, GOV-002 confirms) resolving 145 CE-L2-006. `actors`/`stakeholders` DEFERRED: no evidence-bound source exists and inventing values violates §5/D-004; the 290 findings remain the CR-BP-CE-RL input. Additive schema extensions to `entity.schema.json` (classification block gains optional status/provenance, retro-safe; owner becomes oneOf legacy-string | candidate block). Post-tranche: gate [50] CE-L2 580 -> 290; programme total 1,161 -> 920 advisory. The catalogue remains 3,723 records. D-004 clean.

### CR-BP-CE-L0: Process Context Completeness Tranche (the 8 escape-clause cells)

The first level tranche of the completeness programme ratified under CR-BP-CE-0 (§6, item 2). Lands the CE-L0 remediation: the 43 blocking findings on the 8 escape-clause ProcessContext records (42 CE-L0-001 required-field gaps on ao-activate, ao-retire, eo-activate, fa-activate, fa-retire, ge-retire, sd-activate, sd-retire + 1 CE-L0-006 prohibited `version` field on pc-sd-retire-zxnc3c, removed) plus the CE-L0-004 bidirectionality closure (reciprocal `adjacent_contexts` entries added to 22 same-domain sibling PCs). The canonical required fields (definition, scope, outcomes, adjacent_contexts, processes, status) are added at the top level, derived from each record's own authoritative cell_charter and process_context.scope_summary; no new semantic content is invented. CATALOG.yaml regenerated (the sd-retire PC index version normalizes 1.0.0 -> 0.0.0, consistent with the other 48 PCs). The check_cr_metadata.py CR-number pattern is extended additively to admit the CR-BP-CE-N / CR-BP-CE-LN tranche naming the umbrella CR ratified. Post-tranche: gate [50] CE-L0 profile at 0 blocking findings across all 49 ProcessContext records; 1,210 advisory findings unchanged (the CE-L1..L4 tranche target). No canonical record added or removed; the catalogue remains 3,723. D-004 clean.
### CR-BP-94-EXT-07: README Template Consolidation + Generator V2

Supersedes CR-BP-94-EXT-02's 13-section template. Consolidates 7-section T9.13 + 13-section EXT-02 + 6-section CR-BP-120 (user-attached) into 8-section L0 + 7-section L1-L4 template. New renderers: header-identity-table (CR-BP-120), governance-provenance (admission + change history), behavioral-boundaries (3-row In Scope / Out of Scope / Adjacent table with checkmark/x/link emojis), hierarchical-decomposition (`<details>` collapsible HTML), properties-relationships (full property + relationships tables per T9.13), operational-metrics (the new `metrics` block with KPI / KRI / KCI rendering; `(Pending EXT-04)` placeholder when absent), technical-metadata. Adds OPTIONAL `metrics` block (KPI/KRI/KCI) at L0. Adds `profile` field to `schemas/entities/process-group.schema.json` (the L1 pilot unblock that EXT-06 needs as a prerequisite). Fixes the section numbering skip (8 to 10). Regenerates 49 cell-roots + 3,674 records. Cross-repo cascade (T9.13b) is a follow-on programme. D-004 clean. 118a/118b/118c/123/124/125/126/127/128/129/130/131/132/EXT-02 authorship + entity-system gates remain CONFORMANT.

### CR-BP-132: dea:// Domain Tying Plan (T9.10; precursor; user-approved 2026-10-15)

T9.10 follow-on. The precursor to T9.2 IANA Submission, T9.4 IETF I-D, T9.8 Production Server, and T9.9 Sync Daemon. Per the user directive 2026-10-15, the URI references may be **privately tied to** `technehub-labs.github.io` or `technehub.com` domain. The 7-section plan: (1) domain selection; (2) authority model; (3) resolvable form; (4) access control (Interpretation A: brand/authority, public resolution is the default); (5) IANA registration impact; (6) per-repo domain configuration; (7) migration plan. The intent: the plan may be **replayed and revised later**; the changes should **align with the release assets** when the time comes (CHANGELOG, CATALOG, CITATION.cff, git tags, GitHub Releases, the IANA authority domain declaration). This CR is the formal record; the kanban card (T9.10) is the live status. No code changes; the implementation is in CR-BP-133 + CR-BP-134. D-004 clean. 118a/118b/118c/123/124/125/126/127/128/129/130/131 gates remain CONFORMANT.

### CR-BP-116: Release-History Reset (Path B) + Release-Discipline Extensions

Path B reset. Withdraws v0.1.0 + v0.3.0 GitHub Releases and tags; abandons v0.2.0 + v0.4.0 in CHANGELOG/CITATION only. Resets CITATION.cff to version 0.0.0. Replaces the "Pre-release history (now closed)" section in docs/versioning.md with a new "Release history" section. Adds 4 release-discipline extensions: A (pre-release CI verification contract: the proposed tag SHA must carry a fresh CI run with all 3 workflows SUCCESS); B (prior-cut history table: docs/versioning.md gains a numbered, append-only table that records date + cut CR + commit SHA + gate count + post-mortem link for every release tag ever cut; starts empty post-reset); D (GPG-signing procedure: the release-cut step names the active key fingerprint B2FD3524B35CBDD34251ABE07969C942DB14B2F2 per memory #168, #171 and requires `git tag -v vN.M.P` verification); F (doc split: the release-cut procedure moves from docs/versioning.md into a new docs/release-cut-procedure.md; the pre-release history (now-removed) section is moved to docs/release-history-archive.md as a fossilised record). docs/release-cut-procedure.md is the new authoritative procedure; docs/versioning.md keeps the rules + version-trigger table + prior-cut history table. The first release of the catalogue will be cut at a future state when the version-trigger criteria in docs/versioning.md are met. Recovery: docs/release-history-archive.md captures the v0.1.0 + v0.3.0 release body content. Per user directive 2026-10-15, this is the precursor to a clean release cut (T9.12, deferred). D-004 clean. 118a/118b/118c/123/124/125/126/127/128/129/130/131/132 authorship + entity-system gates remain CONFORMANT.


### CR-BP-131: dea:// URI Sync Tool (T9.7)

T9.7 follow-on. New `scripts/dea_uri_sync.py` (~220 lines) - the operational sync tool that clones + pulls catalog repositories across all known scopes. `clone_scope(scope, registries, depth=1)` clones a scope's repo from GitHub if absent (shallow by default). `pull_scope(scope, registries, ref=None)` fetches + pulls (and optionally checks out a ref). `sync_scope(scope, registries, depth, ref)` is the dispatcher (clone if absent, else pull). CLI modes: `<scope>` (sync a specific scope), `--all` (sync all known scopes), `--ref <ref>` (checkout a ref), `--depth <n>` (clone depth), `--list` (scopes with local/remote-only status). The in-thread scope (`dea-catalog-business-processes`) is skipped. New `tests/test_dea_uri_sync.py` with 14 tests (2 registry, 4 git operations, 2 pull_scope, 2 sync integration, 4 CLI; all pass). D-004 clean. 118a/118b/118c/123/124/125/126/127/128/129/130 gates remain CONFORMANT. Out-of-scope follow-ons: T9.2 IANA submission; T9.4 Permanent status; T9.8 production WSGI/ASGI server; T9.9 sync daemon.

### CR-BP-130: dea:// URI Web Resolver HTTP API (T9.6)

T9.6 follow-on. New `scripts/dea_uri_web.py` (~180 lines) - HTTP server exposing the dea:// URI resolver over HTTP. Uses stdlib `http.server` (no Flask/Quart dependency). 5 endpoints: `GET /health` (status + version), `GET /list` (all scopes), `GET /resolve?uri=...` (resolution JSON), `GET /fetch?uri=...` (file contents), `GET /exists?uri=...` (200/404). CORS enabled (`Access-Control-Allow-Origin: *`) for browser-based usage. Threading server (handles concurrent requests). Defaults: `127.0.0.1:8080`. New `tests/test_dea_uri_web.py` with 12 tests (3 health/list/CORS, 4 resolve, 2 fetch, 2 exists, 1 default 404; all pass). D-004 clean. 118a/118b/118c/123/124/125/126/127/128/129 gates remain CONFORMANT. Out-of-scope follow-ons: T9.2 IANA submission; T9.4 Permanent status; T9.7 sync tool; T9.8 production WSGI/ASGI server.

### CR-BP-129: dea:// URI Remote Resolver (T9.5)

T9.5 follow-on to the Entity System institutionalisation. Extends `scripts/dea_uri_resolver.py` (from CR-BP-128) with a new `_fetch_remote_repo` function and `--remote` CLI flag. When the local clone is absent, the resolver clones the catalog repository from GitHub (shallow clone, --depth 1) and resolves the URI against the freshly-cloned repo. The cloned repo lands at `$SIBLING_ROOT/{repo}` (default: `/home/hermes/Projects/dea-sibling-check/{repo}`). New 3 tests (total 23) cover: known scope remote fetch; unknown scope remote failure; CLI flag acceptance. The remote-fetch is a one-shot clone; ongoing sync is a T9.7 follow-on. D-004 clean. 118a/118b/118c/123/124/125/126/127/128 gates remain CONFORMANT. Out-of-scope follow-ons: T9.2 IANA submission; T9.4 Permanent status; T9.6 web resolver (HTTP API); T9.7 sync tool.

### CR-BP-128: dea:// URI Resolver CLI Tool (T9.3)

T9.3 follow-on to the Entity System institutionalisation. New `scripts/dea_uri_resolver.py` (~250 lines) - the reference implementation of the resolution algorithm from CR-BP-127 §8. The CLI resolves a `dea://` URI to a file path on disk, supports legacy `dea:` ids via the migration id map (CR-BP-mv1; 3640 lines), and works across the in-thread repo + the 11 sibling repos. CLI modes: default (print path), `--exists` (exit code), `--fetch` (print contents), `--list` (all scopes), `--resolve` (path + canonical URI). The slug computation matches the live tree's directory naming convention (descriptor only, no hash). New `tests/test_dea_uri_resolver.py` with 20 tests (5 URI parsing, 4 id rest splitting, 3 registry + migration map, 5 resolution, 3 CLI; all pass). D-004 clean. 118a/118b/118c/123/124/125/126/127 gates remain CONFORMANT. Out-of-scope follow-ons: T9.2 IANA submission; T9.4 Permanent status; T9.5 remote-fetcher (git clone); T9.6 web resolver (HTTP API).

### CR-BP-127: dea:// URI Scheme Registration (T9 follow-on)

T9 follow-on to the General Entity System institutionalisation. New `docs/entity-system/specs/07-dea-uri-scheme.md` (~10K) - the full URI scheme specification per RFC 7595 §7.4. The scheme name is `dea` (ASCII, lowercase). The status is Provisional (pending Permanent). The syntax is `dea://{scope}/{id}` where `scope` is the catalog identity_scope and `id` is the canonical entity id (per the corrected IDM-001 pattern from CR-BP-126). The scheme semantics: the URI is the canonical identifier; not directly resolvable; resolved via the cross-catalog resolution registry. The spec covers: scheme name + status; applicability (OpenDEAM entity catalog); authority + change control (TechNeHub Labs, emmanuel@otchere.com); scheme syntax (ASCII, no query/fragment, BASE32 hash); scheme semantics (canonical identifier; lifecycle-stable); encoding (ASCII only); resolution algorithm (deterministic); security considerations (URI spoofing, repository impersonation, DoS); privacy considerations; interoperability (HTTP/HTTPS conversion, git integration); examples; the IANA registration template (RFC 7595 §7.4 format); the registration procedure (Provisional first, then Permanent via mailing list review); the timeline (2026-10-15 spec drafted; 2026-11-01 IANA submission; 2027-Q1 I-D submission; 2027-Q3 Permanent). T9.2 follow-on is the actual IANA submission. T9.3 follow-on is the resolver CLI tool. T9.4 follow-on is the Permanent status achievement. D-004 clean. 118a/118b/118c/123/124/125/126 gates remain CONFORMANT.

### CR-BP-128: dea:// URI Resolver CLI Tool (T9.3)

T9.3 follow-on to the Entity System institutionalisation. New `scripts/dea_uri_resolver.py` (~250 lines) - the reference implementation of the resolution algorithm from CR-BP-127 §8. The CLI resolves a `dea://` URI to a file path on disk, supports legacy `dea:` ids via the migration id map (CR-BP-mv1; 3640 lines), and works across the in-thread repo + the 11 sibling repos. CLI modes: default (print path), `--exists` (exit code), `--fetch` (print contents), `--list` (all scopes), `--resolve` (path + canonical URI). The slug computation matches the live tree's directory naming convention (descriptor only, no hash). New `tests/test_dea_uri_resolver.py` with 20 tests (5 URI parsing, 4 id rest splitting, 3 registry + migration map, 5 resolution, 3 CLI; all pass). D-004 clean. 118a/118b/118c/123/124/125/126/127 gates remain CONFORMANT. Out-of-scope follow-ons: T9.2 IANA submission; T9.4 Permanent status; T9.5 remote-fetcher (git clone); T9.6 web resolver (HTTP API).

### CR-BP-127: dea:// URI Scheme Registration (T9 follow-on)

T9 follow-on to the General Entity System institutionalisation. New `docs/entity-system/specs/07-dea-uri-scheme.md` (~10K) - the full URI scheme specification per RFC 7595 §7.4. The scheme name is `dea` (ASCII, lowercase). The status is Provisional (pending Permanent). The syntax is `dea://{scope}/{id}` where `scope` is the catalog identity_scope and `id` is the canonical entity id (per the corrected IDM-001 pattern from CR-BP-126). The scheme semantics: the URI is the canonical identifier; not directly resolvable; resolved via the cross-catalog resolution registry. The spec covers: scheme name + status; applicability (OpenDEAM entity catalog); authority + change control (TechNeHub Labs, emmanuel@otchere.com); scheme syntax (ASCII, no query/fragment, BASE32 hash); scheme semantics (canonical identifier; lifecycle-stable); encoding (ASCII only); resolution algorithm (deterministic); security considerations (URI spoofing, repository impersonation, DoS); privacy considerations; interoperability (HTTP/HTTPS conversion, git integration); examples; the IANA registration template (RFC 7595 §7.4 format); the registration procedure (Provisional first, then Permanent via mailing list review); the timeline (2026-10-15 spec drafted; 2026-11-01 IANA submission; 2027-Q1 I-D submission; 2027-Q3 Permanent). T9.2 follow-on is the actual IANA submission. T9.3 follow-on is the resolver CLI tool. T9.4 follow-on is the Permanent status achievement. D-004 clean. 118a/118b/118c/123/124/125/126 gates remain CONFORMANT.

### CR-BP-126: Entity System Stage 7 (Legacy ID Reconciliation)

Final stage of the General Entity System institutionalisation. Resolves CR-BP-121 Gap Register §5.2 U-01 with new `docs/entity-system/specs/06-cross-catalog-uri.md` (~8K) defining the canonical URI form `dea://{scope}/{id}` + the resolvable GitHub URL form. Fixes IDM-001 pattern in `scripts/check_id_system.py` (corrected form `^[a-z]+:[a-z]+(-[a-z]+){1,4}-[a-z2-9]{6}$` matches all 5 type families including BP records with long descriptors like `process-manage-customer-relationship`; the original `[a-z]{2,3}` requirement was too strict). New `tests/test_check_id_system.py` with 14 tests (5 type families, 2 BP descriptor forms, 2 segment counts, 4 negative cases, 1 legacy-dea test, 1 live-tree regression test that scans all canonical records in entities/v1-alpha/). Legacy `dea:` ids are documented in `reconciliation/migration-id-map.yaml` (CR-BP-mv1; 3640 lines) and grandfathered per EGV-012. 118a/118b/118c/123/124/125 gates remain CONFORMANT. D-004 clean. Out-of-scope follow-ons: T7 per-repo disposition registers (sibling repos); T9 URI scheme registration (RFC 7595); T9 cross-catalog resolver tool.

### CR-BP-125: Entity System Stage 6 (Institutionalisation)

Stage 6 of the General Entity System institutionalisation. New `docs/governance/entity-system.md` (the canonical doctrine; ~9K covering 5 concerns, authority model, cardinal rules cross-refs, exception mechanism, migration policy, adoption stages). New `docs/governance/exception-process.md` (the EGV-011 escape hatch; lifecycle: requested/approved/active/expired/retired; the `reconciliation/normalization.yaml` review-retained verdict structure). `docs/governance/cardinal-rules.md` updated: R3 (Entity System cardinal rule) added; "How the rules are enforced" updated; "How to extend" subsection for entity-type profiles; History updated with the CR-BP-121..125 timeline. `CONTRIBUTING.md` updated: "R1 / R2 / R3" section added. New `schemas/entities/_template.yaml` (the common entity envelope template; ~3K worked example with type-specific required fields, relationships, classifications, provenance, lifecycle). `scripts/conformance_result.py` updated: gate at [33] promoted from `blocking: False` (advisory) to `blocking: True` (per CS-010). After this PR, no new entity can be admitted without satisfying the entity-system standard. The 35 `dea:` legacy tails are grandfathered per EGV-012. The 118a/118b/118c/123/124 gates remain CONFORMANT (or, for 123, the disposition register covers the advisory findings). D-004 clean. Follow-on: T7 cross-repo cascade; T8 legacy ID reconciliation.

### CR-BP-124: Entity System Stage 5 (Catalog Adoption + Disposition Register)

Files the per-record disposition for the entity-system gate's ~8700 advisory findings. New `reconciliation/entity-system-disposition-register.yaml` with 4 class-level dispositions: ES-002 BP (accept-residual: admitted records missing envelope fields are documented backward-incompatibilities); ES-002 PC (grandfathered: PC records use slim profile); ES-003 (accept-residual: non-canonical relationship types are valid per pre-entity-system BP-SEM rules; vocabulary migration is a T8 follow-on); ES-004 PC (grandfathered: PC records don't have a lifecycle state machine). New `reconciliation/cross-catalog-resolution.yaml` with 7 catalog identity-scope declarations (dea-catalog-business-capabilities, -business-objects, -organizational-units, -actors, -stakeholders, dea-metamodel, dea-architecture-framework); the `realizes` relationship from BP to BC is the primary cross-catalog pattern. `reconciliation/migration-id-map.yaml` is already in place from CR-BP-mv1 (3640 lines, 35 `dea:` legacy tails grandfathered per EGV-012). No entity, schema, or id changes. Stage 6 (CR-BP-125) institutionalises and promotes the gate from advisory to blocking. D-004 clean.

### CR-BP-123: Entity System Stage 3-4 (Reference Implementation + Umbrella Gate)

Implements the 5-rule umbrella gate per the Conformance Standard (CR-BP-122 §5). New `scripts/check_entity_system.py` (~700 lines, 5 rules: ES-001 Identity, ES-002 Entity Contract, ES-003 Relationship, ES-004 Lifecycle, ES-005 Conformance Umbrella); data-driven from `reconciliation/entity-system-registry.yaml`; --self-test (5 cases) + --strict + --json CLI. The registry declares 6 type-specific profiles (Process / ProcessContext / ProcessGroup / Activity / Task / ProcessScope); ProcessContext uses a slim profile (id + name); the other 5 types use the full envelope. Corrected IDM-001 canonical pattern (`^[a-z]+:[a-z]+(-[a-z]+){1,4}-[a-z2-9]{6}$`) that covers all 5 type families including BP records with long descriptors (the existing IDM-001 in `check_id_system.py` is too strict; that fix is a follow-on in T7 / T8). New 32-test suite in `tests/test_check_entity_system.py` (all pass). Wired into `scripts/conformance_result.py` at [33] as advisory (per CS-010); CI extension runs the gate under --strict after the 118c prose gate. Live tree: ~8700 advisory findings (real shape issues that CR-BP-124 disposition register will address). Stage 6 (CR-BP-125) promotes the gate to blocking. D-004 clean. 118a/118b/118c authorship gates remain CONFORMANT.

### CR-BP-122: Entity System Stage 2 (Specifications)

Codifies the 9 N-classification decisions + 7 U-classification open questions from CR-BP-121's Gap Register into 5 normative spec docs under `docs/entity-system/specs/`. (01) Identity Standard IS-001..IS-006 - canonical `processes:` namespace, `identity_scope` for cross-catalog references, the 35 `dea:` legacy tails grandfathered per EGV-012. (02) Entity Contract Standard EC-001..EC-004 - common envelope (id / type / name / definition / description / relationships / classifications / provenance / lifecycle) + 5 type-specific profiles (Process / ProcessContext / ProcessGroup / Activity / Task) + 6th (ProcessScope) dormant-by-design. (03) Relationship Standard RS-001..RS-005 - 3 stored types (composes / realizes / specializes) + 1 derived (part-of view-time only); source / target type constraints; cardinality rules; cross-catalog references. (04) Lifecycle Standard LS-001..LS-007 - 5-state machine (proposed / admitted / deprecated / retired / superseded); transition table; identity continuity; version-separation discipline per EGV-007. (05) Conformance Standard CS-001..CS-011 - 5-rule umbrella gate ES-001..ES-005; rollup integration; CI enforcement; exception mechanism (review-retained verdict in `reconciliation/normalization.yaml`); advisory-then-blocking staging. U-01 cross-catalog URI form is deferred to T8 of the umbrella programme; U-02..U-07 resolved in the corresponding specs. Design-only: 0 entity changes, 0 schema changes, 0 id changes. Stage 3-4 (CR-BP-123) implements the umbrella gate; Stage 5 (CR-BP-124) files the disposition register; Stage 6 (CR-BP-125) institutionalises. D-004 clean. 118a/118b/118c authorship gates remain CONFORMANT.

### CR-BP-121: General Entity System Stage 1 (Reconnaissance + Charter)

Stage 1 of the 6-stage General Entity System institutionalisation in this catalog. Renumbered from CR-BP-16 (per the user-provided doc's numbering note; CR-BP-116..118 are taken; CR-BP-121 is next-free). The slice is non-destructive: produces 4 doc outputs in `docs/entity-system/` (Charter, Existing Decisions and Gap Register, Normative Design Proposal, Implementation and Adoption Plan) and a carrier CR; 0 entity changes, 0 schema changes, 0 bulk renames. The 33 decisions walked in the Gap Register classify 15 as retained (R), 2 as historical-only (H), 9 as needing framing (N) - codified in the Normative Design Proposal - and 7 as open questions (U) - resolved or deferred in the Implementation Plan. The 5 normative decisions: identity (processes: family canonical; dea: grandfathered per EGV-012), entity contract (common envelope + type-specific profiles), relationships (4 types: composes / realizes / specializes / part-of), lifecycle (5-state machine: proposed / admitted / deprecated / retired / superseded), conformance (5-rule umbrella gate ES-001..ES-005, advisory-then-blocking). Companion: DEA-ID-000 (foundation paper) + CR-012 (org-wide governance CR) in the new `dea-governance` repo. Follow-on slices: CR-BP-122 (Stage 2 specifications), CR-BP-123 (Stage 3-4 reference implementation + umbrella gate), CR-BP-124 (Stage 5 catalog adoption + disposition register), CR-BP-125 (Stage 6 institutionalisation). Cross-repo cascade to the 11 sibling repos is T7 of the umbrella programme. D-004 clean. 118a/118b/118c authorship gates remain CONFORMANT.

### CR-BP-118c: Prose Content-Field Authorship Gate (Agent allowlist)

The 118a authorship gate (AUT-001..003) covers the **metadata** fields whose values are literal identity strings (`**Owner**`, `**Author**`, `audit.author`, `authors[].name`). The 118c slice extends the cardinal rule to **content** fields (`name`, `definition`, `description`, `summary` on entity YAML records) where the denylist applies with one doctrinal exception: the keyword `Agent` is allowlisted in content fields because the dea-catalog-processes domain vocabulary uses `Agent` extensively as a workforce/role noun in 299+ content fields (e.g. "Agent Operations", "Agent Acquisition and Onboarding", `AgentProfile`, `multi-agent.yaml`, "agentive capability") that predate the cardinal rule and have nothing to do with the Coder/Agent authoring tools. A live audit confirms 299 `Agent` content hits in 145 files; all are domain vocabulary, none are authoring-tool references. The other denylist tokens (Coder, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3) are blocked in content fields with the same word-boundary semantics as the metadata gate. New gate `scripts/check_prose_authorship.py` (PROSE-001 blocking, PROSE-002 advisory; data-driven from `reconciliation/prose-fields.yaml`); new test module `tests/test_check_prose_authorship.py` (20 tests, all pass). Live gate stays CONFORMANT; 0 PROSE-001 findings on the current main. CI integration: `ci.yml` runs the gate under `--strict` immediately after the 118a authorship gate. 0 entity content changes; 0 id changes; 0 cross-reference changes. Carrier: `change-requests/CR-BP-118c-prose-authorship-gate.md`.

### CR-BP-118a: Authorship-Field Cardinal Rule + Retroactive Sweep

User directive 2026-10-13: "There is no where that the `Coder (eaojnr)` or `Coder` or `Agent` should be published." Two new cardinal rules (R1: authorship-field allowlist; R2: named-role file rule) are pinned in `docs/governance/cardinal-rules.md` and enforced by a new blocking gate (CR-BP-118 / AUT-001..003) wired at rollup position [32]. The gate is data-driven from a new `reconciliation/authorship-fields.yaml` (allowlist `{Emmanuel A. Otchere, TechNeHub Labs}`; denylist `{Coder, Agent, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3}`). A retroactive sweep rewrites every authorship-metadata hit in the repo: 141 files, 341 textual replacements. 0 entity content changes; 0 id changes; 0 cross-reference changes. Sealed-file integrity preserved (two embargo carrier SHAs re-recorded under CR-BP-118 governance). The 247 prose-content occurrences (`Agent` / `Coder` in record `name` / `definition` / `description` fields) are inventoried for the 118c follow-on but not rewritten. Carrier: `change-requests/CR-BP-118-authorship-cardinal-rule.md`.

### CR-BP-117c: Folder/Path Clarity (C-1 dir rename + C-3 path scheme)

User-facing navigation fix for the 'repeat of entities with different IDs' concern. C-1: all 3,674 record directories renamed from opaque `<cell>-<hash>` to kebab-cased record names via `scripts/rename_dirs_human_names.py` (shipped for auditability + sibling-repo replay; `git mv`, bottom-up, zero collision fallbacks - EID-001's same-level uniqueness invariant made collisions unreachable). A task path that was `fa-retire/fa-retire-2ptdnw/fa-retire-wkbrsa/fa-retire-3g3m9u/fa-retire-confirm-q2xkf3/` is now `fa-retire/Regulated-Run-Off/Conclude-Regulated-Run-Off/Settle-Final-Claim/Confirm-Finality/`. The BASE32 hash stays in the record filename (IDM-001 unchanged); cell dirs keep their `<domain>-<stage>` slugs. C-3: every L0 ProcessContext README gains a `## 13. Path Scheme` section rendering the cell's directory tree with level labels (new `path-scheme` section in `scripts/generate_readmes.py`; 49 cell-root READMEs regenerated, other 3,674 READMEs byte-identical per RDM gate). C-2 (symlinks) skipped per CR opt-in note. CATALOG.yaml regenerated (3,877 path entries). 2 doc references in `docs/examples/manage-customer-relationship.md` updated. New test module `tests/test_folder_path_clarity.py` (12 tests, all pass). 0 entity-record content changes; 0 id changes; 0 cross-reference changes (refs use `processes:<id>` form, not paths). Carrier: `change-requests/CR-BP-117-entity-id-convention-clarity.md`.

### CR-BP-117a: Entity-Identity Clarity Gate (Diagnosis Slice)

Single-PR diagnosis slice that surfaces the 22 cross-level name collisions the user-noticed "repeat of entities with different IDs" pattern. New blocking gate `scripts/check_entity_identity.py` (EID-001..004) wired into the 31-gate rollup at position [31] after RDM. Four rules: EID-001 same-level identity collisions (advisory; live: 0 hits, expected because IDM-001 catches at write time); EID-002 README references the canonical id token in line 1 (advisory; live: 0 hits, all READMEs regenerated by CR-BP-114); EID-003 README body surfaces the level token (advisory; live: 0 hits, generator already includes "required at the L<n> level"); EID-004 cross-level name reuse reported as an inventory (advisory, informational; live: 22 hits, all are the L0 cell / L1 group / L2 process containment-tree pattern - not defects). The 22 cells where the collision occurs: A&O x 2 (Activate, Build), E&O x 4 (Activate, Build, Improve, Retire), F&A x 1 (Activate), G&E x 5 (Activate, Build, Design, Improve, Operate), P&R x 4 (Build, Conceive, Design, Improve), S&D x 6 (Activate, Build, Design, Improve, Operate, Retire). S&D is the most collision-rich because of the dual L0+L2 pattern at SD.Activate and SD.Retire. CR-BP-117b (id-convention rename candidates) and CR-BP-117c (folder/path clarity) are follow-on slices gated on the user's read of the EID-004 inventory. New test module `tests/test_check_entity_identity.py` (level inference, level-name formatting, same-level collision detection, cross-level allow, EID-004 inventory, live invariants, CLI). 0 entity-record changes; 0 id changes. Carrier: `change-requests/CR-BP-117-entity-id-convention-clarity.md`.

### CR-BP-115: Admission-Authority Marker (Data over Regex) and open_change_requests Count Fix

Single-PR governance fix replacing the last piece of admission-authority state that lived in code. (a) Replaces the hardcoded `_ADMISSION_CR_RE` regex allowlist in `scripts/check_admission_gate.py` (21 enumerated CR ids + a 45-line narrative comment with a verbatim-duplicated paragraph) with a machine-readable `**Admission authority**: yes` marker carried in the CR files themselves. The allowlist becomes derived data: authoring an admission tranche and registering its authority collapse into the same edit, in the same file, in the same PR. 33 CR files backfilled with the marker (the frozen manifest derived mechanically from the old regex). `--json` output gains `admission_authorities` for reviewer visibility. (b) Fixes the duplicated condition at `scripts/regenerate_catalog.py:466` ("Status**: Merged" in head or "Status**: Merged" in head), whose dead branch counted all non-Merged CRs as open. `open_change_requests` drops from 128 to 97 (32 Accepted + 1 Merged + 2 no-status files now correctly classified). Status parsing upgraded from substring matching to line-level metadata matching (mirrors `check_cr_metadata.py`'s META_LINE pattern), eliminating body-text false positives. New test modules: `tests/test_check_admission_gate.py` (marker regex, bare-id derivation, authority loading, live manifest equality, CLI) and `tests/test_regenerate_catalog_open_count.py` (every status class, qualified variants, no-status warning, body-text rejection, live sanity). 0 entity-record changes; 0 id changes; ADM-001 semantics unchanged (authority set identical before and after). Carrier: `change-requests/CR-BP-115-admission-authority-marker.md`.

### CR-BP-114: Record README Regeneration, Drift Gate, and Release-Cut Integration

Single-PR remediation closing the last pre-mv1 presentation surface. All 3,723 record READMEs under `entities/v1-alpha/` regenerated from the current entity records via `scripts/generate_readmes.py --force` (new flag; the generator previously skipped existing READMEs, which let the tree freeze at the pre-mv1 state). Four stale README classes replaced: 3,405 frozen generator READMEs (legacy `dea:*` ids), 162 tranche-written L1/L2 directory READMEs, 100 task dirs carrying research-README content instead of the Task documentation profile, and 49 stale cell-root copies of the retired contexts-register README. Generator also gains `--check` (drift detection, exit 3; mirrors `regenerate_catalog.py --check`) and an L0 type-label fix (`Type: ProcessContext` instead of `Type: Record`). New blocking gate `scripts/check_readme_consistency.py` (RDM-001 missing/stale, blocking; RDM-002 orphan, advisory) wired into `conformance_result.py` (GATES 29 -> 30) and `ci.yml` (+1 blocking step): record READMEs are now a generated artifact under CI enforcement, the same contract as CATALOG.yaml. `docs/versioning.md` "Cutting the next tag" gains step 3 verifying README consistency before every release cut. tests/test_check_readme_consistency.py: 8 tests pass; live gate CONFORMANT under `--strict`. 0 id changes; 0 record-content changes; legacy `dea:*` tokens inside record definition prose preserved verbatim (content migration is a separate CR decision). CATALOG.yaml regenerated: `open_change_requests` 127 -> 128, all other counts unchanged. Carrier: `change-requests/CR-BP-114-readme-regeneration-drift-gate.md`.

### CR-BP-113: mv1 Migration Completion - Docs, Templates, Schemas, and HREF Repair

Single-PR remediation completing the CR-BP-mv1 migration in 5 surfaces the structured-data layer left behind. (a) Repairs 272 broken relative href targets across 189 entity/discovery files (data-driven via `reconciliation/migration-id-map.yaml` + an explicit CR-rename table); folded-scalar hrefs in 5 process-group records also collapsed. (b) Modernizes all 5 entity templates (business-process, activity, task, process-group, process-scope) to the `processes:*` id family and current one-directory-per-record layout, including the evidence-link type enum at `templates/business-process.yaml:92`. (c) Fixes the two schema/validator leftovers: `process-scope.schema.json` id pattern flipped to `^processes:scope-`; `scripts/check_id_system.py` IDM-006 regex extended to `scope`; a residual `dea:scope-customer-facing-operations` id in `processes:process-pr-operate-bbe384`'s `metadata.scope` block added to `migration-id-map.yaml` known_residuals. (d) Completes the docs layer: 3 `contexts/v1-alpha/` live refs and 12 `dea:*` id-family refs across 4 files (docs/context.md, docs/architecture.md, docs/examples/manage-customer-relationship.md rewritten as a current-shape worked example, README.md) flipped to canonical `processes:*` / `entities/v1-alpha/`; historical narrative kept inside explicitly-marked legacy blocks. (e) Repairs `change-requests/README.md` (removed 139 duplicate rows; added the missing CR-BP-102 and CR-BP-113 rows) and retargets the stale contributions-queue record to the live BP location. Three new permanent gates: `check_href_targets.py` (HREF-001..003, blocking), `check_templates.py` (TPL-001..005, blocking), `check_cr_readme.py` (CRR-001..003, blocking, in-repo uniqueness only; cross-repo table exempts duplicates since it indexes sibling-repo CRs once per narrative anchor). Wired into `conformance_result.py` GATES (26 -> 29) and `ci.yml` (3 new blocking steps). Targeted pytest 27/27 passed (`tests/test_check_href_targets.py` + `tests/test_check_templates.py` + `tests/test_check_cr_readme.py`); live `conformance_result.py` CONFORMANT (0 blocking); 0 entity-record changes; CATALOG.yaml regenerated: `open_change_requests` 126 -> 127, all other counts unchanged. Carrier: `change-requests/CR-BP-113-mv1-migration-completion.md`.

### CR-BP-112: Independent-Authorship Determination, NOTICE/LICENSE Correction, and Reference Embargo Gate

Single-PR governance slice closing the attribution posture end-to-end. Four moves: (a) records the formal independent-authorship determination that grounds NOTICE's "Third-party attributions: None" declaration (all 3,723 entity records, 29 discovery records, and research registers are an independent original work authored under this repo's CR governance chain; the mentions removed by the 2026-09-22 strip were evidence-cite-level references, not derivation; citation is not incorporation); (b) fills the LICENSE Apache-2.0 appendix copyright placeholder (Copyright [yyyy] [name of copyright owner] -> Copyright 2026 TechNeHub Labs, matching NOTICE's existing copyright line); (c) sweeps the residual embargoed-term mentions that post-date the strip (CHANGELOG.md CR-BP-TMF-EMBARGO entry retitled and body rephrased to "the embargoed framework"; the three later CR summaries' embargo-compliance attestation lines rephrased to "Zero embargoed-framework references introduced"; change-requests/README.md rows for the strip CR and CR-BP-105/-106/-107 rephrased identically; CR-BP-105 acceptance line 93, CR-BP-106 lines 27/118/134, CR-BP-107 line 19 rephrased; drop-do-not-substitute policy unchanged); (d) adds a permanent blocking conformance gate `scripts/check_reference_embargo.py` (EMB-001..004) so references cannot re-enter silently. The gate masks the `CR-BP-TMF-EMBARGO` / `TMF-EMBARGO` id token (class 2: a change-request id, not the organization) and the paths of sealed files, hash-locks the sealed carrier and the definition-site files (gate script, allowlist, carrier CR, test fixtures) under EMB-003, and reads a data-driven false-positive registry (`reconciliation/reference-embargo-allowlist.yaml`) seeded with the 7 known code-identifier false positives documented in the strip CR. Gate wired into `conformance_result.py` GATES (26 total) as blocking and into `ci.yml` as a blocking step immediately after the ID System gate. NOTICE "Third-party attributions" section carries the determination basis line. Targeted pytest 16/16 passed (`tests/test_check_reference_embargo.py`); `check_reference_embargo.py --strict` CONFORMANT (0 findings); `--self-test` PASS; `check_cr_metadata.py --strict` CONFORMANT (126 CR files); full-repo audit for the term list returns zero substantive hits outside the sealed carrier, the masked id token, and the recorded false-positive registry. No entity-record changes; no id changes; CATALOG.yaml regenerated: `open_change_requests` 125 -> 126; all other counts unchanged. Carrier: `change-requests/CR-BP-112-independent-authorship-determination.md`.

### CR-BP-111: A&O Regulator-Tied L3/L4 Decomposition Tranche (5 BPs x 4 Activities x 5 Tasks = 100 new records)

L3/L4 decomposition follow-on to CR-BP-106 (admitted 5 regulator-tied BPs at AgencyAndOrganization x {Conceive, Design, Build, Operate, Improve}). Lands 20 new Activity records (4 per BP following the 4-concern pattern: supervisor-controlled scope, fitness-and-propriety, supervised-training completion, continuing-supervisor notification) and 100 new L4 Task records (5 per Activity per the 5-phase verb-object completion pattern from `scripts/decompose_l4.py`). 5 BP records patched with `metadata.activity_references` back-references. 5 `research/l3-candidate-universe.yaml` files authored. CATALOG.yaml regenerated: canonical 3,602 -> 3,722 (+120); research_files 329 -> 334 (+5); open_change_requests 122 -> 124. `scripts/check_admission_gate.py` allowlist extended to admit `CR-BP-111`. 6 test files bumped for the new counts (Activity 560 -> 580; Tasks 2,800 -> 2,900; total 3,598 -> 3,718 records). Posture: `check_activity_model.py` CONFORMANT (0 findings); `check_admission_gate.py --strict-provenance` CONFORMANT-WITH-WARNINGS (0 blocking); `check_cr_metadata.py --strict` CONFORMANT. The `scripts/decompose_l4.py` script's pre-mv1 path scheme is worked around by `scripts/reorg_cr_bp_111_tasks.py`; a permanent fix to `decompose_l4.py` is filed as a follow-on. Carrier: `change-requests/CR-BP-111-ao-regulator-tied-l3-decomposition.md`.

### CR-BP-107: CR-META Legacy Retro-Fit (Validator + 9 Historical CRs)

Single-PR retro-fit programme closing the long-running `validate` workflow CR-META failures (21 findings across 9 CR files since at least 2026-09-22). Two moves: (1) extend `scripts/check_cr_metadata.py` to admit three pre-existing CR naming patterns (CR-BP-SPEC-*, CR-BP-TMF-EMBARGO, and cross-repo CR-<UPPER>-<digits>); (2) add missing Status / Layer / Owner metadata to 5 historical CRs (CR-BP-02, -03A, -04, -SPEC-BP-01, -ECF-CG-004) and correct the Status value of CR-BP-mv1. CR-BP-13's `**Companion to**` is rephrased to include an intra-repo `CR-BP-11` anchor plus prose explaining the cross-repo reference. No entity-record changes. No `CATALOG.yaml` regeneration. Posture: `check_cr_metadata.py --strict` reports `CONFORMANT` (0 new, 0 legacy findings); `--self-test` PASS. Carrier: `change-requests/CR-BP-107-cr-meta-legacy-retrofit.md`.

### CR-BP-106: AgencyAndOrganization Regulator-Tied Admission Tranche (5 Cells, Combined)

Combined single-PR admission of the 5 regulator-tied Business Processes at the AgencyAndOrganization x {Conceive, Design, Build, Operate, Improve} ECF coordinates, admitted under the CR-BP-105 escape-clause discovery outcome (10/10, ADMIT-CANONICAL recommendation) under the CR-BP-62 method. 5 PC replacements + 5 PG replacements + 5 new BPs + 5 BP READMEs = 20 new/modified files:

- ao-conceive: Conceive Licensed or Regulated Agent Capacity (FCA SMCR CF1..CF11; state healthcare licensure scopes; EU AI Act Art. 9 risk classification; US state bar admissions)
- ao-design: Design Regulated Role Architecture (FCA SMCR SYSC 25 Annex 1; FAA Part 121 subpart Y CRM; EU AI Act Art. 14 human-oversight roles; The Joint Commission credentialing-and-privileging)
- ao-build: Build Regulated Agent Pool (FCA Financial Services Register; NMLS / NAIC Producer Database; FAA airmen certification database; OFAC SDN screening per 31 CFR 501; Bank Secrecy Act per 31 USC 5311; FCRA per 15 USC 1681; ADA per 42 USC 12102)
- ao-operate: Operate Regulated Performance Oversight (FCA SMCR Conduct Rules (COCON); FINRA Rule 3110; FAA Part 117; state bar MCLE; state healthcare CME; NAIC CE; EU AI Act Art. 14 continuing-oversight)
- ao-improve: Improve Regulated Workforce Capability (FCA SMCR fit-and-proper annual assessment (SYSC 25 / FIT); state bar MCLE; state healthcare CME; NAIC CE; FAA Part 121 subpart Y recurrent training; EU AI Act Art. 14 ongoing training)

The 5 regulator-tied BPs complete the A&O regulator-tied chain (Conceive -> Design -> Build -> existing Activate (PR #122) -> Operate -> Improve -> existing Retire (PR #114)). A&O is the first domain with regulator-tied coverage across all 7 stages. Posture: 28 discovery records checked, 0 findings; IDM-001..007 CONFORMANT (3603 records); MECE-001..008 CONFORMANT; LCM-001..005 CONFORMANT; ACT-001..015 CONFORMANT (560 Activities, 145 BPs); BP-C1..C4 + BP-QUAL-001..012 CONFORMANT; S21 CONFORMANT; TASK-001..005 CONFORMANT (2800 Tasks); targeted pytest 167/167 passed; broad catalog validator sweep 244/244 passed; `open_change_requests` 120 -> 121. Zero embargoed-framework references introduced (CR-BP-TMF-EMBARGO compliance continues). Lands after CR-BP-105 (#155) which established the discovery recommendations. L3 Activity and L4 Task decomposition lands in CR-BP-111 (deferred follow-on tranche).

### CR-BP-TMF-EMBARGO: reference embargo compliance strip

User directive 2026-09-22 (eaojnr, explicit religious mandate): NEVER reference the embargoed framework (see the embargoed term list in the carrier CR and gate allowlist) in any artifact of any org repo. Drops all 73 substantive embargoed-framework citations across 24 merged-history files: 7 discovery records (CR-BP-63 baseline), 12 admitted entity files across EO/FA/PR/PR-Design/PV-Retire clusters, 3 PR.Operate research register files, 8 change-request documents (CR-BP-04 / -11 / -63 / -64 / -66 / -67 / -74 + README table), 2 tooling files (`tests/test_build_bp13a_tranche.py` whitelist, `tools/build_bp13a_tranche.py` evidence_links), 1 archive (`01_plan/archive/pr-bp-13a.md`). Substitution policy: drop, do not substitute. The PR.Design cluster gains an APQC PCF cite to maintain the `test_render_l2_process_uses_real_industry_evidence` regression guard (no embargoed-framework cite reintroduced). Carrier: `change-requests/CR-BP-TMF-EMBARGO-tmforum-reference-strip.md`. Posture: 25 conformance gates CONFORMANT (10 blocking + 15 advisory); targeted pytest 39/39 passed; 0 new entity records; `CATALOG.yaml` unchanged; `reconciliation/conformance_report.yaml` runtime-path noise reverted. Next slice: A&O domain-deep sourcing tranche (Option C) gated on this landing.

### CR-BP-105: AgencyAndOrganization Domain-Deep Sourcing Tranche (Escape-Clause Discovery for Conceive/Design/Build/Operate/Improve)

Discovery-only slice under the CR-BP-62 escape-clause method, applying domain-deep sourcing (Option C of the programme doctrine) to the five AgencyAndOrganization ECF cells that previously had only the substrate-neutral general-case BP: Conceive, Design, Build, Operate, Improve. Five new escape records at `discovery/v1-alpha/agency-and-organization-{conceive,design,build,operate,improve}-escape.yaml`, each evaluating one regulator-tied candidate against BP-LIFE-001..015 with the canonical five-axis rubric. All five recommend ADMIT-CANONICAL (10/10):

- ao-conceive: Conceive Licensed or Regulated Agent Capacity (FCA SMCR CF1..CF11; state healthcare licensure scopes; EU AI Act Art. 9 risk classification; US state bar admissions)
- ao-design: Design Regulated Role Architecture (FCA SMCR SYSC 25 Annex 1; FAA Part 121 subpart Y CRM; EU AI Act Art. 14 human-oversight roles; The Joint Commission credentialing-and-privileging)
- ao-build: Build Regulated Agent Pool (FCA Financial Services Register; NMLS / NAIC Producer Database; FAA airmen certification database; OFAC SDN screening per 31 CFR 501; Bank Secrecy Act per 31 USC 5311; FCRA per 15 USC 1681; ADA per 42 USC 12102)
- ao-operate: Operate Regulated Performance Oversight (FCA SMCR Conduct Rules (COCON); FINRA Rule 3110; FAA Part 117; state bar MCLE; state healthcare CME; NAIC CE; EU AI Act Art. 14 continuing-oversight)
- ao-improve: Improve Regulated Workforce Capability (FCA SMCR fit-and-proper annual assessment (SYSC 25 / FIT); state bar MCLE; state healthcare CME; NAIC CE; FAA Part 121 subpart Y recurrent training; EU AI Act Art. 14 ongoing training)

The five regulator-tied candidates complete the upstream + downstream chain for A&O domain-deep sourcing, bridging the existing Activate licensed-workforce BP (PR #122 / CR-BP-81) and the existing Retire regulated-workforce-wind-down BP (PR #114 / CR-BP-73). Posture: 28 discovery records checked, 0 findings; 25 conformance gates CONFORMANT; `open_change_requests` 119 -> 120. Zero embargoed-framework references introduced (CR-BP-TMF-EMBARGO compliance continues). Admission tranches (CR-BP-106..110 per-cell, each landing full PC + PG + BP stack) gate on this discovery slice. Lands after CR-BP-TMF-EMBARGO (#154) so the embargo remediation precedes the sourcing tranche.

### CR-BP-mv1: Entity storage + id system migration (org-wide Wave 1)

Migrates the repo to the org-wide id system and the L0-rooted containment tree (metamodel canonical specs: dea-metaframework `docs/id-system.md` + `docs/entity-storage-layout.md`, PR #31). All 3,598 canonical records rewritten from the legacy `dea:*` id family to `processes:<level>-<domain>-<stage>-<hash>`; every structured cross-reference rewritten; the flat pre-migration entity layout replaced by the containment tree (`contexts/v1-alpha/` retired; PCs live at cell level). Migration id map at `reconciliation/migration-id-map.yaml` (3,623 entries + documented known residuals). New blocking gate `scripts/check_id_system.py` (IDM-001..007 catalog-wide; IDM-008 PR-scoped file coherence with per-PR CI report artifact). Cross-check stage (XC-01..11) via `scripts/cross_check_org_wide.py`: 145 CR/ADR artifacts audited org-wide; 77 historical CRs + 3 sibling-repo ADRs received layout-note banners (content verbatim). Disclosed repairs: disposition register completed for the CR-BP-101 SD/Retire BP; tranche plan completed (`sd-ret.101`); stale count assertions bumped (139 -> 140 BP counts; 73 -> 79 tranche count) with pre-existing drift documented in the PR body. Register audit gate repaired for the containment tree (walker + canonical `eo` domain token) and AO x Retire register cell `audit_status` corrected to `landed` (pre-existing drift on main). PR #148 (CR-BP-L4-03) merged ahead of this slice; its 340 enriched GovernanceAndExistence Task records were absorbed via three-way splice at merge time (migration structure kept, enriched content spliced in, legacy ids rewritten through the id map).

## [2.4.0-migration] - 2026-09-07

### CR-BP-18 implementation: ECF Domain enum migration to the v2.4.0
canonical Domain set (carried by `technehub-labs/dea-metaframework` v2.4.0;
CR-ECF-007 + ADR-ECF-002). One of seven Domains renamed: Domain 3
`PeopleAndOrganization` -> `AgencyAndOrganization` (kebab-case
`people-organization` -> `agency-organization`), driven by the Substrate
Independence Stress Test. 16 files re-keyed (3 schemas, 3 check scripts,
1 contribution template, 3 research files, 1 docs file, 5 CR records);
reconciliation artifacts regenerated. The DOMAIN_NAMES abbreviation key
`po` -> `ag` in `tools/build_bp13a_tranche.py`. No content redistribution
required (CR-ECF-007 §6.3).

## [2.3.0-migration] - 2026-09-07

### CR-BP-17 (a.k.a. CR-BP-ECF-01) implementation: ECF Domain enum migration to the v2.3.0
canonical Domain set (carried by `technehub-labs/dea-metaframework` v2.3.0;
CR-ECF-006 + ADR-ECF-001). Five of seven Domains renamed; one Domain
replaced (Supply & Resources -> Strategy & Direction). 109 files modified;
5 context YAMLs + 1 CR file renamed; 2 reconciliation artifacts regenerated.

This is the 3rd landing in the v2.3.0 wave (after metaframework + metamodel);
the next is `dea-catalog-business-capabilities` (CR-BC-ECF-01).

### Changed

- **Process Context ID abbreviations** (CR-BP-17 (a.k.a. CR-BP-ECF-01) §1.1, v2.3.0):

  | # | Before (v2.2.0) | After (v2.3.0) |
  |---|------------------|------------------|
  | 1 | `cd` (CustomerAndDemand) | `pr` (PartyAndRelationship) |
  | 2 | `sr` (SupplyAndResources) | `sd` (StrategyAndDirection) |
  | 5 | `po` (ProductAndOffering) | `pv` (ProductAndValue) |
  | 6 | `od` (OperationsAndDelivery) | `oe` (EnablementAndOperations) |
  | 7 | `fv` (FinanceAndValue) | `fa` (FinanceAndAccounting) |

- **5 Process Context YAMLs renamed + content migrated**:
  - `dea-pc-cd-b.yaml` -> `dea-pc-pr-b.yaml` (Party & Relationship x Build)
  - `dea-pc-cd-c.yaml` -> `dea-pc-pr-c.yaml` (Party & Relationship x Conceive)
  - `dea-pc-cd-d.yaml` -> `dea-pc-pr-d.yaml` (Party & Relationship x Design)
  - `dea-pc-cd-im.yaml` -> `dea-pc-pr-im.yaml` (Party & Relationship x Improve)
  - `dea-pc-cd-op.yaml` -> `dea-pc-pr-op.yaml` (Party & Relationship x Operate)
- **1 CR file renamed**: `CR-BP-13a-customer-and-demand-admission.md` ->
  `CR-BP-13a-party-and-relationship-admission.md` (the CustomerAndDemand
  tranche is now the PartyAndRelationship tranche).
- **3 JSON schemas** (`process-context.schema.json`, `entity.schema.json`,
  `contribution.schema.json`): Domain enums migrated to v2.3.0.
- **8 conformance scripts** in `scripts/`: CANON enum, lowercase mapping,
  test fixtures, and disposition records migrated.
- **1 build script** in `tools/build_bp13a_tranche.py`: `DOMAIN_NAMES`
  keys flipped from `cd/sr/pd/od/fv` to `pr/sd/pv/oe/fa`.
- **4 test files** in `tests/`: fixtures migrated.
- **2 reconciliation artifacts regenerated**: `inventory.yaml` and
  `baseline/v1.yaml` (they round-trip byte-identically under the new
  identifiers; `scripts/build_inventory.py --self-test --strict` passes).
- **11 CR files in `change-requests/`**: every narrative reference to
  the v2.2.0 Domain names updated.
- **6 docs files in `docs/`**: narrative updated.
- **README.md** + **change-requests/README.md**: pointers updated.
- All CR/programme references to the renamed Domains re-keyed.

### Not changed (out of scope for the v2.3.0 migration)

- **No new Process Contexts admitted.** The v2.3.0 wave is a pure
  rename; no new coordinates are admitted in this PR.
- **The L1 process discovery work for the renamed Domains** (Strategy
  & Direction, Product & Value, Enablement & Operations, Finance &
  Accounting, Party & Relationship deepening) is parked as a separate
  task that follows this PR — not in scope.
- **The `test_check_struct_clean_repo_passes` pre-existing failure**
  (`STRUCT-OK` is in stdout but the test asserts in stderr) — pre-existing,
  not introduced by this PR.

### Verification

- `tests/conformance/`: 8/8 conformance suites pass.
- `tests/runtime/`: all runtime tests pass.
- `tests/test_build_bp13a_tranche.py`: **15/15 pass**.
- `tests/test_apply_phase_5_tranche.py`: all pass (idempotency holds).
- `tests/test_reconciliation_baseline.py`: 11/12 pass (1 pre-existing
  failure unrelated to this PR).
- `scripts/check_ecf_conformance.py`: **PASS** (28 entries conform).
- `scripts/check_process_context.py`: **PASS** (PC-001..PC-008).
- `scripts/check_process_semantics.py`: **CONFORMANT** (BP-SEM S21).
- `scripts/build_inventory.py --self-test --strict`: **PASS**
  (inventory + baseline round-trip byte-identically under v2.3.0 IDs).

## [2.5.0-conformance-gate] - 2026-09-08

The CR-BP-16 conformance gate machinery (S10 / S15 / S16 / S17 / S18 /
S22 / S25; CR-META strict mode; unified Conformance Result) is now
live in CI. Landed across PRs #38-#42; the second `[Unreleased]`
block that this section replaces predated the CR-BP-22 audit / CR-BP-24
discipline. Date-stamped retroactively per the existing
`[2.4.0-migration]` / `[2.3.0-migration]` pattern.

### CR-BP-16 §16 enforcement promotion (CR-META strict mode)

The CR-META-001..006 gate is now **blocking** in CI for new
and modified CRs. Legacy CRs (mtime < 2026-09-06) remain
advisory. Five CRs were retro-fitted to the §21 metadata
format: CR-BP-03C, CR-BP-12, CR-BP-14, CR-BP-15, and
CR-BP-16. The 16th (CR-BP-13A) was already §21-compliant
and was used as the canonical reference.

- `scripts/check_cr_metadata.py` (extended):
  - **New `--cutoff-date` flag** (default 2026-09-06 = CR-BP-16
    acceptance). CRs last modified on or after the cutoff are
    classified as "new"; CRs modified earlier are "legacy".
  - **New `--strict` mode**: blocks the gate when any NEW CR
    fails any rule. Legacy CRs are reported as advisory and
    do not block.
  - **CR-META-001 normalisation**: `Proposed (2026-09-03)` is
    accepted as a valid `Proposed` Status (parens stripped).
  - **CR-META-002 normalisation**: `L1 (Process Catalog)` is
    accepted as a valid `L1` Layer (parens stripped).
  - **Filename pattern** extended to admit `CR-BP-NN` with
    uppercase letter suffix (legacy `CR-BP-03C`).
  - **Metadata line pattern** admits both `**Key**: value`
    (canonical) and `**Key:** value` (legacy / GitHub-issues).
  - **JSON output** includes `new_findings` and
    `legacy_findings` arrays + `cutoff_date`.
  - Self-test extended with cutoff-aware good and bad fixtures.
- `change-requests/CR-BP-03C-sample-process-contribution.md`:
  added `**Layer**: L1` + `**Owner**: TechNeHub Labs`.
- `change-requests/CR-BP-12-process-group-profile.md`:
  bolded existing metadata + added Layer/Owner.
- `change-requests/CR-BP-14-process-semantic-reconciliation.md`:
  added full §21 metadata block (Status, Layer, Owner, Type,
  Scope, Depends On).
- `change-requests/CR-BP-15-process-catalog-reconciliation.md`:
  added full §21 metadata block.
- `change-requests/CR-BP-16-process-catalog-conformance-gate.md`:
  added §21 metadata for both CR-BP-16 and CR-BP-15-IMP
  blocks.
- `reconciliation/baseline/v1.yaml`: refreshed SHA-256 for
  the 3 CRs whose content changed.
- `reconciliation/inventory.yaml`: regenerated to reflect the
  touched CRs.
- `.github/workflows/ci.yml`: CR-META step now runs
  `python scripts/check_cr_metadata.py --strict`.
- `docs/conformance-pipeline.md`: new "CR Validation (Step 9)
  cutoff policy" subsection documents the policy.
- `tests/test_cr_bp16_gates.py` (extended, 5 new tests):
  - `test_cr_meta_strict_passes_when_no_new_failures`:
    --strict returns 0 when no NEW CR fails.
  - `test_cr_meta_strict_fails_on_new_bad_fixture`: --strict
    fails on a future-dated bad fixture.
  - `test_cr_meta_strict_passes_on_legacy_bad_fixture`:
    --strict passes on a past-dated bad fixture.
  - `test_cr_meta_accepts_layer_with_parenthetical_qualifier`:
    `L1 (Process Catalog)` normalised to `L1`.
  - `test_cr_meta_accepts_status_with_date_qualifier`:
    `Proposed (2026-09-03)` normalised to `Proposed`.

CR-BP-16 §29 acceptance criteria: **11 fully met** (up from 10);
1 partial (provenance schema validation only); 0 unmet.

Conformance Result on the new branch: **CONFORMANT**
BP-SEM live: 0 errors, 0 warnings: CONFORMANT
BP-AR live: 0 findings: CONFORMANT
Conformance Levels: 38/38 at Level 4
CR-META on the new branch: ADVISORY-LEGACY (24 legacy findings,
0 new findings); --strict returns 0.

### CR-BP-16 conformance pipeline (S17/S18/S19/S25) + unified Conformance Result

The CR-BP-16 §17 CI Conformance Pipeline, §18 unified
Conformance Result, §19 blocking-conditions mapping, and
§25 continuous-conformance triggers are now live. Every PR
receives a single CONFORMANCE RESULT verdict that aggregates
all 10 pipeline steps.

- `docs/conformance-pipeline.md` (new, 153 lines): documents
  the 10-step pipeline (Schema, Structure, References,
  Semantics, Hierarchy, Specialization Graph, MECE, Provenance,
  CR Validation, Conformance Result), the blocking-vs-advisory
  matrix, the §19 blocking-conditions mapping (13 conditions),
  and the §25 continuous-conformance triggers. Closes D7
  (the missing visitor-facing pipeline doc).
- `scripts/conformance_result.py` (new, 162 lines): runs all
  15 gates (10 blocking + 5 advisory) and produces a single
  CONFORMANCE RESULT verdict. Verdict is one of CONFORMANT,
  CONFORMANT-WITH-WARNINGS, or NON-CONFORMANT (CR-BP-16 §18).
  `--json` mode emits a structured report. `--strict` treats
  advisory failures as blocking.
- `.github/workflows/ci.yml`: new "Aggregate Conformance
  Result (CR-BP-16 §17/S18)" step runs after the per-gate
  steps. The aggregated verdict is the canonical pre-merge
  source.
- `docs/conformance.md`: links to `docs/conformance-pipeline.md`
  in the See Also block.
- `tests/test_conformance_result.py` (new, 7 tests): verdict
  on live, JSON shape, --strict propagation, pipeline doc
  existence + coverage of all 10 steps, all 13 §19 blocking
  conditions, and all 7 §25 continuous-conformance triggers.

Conformance Result on main: **CONFORMANT**
BP-SEM live: 0 errors, 0 warnings: CONFORMANT
BP-AR live: 0 findings: CONFORMANT
Conformance Levels: 38/38 at Level 4

### CR-BP-16 full conformance gate: S10/S15/S16/S22 machinery

The remaining CR-BP-16 sections called out in §29 acceptance
criteria are now live as CI machinery (advisory). The catalogue
remains **38/38 Level 4 (Canonically Conformant)** and **0
BP-SEM / BP-AR findings**.

- `scripts/check_process_semantics.py` (extended):
  - New rule **BP-SEM-014 Specialization Cycle Detection**
    (CR-BP-16 S10). The specializes graph MUST be acyclic;
    self-specialization and any cycle (A -> B -> ... -> A) are
    architectural regressions. Module docstring updated to
    document BP-SEM-014 alongside BP-SEM-001..013. Self-test
    extended with a cycle fixture.
- `scripts/check_cr_metadata.py` (new): CR-BP-16 S16 metadata
  validator. Six rules (CR-META-001..006) check that every
  architectural CR carries **Status**, **Layer**, **Owner**,
  **Depends on** (with CR-BP-NN refs), **Companion to**, and a
  filename matching the CR-BP-NN pattern. **Advisory** mode:
  legacy CRs lack S21 metadata; CR-BP-13A is the planned first
  CR to demonstrate full S21 compliance.
- `scripts/check_documentation_conformance.py` (new): CR-BP-16
  S22 normative terminology consistency checker. Three rules
  (DOC-001..003) flag legacy synonym usage without the preferred
  term, unresolvable canonical id references, and standalone
  'Process' usage outside compound forms. **Advisory** mode.
- `scripts/check_admission_gate.py` (new): CR-BP-16 S15 new-
  process admission gate. Eight rules (ADM-001..008) check
  Evidence coverage (admission CR in change_history), Identity
  shape, Context resolution, Group fit, Boundary completeness
  (triggers, outcomes), Intent+Classification in approved
  vocabularies, Specialization validity, and Provenance shape.
  **Advisory** mode: surfaces findings on the locked population
  for review.
- `.github/workflows/ci.yml`: new "Run CR metadata gate" step
  (advisory); new "Run documentation conformance gate" step
  (advisory); new "Run admission gate" step (advisory).
- `tests/test_check_process_semantics.py`:
  - New `test_bp_sem_014_detects_cycle`: confirms BP-SEM-014
    fires on a 2-record cycle.
  - New `test_bp_sem_014_rejects_self_specialization`: confirms
    BP-SEM-014 fires on self-specialization.
  - Parametrized rule-coverage test extended for BP-SEM-014.
- `tests/test_cr_bp16_gates.py` (new, 11 tests): CR metadata,
  documentation conformance, and admission gate tests.

BP-SEM live verdict: 0 errors, 0 warnings: CONFORMANT
BP-AR live verdict: 0 findings: CONFORMANT
CR-META live verdict: 46 findings across 16 CR files (advisory;
legacy CRs lack S21 metadata)
DOC live verdict: 436 findings across many docs files (advisory;
docs cleanup is a separate programme item)
ADM live verdict: 54 findings across 18 Process records (advisory;
boundary + provenance fields are recommended, not required)
Conformance Levels: 38/38 at Level 4

**CR-BP-16 §29 acceptance criteria update:**
- [x] CI executes structural validation (was already PASS in PR-31)
- [x] CI executes semantic validation (BP-SEM; PR-29 + PR-36)
- [x] CI validates specialization graphs (BP-SEM-013 + BP-SEM-014;
  PR-37 + this PR)
- [x] CI validates references (BP-SEM-008; PR-31)
- [x] Architectural regression patterns are detected (BP-AR-001..007;
  PR-38)
- [x] CI validates CR metadata (CR-META-001..006; this PR)
- [x] Conformance results reproducible (--check modes; PR-38)
- [x] Canonical status tied to conformance + governance (Level 4;
  PR-38)
- [x] Gate does not equate ECF coverage with process completeness
  (BP-SEM-008; PR-31)
- [partial] CI validates provenance (gate machinery live; full
  change_history schema validation is a separate item)
- [partial] New-process admission has mandatory conformance path
  (gate machinery live; mandatory enforcement requires CR-BP-13A
  to land first as the pilot)
- [partial] Documentation describes the gate (gate machinery live;
  docs walkthrough is a separate programme item)

### CR-BP-15-IMP Phase 7: Pre-admission readiness

The permanent CR-BP-16 conformance gate machinery is now live:
the seven architectural regression patterns (BP-AR-001..007)
and the per-record conformance report (CR-BP-16 S23/24 Levels
1-4) are both running in CI. The catalogue is **38/38 Level 4
(Canonically Conformant)**.

- `scripts/check_architectural_regression.py` (new): the seven
  architectural regression patterns from CR-BP-16 S21 are now a
  blocking CI gate. Each pattern forbids conflation of two
  semantic concepts:
  - BP-AR-001: Business Process != Process Kernel
  - BP-AR-002: ECF Coordinate != Business Process
  - BP-AR-003: Process Group != Business Function
  - BP-AR-004: Capability != Process
  - BP-AR-005: Audience != Context (also catches reintroduction
    of legacy `process_audience` scalar)
  - BP-AR-006: Intent != Classification (also scans
    specialization_pattern / specialization_basis)
  - BP-AR-007: Specialization != Decomposition (catches
    same-context `specializes` relationships)
  Supports `--strict`, `--json`, `--self-test` (5 of 7 patterns
  are unit-tested via fixtures; the Process Group / Capability
  patterns are field-level and don't surface in the canonical
  data structure).
- `scripts/build_conformance_report.py` (new): generates
  `reconciliation/conformance_report.yaml` from the live
  catalogue. Each record is assigned a Conformance Level:
  - Level 0: Unassessed
  - Level 1: Structurally Conformant (schema + references)
  - Level 2: Semantically Conformant (BP-SEM clean)
  - Level 3: Architecturally Conformant (BP-AR clean)
  - Level 4: Canonically Conformant (evidence + governance)
  Supports `--check` to assert the report is up to date.
- `reconciliation/conformance_report.yaml` (new, generated):
  38 records, all Level 4 (Canonically Conformant).
- `.github/workflows/ci.yml`: new "Run architectural regression
  gate" step (blocking); new "Refresh conformance report" step
  (advisory). CI now runs BP-AR + report refresh on every PR.
- `tests/test_architectural_regression.py` (new): 7 tests
  covering the self-test, live conformance, JSON shape,
  canonical-bad fixture rejection, and report invariants.

BP-SEM live verdict: 0 errors, 0 warnings: CONFORMANT
BP-AR live verdict: 0 findings: CONFORMANT
Conformance Levels: {0: 0, 1: 0, 2: 0, 3: 0, 4: 38}

**Pre-admission readiness:** the §24 admission freeze can now
be lifted as soon as CR-BP-13A / CR-BP-13B admission tranches
are ready, because the BP-AR-001..007 gate will catch
architectural regressions at PR time. Phase 7 closes the
readiness loop opened by Phase 1-6.

### CR-BP-15-IMP Phase 6: Specialization machinery (machinery-only)

The BP-SEM-013 specialization-relationship validation rule is now
live, but **zero `specializes` relationships are introduced** on
the canonical 18 records. Phase 6 is machinery-only.

- `scripts/check_process_semantics.py` (modified):
  - New rule **BP-SEM-013** validates `relationships[]` entries
    with `relationship_type: specializes`. A valid specializes
    relationship MUST: target a canonical Process entry; carry a
    `specialization_pattern` from the approved basis vocabulary
    or a non-empty `specialization_basis` field; resolve to an
    existing Process entry.
  - Module docstring updated to document BP-SEM-013 alongside
    BP-SEM-001..012.
  - Self-test extended: broken fixture carries an unresolved
    specializes target (must fail); fixed fixture carries a
    valid specializes with approved basis (must pass).
- `tests/test_check_process_semantics.py`:
  - New `test_bp_sem_013_rejects_unresolved_specializes_target`:
    confirms BP-SEM-013 fires on an unknown target.
  - New `test_bp_sem_013_accepts_valid_specializes`: confirms
    BP-SEM-013 passes on a valid canonical-fan-out.
  - Parametrized rule-coverage test extended for BP-SEM-013.
- `reconciliation/dispositions/register.yaml`: `phase6_status`
  section added; `specializations_introduced: 0`,
  `validation_mode: machinery-only`, `bp_sem_013_rule_added:
  true`, with rationale documented inline.

**Why no specializations introduced:** CR-BP-14 S23 semantics
distinguish specialization (cardinality fan-out under a
controlled pattern like `by-customer-segment`) from
decomposition (sequential work within a single context, using
`composes`). Every candidate pair examined in Phase 6 planning
- `customer-journey-design` + `customer-experience-design`
  (cd-d);
- `design-policies-and-controls` + `design-governance-system`
  (ge-d);
- `market-and-demand-conception` + `customer-strategy-conception`
  (cd-c);
- is sequential decomposition, not cardinality fan-out. The
  CR-BP-14 S24 admission freeze prevents new admission
  tranches that would introduce clean fan-out candidates
  (e.g., `manage-enterprise-customer` specializing
  `manage-customer-relationship` under `by-customer-segment`).

**Future work:** Phase 7 (or the first post-freeze admission
tranche) will exercise BP-SEM-013 against a real fan-out
candidate. The machinery is in place; the canonical evidence
  will arrive when admission resumes.

BP-SEM live verdict: **0 errors, 0 warnings: CONFORMANT**
(no live records have `specializes` relationships, so BP-SEM-013
has no input to flag).

### CR-BP-15-IMP Phase 5 fourth tranche (ge-op) + Phase 5 closure

The final two governance-existence operate records have been
reconciled to the CR-BP-14 canonical contract. The disposition
register is now LOCKED (18/18). **The CR-BP-15-IMP Phase 5 loop
is complete.**

- `entities/v1-alpha/dea:process-audit-policy-compliance/`
  (ge-op): legacy `support` intent -> canonical `govern`
  (audit-and-oversight is governance activity); audience-vs-context
  high-risk flag resolved by removing `process_audience`
  (canonical `context: [{ref: dea:pc-ge-op}]` replaces it);
  serves toward `ecf:governanceAndExistence.operate`.
- `entities/v1-alpha/dea:process-operate-governance-oversight/`
  (ge-op): legacy `management` intent -> canonical `operate`;
  same ge-op migration pattern.
- `contexts/v1-alpha/dea_pc-pr-op.yaml` -> `dea-pc-pr-op.yaml`
  (filename typo fixed; canonical id `dea:pc-pr-op` was always
  correct inside the file). Updated 4 documentation references
  (CR-BP-03C + CR-BP-12 + manage-customer-relationship.md +
  CHANGELOG). The BP-SEM-008 context-reference-integrity check
  now passes.
- `reconciliation/diffs/phase-5-ge-op.yaml` (new): per-tranche
  audit trail; 2 records touched; closure observations on the
  audience-vs-context resolution and the filename correction.
- `reconciliation/dispositions/register.yaml`: register_status
  -> LOCKED; register_lock_progress records all 10 tranches and
  18 locked records; 0 remaining.
- `.github/workflows/ci.yml`: Process Semantics gate promoted
  from advisory (`--strict || true`) to **blocking** (`--strict`).
  Any future regression on the canonical CR-BP-14 contract is
  caught at PR time.
- `tests/test_reconciliation_baseline.py`: legacy_findings_present
  test updated to reflect the all-locked state (0 remaining,
  not 2).
- `tests/test_apply_phase_5_tranche.py`: register_lock_progress
  test now asserts the LOCKED status of the disposition register
  and the 18-of-18 lock progress.
- `tests/test_check_process_semantics.py`: live --strict test
  updated to assert CONFORMANT (0 errors, 0 warnings) on the
  post-Phase-5 catalogue. Added `test_strict_mode_fails_on_
  legacy_fixture` to lock the strict-mode machinery against a
  synthetic legacy-bearing sandbox.

BP-SEM live verdict: **0 errors, 0 warnings: CONFORMANT**
for the first time since CR-BP-14 S21 was introduced.

### CR-BP-15-IMP Phase 5 third tranche (ge-b + ge-c + ge-d + ge-im)

Seven governance records have been reconciled to the CR-BP-14
canonical contract. The disposition register is now 16-of-18
locked.

- `entities/v1-alpha/dea:process-codify-charters-and-policies/`
  (ge-b): legacy `operational` intent -> canonical `operate`;
  ge-b context block; serves toward
  `ecf:governanceAndExistence.build`.
- `entities/v1-alpha/dea:process-establish-governance-bodies/`
  (ge-b): legacy `operational` intent -> canonical `operate`;
  same ge-b migration pattern.
- `entities/v1-alpha/dea:process-develop-governance-strategy/`
  (ge-c): legacy `management` intent -> canonical `develop`;
  ge-c block; serves toward `ecf:governanceAndExistence.conceive`.
- `entities/v1-alpha/dea:process-initiate-policy-and-charter/`
  (ge-c): legacy `management` intent -> canonical `manage`;
  same ge-c pattern; serves toward
  `ecf:governanceAndExistence.conceive`.
- `entities/v1-alpha/dea:process-design-governance-system/`
  (ge-d): legacy `management` intent -> canonical `develop`;
  ge-d block; serves toward `ecf:governanceAndExistence.design`.
- `entities/v1-alpha/dea:process-design-policies-and-controls/`
  (ge-d): legacy `management` intent -> canonical `develop`;
  same ge-d pattern.
- `entities/v1-alpha/dea:process-review-governance-effectiveness/`
  (ge-im): legacy `management` intent -> canonical `govern`
  (review-and-correction is governance activity per the
  disposition register rationale); ge-im block; serves toward
  `ecf:governanceAndExistence.improve`.
- `reconciliation/diffs/phase-5-ge-b-ge-c-ge-d-ge-im.yaml`
  (new): per-tranche audit trail; 7 records touched;
  cross-tranche observations on ge-c intent diversity,
  ge-d as L2 conceptual foundation, ge-im as single-record
  Improve context work.
- `reconciliation/dispositions/register.yaml`: register_lock
  progress updated to 16 locked records (cd-b, cd-c, cd-d,
  cd-im, cd-op, ge-b, ge-c, ge-d, ge-im) and 2 remaining
  (the ge-op records; PR-9 next).
- `tests/test_reconciliation_baseline.py`: legacy_findings_present
  test updated to reflect the third tranche lock (2 remaining,
  not 9).
- `tests/test_apply_phase_5_tranche.py`: register_lock_progress
  test expanded to cover the four governance tranches.

BP-SEM live verdict: 2 errors (down from 9). Only the two
ge-op records remain.

### CR-BP-15-IMP Phase 5 second tranche (cd-d + cd-im + cd-op)

Five additional party-relationship records have been reconciled to
the CR-BP-14 canonical contract. The disposition register is now
9-of-18 locked.

- `entities/v1-alpha/dea:process-customer-experience-design/`:
  legacy `management` intent -> canonical `develop`; cd-d context
  block; serves toward `ecf:customerAndDemand.design`.
- `entities/v1-alpha/dea:process-customer-journey-design/`:
  legacy `support` intent -> canonical `develop`; same cd-d
  migration pattern.
- `entities/v1-alpha/dea:process-demand-design/`: legacy
  `management` intent -> canonical `develop`; same cd-d
  pattern.
- `entities/v1-alpha/dea:process-customer-insight-and-retention/`:
  legacy `management` intent -> canonical `operate` (Improve
  context work is operational); cd-im block; serves toward
  `ecf:customerAndDemand.improve`.
- `entities/v1-alpha/dea:process-manage-customer-relationship/`:
  legacy `management` intent -> canonical `manage`; cd-op block;
  serves toward `ecf:customerAndDemand.operate`. The existing
  `realizes` capability relationship is preserved.
- `reconciliation/diffs/phase-5-cd-d-cd-im-cd-op.yaml` (new):
  per-tranche audit trail; 5 records touched; cross-tranche
  observations on cd-d density and the management-vs-manage
  intent disambiguation.
- `reconciliation/dispositions/register.yaml`: register_lock
  progress updated to 9 locked records (cd-b, cd-c, cd-d,
  cd-im, cd-op) and 9 remaining.
- `tests/test_reconciliation_baseline.py`: legacy_findings_present
  test updated to reflect the second tranche lock (9 remaining,
  not 14).

BP-SEM live verdict: 9 errors (down from 14). Half of the
party-relationship records now conform to the canonical contract.

### CR-BP-15-IMP Phase 5 first tranche (cd-b + cd-c)

The first two party-relationship tranches (4 records: 2 build + 2
conceive) have been reconciled to the CR-BP-14 canonical contract.
The disposition register is now PARTIALLY_LOCKED with 4 records
locked.

- `entities/v1-alpha/dea:process-customer-channel-and-acquisition-build/`:
  legacy `operational` intent -> canonical `operate`; legacy
  scalar `process_context: dea:pc-pr-b` -> canonical
  `context: [{ref: dea:pc-pr-b}]` block; legacy
  `process_audience: party-relationship` removed; canonical `serves`
  relationship toward `ecf:customerAndDemand.build` added;
  change_history entry appended.
- `entities/v1-alpha/dea:process-demand-generation-build/`: same
  migration as the cd-b peer (operate + dea:pc-pr-b + serves).
- `entities/v1-alpha/dea:process-customer-strategy-conception/`:
  legacy `management` intent -> canonical `develop`; cd-c
  context; serves toward `ecf:customerAndDemand.conceive`.
- `entities/v1-alpha/dea:process-market-and-demand-conception/`:
  same migration as the cd-c peer.
- `reconciliation/diffs/phase-5-cd-b-cd-c.yaml` (new): per-tranche
  audit trail; 4 records touched; SHA-256 evolution recorded;
  cross-tranche observations.
- `reconciliation/dispositions/register.yaml`: register_status
  -> PARTIALLY_LOCKED; register_lock_progress records 4 locked
  records and 14 remaining.
- `schemas/entity.schema.json`: `process_audience` removed from
  the `required` list; the legacy field remains readable as a
  backward-compat alias (CR-BP-14 /19) but is no longer
  required for canonical entries.
- `scripts/apply_phase_5_tranche.py` (new): reproducible tranche
  migration script; supports `--self-test` (idempotence contract)
  and `--tranche <id>` for any of the 10 tranches; applies the
  full migration pattern (intent, audience removal, context
  block, serves relationship, change_history append).
- `tests/test_apply_phase_5_tranche.py` (new): 8 tests covering
  the migration script + per-record shape + idempotence + lock
  progress.
- `tests/test_reconciliation_baseline.py`: legacy_findings_present
  test updated to reflect the Phase 5 first-tranche lock (14
  remaining, not 18).

Programme position: CR-BP-14 still **Implemented**; CR-BP-15 +
CR-BP-15-IMP still **Proposed**; this PR is the fourth
CR-BP-15-IMP delivery and the first Phase 5 tranche migration.

BP-SEM live verdict: 14 errors (down from 18). The 4 migrated
records no longer trigger BP-SEM-007 (canonical context: block
required).

### CR-BP-15-IMP Phase 3-4: Disposition register + tranche plan

CR-BP-15 §28 (the ten dispositions) is now formalised; the 18
Business Processes in the canonical catalogue each receive a
preliminary RECLASSIFY disposition. The 18 records are grouped
into 10 tranches (one per Process Context) so future CR-BP-15-IMP
Phases 5-7 migrations are sequenced.

- `reconciliation/dispositions/schema.yaml` (new): the canonical
  disposition schema; 9 dispositions (RETAIN, RECLASSIFY, RENAME,
  SPECIALIZE, MERGE, SPLIT, MOVE, DEFER, RETIRE) each with
  required/optional fields, target_id requirement, and a
  rationale pattern; the reclassify_axes block documents the
  CR-BP-14 §17 migration mapping.
- `reconciliation/dispositions/register.yaml` (new, PRELIMINARY):
  18 disposition entries (one per Business Process); every
  entry is RECLASSIFY at this stage because every record carries
  the documented legacy fields; rationale + evidence recorded
  per entry; the register will be LOCKED in CR-BP-15-IMP
  Phase 5 (PR-6 onward).
- `reconciliation/tranches/plan.yaml` (new): 10 tranches (cd-b,
  cd-c, cd-d, cd-im, cd-op, ge-b, ge-c, ge-d, ge-im, ge-op); two
  are flagged high-risk (ge-b: audience-vs-context; ge-op:
  cross-tranche references); per-tranche PR target, owner
  placeholder, and review checkpoints recorded.
- `reconciliation/README.md`: orientation block extended to
  describe Phases 3-4 layout and Phase 5-7 roadmap.
- `scripts/check_dispositions.py` (new): disposition validator
  with --self-test; checks that every record has exactly one
  disposition entry, that every disposition id is canonical,
  that RECLASSIFY changes conform to the CR-BP-14 axes and
  vocabularies, that context targets resolve to the Process
  Context register, and that the tranche plan covers every
  disposition entry.
- `tests/test_dispositions.py` (new): 9 tests covering the
  disposition validator + register + tranche plan.
- `.github/workflows/ci.yml`: Disposition register step added
  (advisory until the register is LOCKED).

Programme position: CR-BP-14 still **Implemented**; CR-BP-15 +
CR-BP-15-IMP still **Proposed**; this PR is the third
CR-BP-15-IMP delivery.

### CR-BP-15-IMP Phase 1-2: Inventory + immutable baseline

CR-BP-15 §6 / §7 (existing-population reconciliation) is now
seeded. The Phase 1 inventory enumerates every canonical record at
the moment CR-BP-14 was declared Implemented; the Phase 2 baseline
freezes each record's SHA-256 so future tranches can diff exactly
which bytes were touched.

- `reconciliation/inventory.yaml` (new): 18 Business Processes +
  10 Process Groups + 10 Process Contexts + 4 Change Requests
  (CR-BP-14, CR-BP-15, CR-BP-15-IMP, CR-BP-16); per-record
  metadata + `legacy_findings` (BP-SEM raw findings on each
  record).
- `reconciliation/baseline/v1.yaml` (new): immutable SHA-256
  snapshot of every record's file contents; baseline_version = v1;
  baseline_commit = 816c63b (CR-BP-14 Implemented); baseline_at =
  2026-09-06.
- `reconciliation/README.md` (new): orientation for visitors;
  layout, phase progression, STRUCT conformance reference.
- `scripts/build_inventory.py` (new): reproducible generator;
  `--self-test --strict` asserts byte-identity with committed
  files; supports `--out` for diff scenarios.
- `scripts/check_struct.py` (new, decision D6): STRUCT conformance
  check that flags unknown top-level entries; intentionally
  permissive (the catalogue's contracts own schema integrity);
  wired into CI as an advisory step.
- `tests/test_reconciliation_baseline.py` (new): 9 tests covering
  inventory regeneration, baseline SHA-256 integrity, and STRUCT
  typo detection.
- `.github/workflows/ci.yml`: STRUCT conformance step added
  between Legacy Migration gate and Process Semantics gate.

Programme position: CR-BP-14 still **Implemented**; CR-BP-15 +
CR-BP-15-IMP still **Proposed**; this PR is the first CR-BP-15-IMP
delivery.

### CR-BP-14 Phase 4: Documentation reconciliation (Implemented)

CR-BP-14 §22 is now satisfied. The repository prose reflects the
CR-BP-14 semantic contract; legacy vocabulary references are
reconciled to the canonical forms or marked historical; no
superseded semantic contract remains presented as normative.

- `docs/architecture.md`: oriented (links to the semantic-contract
  and governance documents); L0/L1/L2 narratives rewritten to the
  CR-BP-14 §6 / §7 definitions; Process Group confirmed as catalog-
  owned, not a metamodel entity; See-also expanded.
- `docs/identity.md`: identity-independence clause added (CR-BP-14
  §15); BP-ARC-ID-004 cross-check note clarifies its distinction from
  BP-SEM-003/004; See-also expanded; broken `../../` link defect
  swept.
- `docs/classification.md`: front matter records the CR-BP-14 §10 /
  §11 formal separation; the canonical `classifications/process-intents.yaml`
  link is now correct (the pre-existing `../../classifications` link
  defect is swept); See-also expanded.
- `docs/relandscape.md`: See-also expanded with the semantic-
  contract document and the BP-SEM validator; CR-BP-14 §24
  admission-freeze reference added; broken `../../` link defect
  swept.
- `docs/context.md` (new): Process Context as canonical placement
  (CR-BP-14 §5, §13, §20); the canonical `context:` block;
  multiplicity rule; the Process Context register at
  `contexts/v1-alpha/`; relationship to BP-SEM-007 and BP-SEM-008.
- `docs/specialization.md` (new): specialization as semantic
  refinement (CR-BP-14 §12); approved specialization bases;
  specialization vs decomposition; canonical form; identity
  independence (BP-SEM-009).
- `README.md` §2 (Process Architecture): the four-axes table is
  replaced with the CR-BP-14 axes (Intent / Classification /
  Specialization / Context); the obsolete `Audience` axis is replaced
  by the canonical `context:` block; §8 No Breaking Changes explains
  the migration-period field aliasing.

Register close-out: **CR-BP-14 -> Implemented** (the constitutional
phase is complete; CR-BP-15-IMP owns the existing-population
migration; CR-BP-16 owns the permanent gate).

### CR-BP-14 Phase 3: BP-SEM-001..012 Process Semantics gate

- `scripts/check_process_semantics.py` (new): implements BP-SEM-001
  (Intent Vocabulary), BP-SEM-002 (Classification Vocabulary),
  BP-SEM-003/004 (Intent/Classification Independence by construction),
  BP-SEM-005 (Specialization Validity), BP-SEM-006 (Specialization
  Differentiation), BP-SEM-007 (Context Distinction), BP-SEM-008
  (Context Reference Integrity), BP-SEM-009 (Identity Independence by
  construction), BP-SEM-010 (Legacy Detection), BP-SEM-011
  (Classification Collision, advisory), BP-SEM-012 (Context
  Multiplicity, advisory). Each finding carries a deterministic
  `rule:<code>` prefix; warnings never block unless `--strict`.
- `--self-test` exercises every BP-SEM rule on a broken fixture and
  asserts the fixed fixture is blocking-free with the expected advisory
  findings.
- Wired into CI as an advisory step between the legacy migration gate
  and the process group gate (`--strict || true`): the current
  canonical population carries CR-BP-14 S24 admission-freeze findings
  (legacy process_intent, legacy scalar process_context, missing
  canonical `context:` block, legacy process_audience); the validator
  surfaces them and CR-BP-15-IMP Phases 8..10 reduces them.
- New `tests/test_check_process_semantics.py` (16 tests) locks the
  self-test, docstring coverage of every code, and the live/strict
  verdict contract.
- The live run finds: 18 entries missing the canonical `context:`
  block (BP-SEM-007); all 18 carry legacy `process_intent` or legacy
  `process_audience` (BP-SEM-010); all 18 carry the legacy scalar
  `process_context` (BP-SEM-010). These are exactly the seed findings
  already documented in the CR-BP-14/15/16 programme plan.

### CR-BP-14 Phase 2: Process Context block and contextual relationships

- `context:` block added to `schemas/entity.schema.json` and
  `schemas/contribution.schema.json` (CR-BP-14 §13, §20): an array of
  `{ref: dea:pc-*}` Process Context references; multiple contexts are
  permitted where evidence justifies them (BP-SEM-012).
- `relationship_type` enum extended with `serves` and `contributes-to`
  (both admitted by the metamodel relationship registry; catalog-governed
  extension, no metamodel CR required). `operates-within` is deliberately
  absent: its semantics are carried by the `context:` block.
- `target_id` now admits canonical ECF identifiers
  (`ecf:<lowerCamelDomain>[.<lowerCamelStage>]`, the CG-003 form)
  alongside entity ids; the entity-id branch excludes the `ecf:` prefix
  so the kebab-case label form is rejected (consistent with CG-004 §10).
- Contribution template updated: the canonical `context:` block replaces
  the pre-CR-BP-14 `process_context` scalar; a `serves` relationship
  example toward an ECF coordinate is included.
- New `tests/test_process_context_relationships.py` (16 tests) locks the
  block shape, enum extension, target patterns, and backward
  compatibility of all existing canonical entries.
- Recorded for CR-BP-15-IMP Phase 10: existing entries carry a legacy
  scalar `process_context` field that predates the canonical block; the
  schema remains permissive toward it until the audience/context
  migration.

### CR-BP-15 + CR-BP-16 landing and knowledge harvest

- CR-BP-15 (Process Catalog Reconciliation) and CR-BP-16 (Process
  Catalog Conformance Gate, carrying CR-BP-15-IMP) landed verbatim at
  `change-requests/CR-BP-15-process-catalog-reconciliation.md` and
  `change-requests/CR-BP-16-process-catalog-conformance-gate.md`.
- New visitor-facing documentation distilled from the CR lineage:
  `docs/semantic-contract.md` (the semantic constitution: six
  characterization dimensions, controlled vocabularies, the normative
  separations) and `docs/governance/reconciliation-programme.md` (the
  closed governance loop, CR lineage, reconciliation dispositions,
  conformance levels, repository status model).
- README gains a "Reading This Repository" orientation block.
- CR register + README change programme: CR-BP-15 and CR-BP-16 rows
  added as Proposed; CR-BP-14 row updated to reflect Phase 1 (PR #26).

### CR-BP-14: Process Semantic Reconciliation (landing + Phase 1)

Landing (PR #25):
- CR landed verbatim at
  `change-requests/CR-BP-14-process-semantic-reconciliation.md`.
- CR register synchronized with actual status (CR-BP-14 §23): CR-BP-13b
  corrected to Merged (PR #24); README change programme rows synced for
  CR-BP-03/03A/03C/04/11/12/13/13a/13b; stale Activity Model / Execution
  Boundary placeholders renumbered as unnumbered future rows.

Phase 1 (semantic vocabularies + schema; CR-BP-14 §9, §10, §11, §17, §18, §20):
- New controlled vocabulary `classifications/process-intents.yaml`: the
  seven-value purpose-oriented Process Intent vocabulary (govern / manage /
  operate / deliver / support / develop / transform) with the §17 legacy
  migration mapping (operational -> operate or deliver; support -> support;
  management -> manage or govern; evidence-based, never mechanical).
- `schemas/entity.schema.json`: `process_intent` enum extended to the
  canonical seven values with legacy `operational` / `management` retained
  as deprecated migration aliases; new optional `process_classification`
  block (canonical form per §20); `process_type` retained unchanged as the
  landscape classification and backward-compatible alias (§18);
  `process_audience` marked as legacy migration alias (§13, §19).
- `schemas/contribution.schema.json` mirrors the same extensions.
- `classifications/process-types.yaml` header records the CR-BP-14 §10
  Process Classification semantics and the Intent != Classification rule
  (§11; BP-SEM-011).
- `scripts/check_process_specialization.py` BP-SPEC-01-007 text updated to
  quote the extended intent vocabulary; non-promotion rule unchanged.
- `docs/classification.md` gains a CR-BP-14 Phase 1 status section; the
  pre-CR-BP-14 prose is marked historical pending Phase 4 reconciliation.
- Contribution template updated to the canonical intent vocabulary with the
  optional `process_classification` block shown.
- New `tests/test_process_intents.py` locks vocabulary / schema mirror
  integrity.

### CR-CATALOG-STRUCT-02: Process Catalog Adoption (Three-Step Migration)

Brings `dea-catalog-processes` into conformance with the catalog repository
standard (CR-CATALOG-STRUCT-01).

Step 1 (layout):
- `entities/v1-alpha/dea:process-manage-customer-relationship/{research,candidates,retired}/`
  subtree created; canonical file moved from `dea_bp_manage-customer-relationship.yaml`
  and renamed to canonical `dea:process-*` form (CR-BP-04).
- `entities/v1-alpha/dea:group-customer-lifecycle-management/{research,candidates,retired}/`
  subtree created; canonical file moved from `dea_group-customer-lifecycle-management.yaml`.

Step 2 (research distribution):
- `docs/research/l1-register.yaml`, `l1-candidate-universe.yaml`, `L1-REGISTER-v0.1.md`
  moved into `entities/v1-alpha/dea:group-customer-lifecycle-management/research/`
  (research is about L1 Process Groups; L1 entities own L1 evidence).
- `docs/research/` removed (empty after the move).
- Provenance `research/README.md` per subtree.

Step 3 (contribution flow):
- `contributions/processes/` intake queue and template kept as-is (catalog
  hosts one entity type; renaming is a future concern).

Catalog index + CI:
- `CATALOG.yaml` (machine-generated, 1.9 KB) committed.
- `TEMPLATE_VERSION` (`0.1.0`) written; matches the canonical template.
- `metamodel-pointer.yaml` extended with additive top-level metadata block
  (id/name/abbreviation/version/status/metamodel_version/description/owner);
  existing nested `metamodel:` and `catalog:` blocks unchanged.
- `scripts/regenerate_catalog.py`, `scripts/check_catalog_index.py`, and
  `catalog-index-schema/catalog-index-schema.json` vendored from
  `dea-metaframework/tools/` (CST-013/CST-014).
- `.github/workflows/ci.yml` updated to run the regenerator check, the
  gate, the per-file schema dispatch (with state-directory filter), the
  six existing catalog validators, and the cross-repo conformance suite.
- `scripts/check_ecf_conformance.py` fixed: skip files under
  `research/`, `candidates/`, `retired/` (state-directory files are not
  catalog entries and do not carry `ecfConformance`).

Verification:
- All 6 catalog validators PASS.
- Regenerator --check exits 0.
- Gate --strict exits 0.
- Conformance --strict: 16/16 CSTs passed, 0 warnings.
- Cross-repo contract satisfied; STRUCT-03..05 can adopt the same pattern.

### CR-BP-12: L1 Process Group Profile, Schema, and Validator

Lands the first-class Process Group record type. Process Group remains a catalog-owned record (NOT a metamodel entity). The canonical containment direction is `L1 group --composes--> L2 process`; the inverse `part-of` view is generated at query time per CR-002 §8 because the metamodel relationship-type enum does not currently admit `part-of`.

#### Added

- `schemas/entities/process-group.schema.json` — JSON Schema for Process Group entries. ID family: `dea:group-*` (CR-BP-04 §4).
- `classifications/process-group-kinds.yaml` — six-value controlled vocabulary (`end-to-end`, `functional`, `support`, `cross-cutting`, `governance`, `innovation`).
- `scripts/check_process_group.py` — validator enforcing PG-001..PG-008; includes `--self-test` mode.
- `entities/v1-alpha/dea_group-customer-lifecycle-management.yaml` — the first canonical Process Group record; promotes the `metadata.group` label that lived on `dea:process-manage-customer-relationship` into a governed first-class record with `process_group_kind: end-to-end`.
- New CI step in `.github/workflows/ci.yml` that runs `scripts/check_process_group.py` on every PR.

#### Changed

- `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml` loses the `metadata.group` block; the Process Group is now an external first-class record referenced via the Process Group's `composes` array.

#### Not changed

- Existing Process Context (`dea:pc-pr-op`), classifications, contribution template, and contribution report workflow remain as PR #17 + #18 + #19 landed them.
- No Process Group promotion to the OpenDEA Core metamodel (CR-BP-14, future, conditional).
- Process Group kinds vocabulary is closed; additions require a CR-BP-12 minor revision.

### CR-BP-04: Business Process Identity & ID-Family Reconciliation

Documentation-first CR. Locks the four canonical ID families used by the
catalog (`dea:process-*`, `dea:pc-*`, `dea:group-*`, `dea:scope-*`) and the
legacy-migration `dea:bp:*` colon-separated family. Resolves the apparent
`dea:bp-*` versus `dea:process-*` drift by collapsing it to three intentional
roles: (1) legacy-migration reference inside `legacy_ids` arrays; (2) canonical
Business Process id on live entities and Process Context references;
(3) validator self-test fixture, used only to exercise failure paths inside
`scripts/check_legacy_migration.py` and `scripts/check_process_identity.py`.

#### Added

- `change-requests/CR-BP-04-id-family-reconciliation.md` (the CR; 13 sections;
  Design Specification tone; no en/em dashes; locks the colon-vs-dash
  distinction for the legacy family).
- New section **Canonical ID families (CR-BP-04 §4)** in `docs/identity.md`,
  restating the four-family contract verbatim.

#### Not changed

- No schema change. `schemas/entity.schema.json`, `schemas/contribution.schema.json`,
  and `schemas/entities/process-context.schema.json` already conform to the
  rule this CR documents.
- No validator change. `check_process_identity.py`, `check_process_context.py`,
  `check_legacy_migration.py`, and `check_ecf_conformance.py` already enforce
  the rule this CR documents.
- No entity change. No live catalog content uses the `dea:bp-*` dash form as
  a canonical identifier.
- No migration script. The `dea:bp-bad-*`, `dea:bp-parent`, and `dea:bp-child-*`
  validator fixtures remain as synthetic broken-input examples.

### CR-BP-11: L1 Process Group Discovery Across the 49 ECF Coordinates

Research-only register. Establishes a comprehensive L1 Process Group
discovery across the 7x7 ECF matrix (49 coordinates). Records an explicit
disposition per coordinate: 38 `accepted`, 11 `deferred`. Five cross-domain
findings are recorded once at their primary coordinate and referenced from
peer coordinates (Technology Management held unmapped; Change Management
cross-cutting at governance-existence x improve; Partner Management
dual-home at party-relationship x conceive; Resilience/Innovation/Analytics
at their primary coordinates; Marketing distinct from Customer Management).

The register is the input gate for CR-BP-12 (L1 Process Group profile +
schema + validator) and CR-BP-13..BP-19 (seven-domain admission tranches).
No canonical L1 records, no new schema, no new validator, no new CI
surface are added in this CR. The existing canonical L2 entry
(`dea:process-manage-customer-relationship`) remains the only canonical
Process entity in the catalog.

Process Group remains a catalog-owned record type, not an OpenDEA Core
metamodel entity. The canonical containment direction is
`L1 group --composes--> L2 process`; the inverse `part-of` is a derived
query view. Process Group and Business Function are explicit distinct
catalog-topology constructs (not synonyms, not subtypes, not aliases).

#### Added

- `change-requests/CR-BP-11-l1-process-group-discovery.md` (the CR;
  19 sections; Design Specification tone; no en/em dashes).
- `docs/research/l1-register.yaml` (the 49-coordinate disposition
  register; machine-readable; each coordinate carries process_context,
  l1_candidates, l2_candidates, in_scope, out_of_scope, evidence,
  disposition, deferral_reason).
- `docs/research/l1-candidate-universe.yaml` (the L1 candidate
  universe; 102 candidates across 49 coordinates; five cross-domain
  findings).
- `docs/research/L1-REGISTER-v0.1.md` (persona-readable summary).

#### Not changed

- Existing canonical entries under `entities/v1-alpha/`, `contexts/v1-alpha/`,
  `contributions/processes/`, `docs/examples/`, `schemas/`, `scripts/`,
  `classifications/`, `.github/workflows/` remain as PR #17 landed them.
- No `dea:bp-*` versus `dea:process-*` ID-family reconciliation happens
  here; that is a separate CR-BP-04.

### CR-BP-03C: Sample Business Process Contribution (walk-the-flow)

Lands the **first** Business Process entry in the catalog,
walking the full CR-BP-03 / CR-BP-03A / CR-BP-02 flow
end-to-end. The sample entry — `dea:bp:manage-customer-relationship`
("Manage Customer Relationship") — exercises every part of
the machinery:

  - 4-axis classification (intent / type / specialization /
    audience), all populated.
  - Process Identity contract (verb + object + outcome +
    evidence; BP-ARC-ID-001..005 PASS).
  - Canonical relationships (array-of-relationship-instances
    per metamodel relationship-instance.json; one realizes
    relationship to `dea:entity-capability:manage-customer-relationship`).
  - L0/L1/L2 conceptual hierarchy (Scope and Group recorded
    in metadata; NOT promoted to separate catalog entities
    per CR-BP-03 §3).
  - Process Context reference (the entry belongs to the
    PartyAndRelationship × Operate cell at
    `dea:pc-pr-op`).
  - ECF Conformance Gate (inherits-catalog; canonical
    references resolve to `ecf:partyRelationship.operate`;
    extensions declare `doesNotRedefine: true`).
  - Process Identity validator: case-insensitive + doubled-
    parentheses-tolerant fuzzy match (`_fuzzy_name_match`).

#### Added

- `change-requests/CR-BP-03C-sample-process-contribution.md`
  (md5 `0504cbca05a1875aac02137c959b7cab`; byte-identical to
  working folder `/home/hermes/dea-work/process/00_inbox/`).
- `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`
  (the canonical BP entry; first entry in the catalog;
  id `dea:process-manage-customer-relationship`).
- `contexts/v1-alpha/dea-pc-pr-op.yaml` (the Cell Charter for
  PartyAndRelationship × Operate; first Cell Charter in the
  catalog).
- `contributions/processes/dea_bp_manage-customer-relationship.yaml`
  (the contribution record; first contribution in the catalog).
- `contributions/processes/dea_bp_manage-customer-relationship.report.md`
  (the generated reclassification report; status=PASS,
  zero recommendations).
- `docs/examples/README.md` (introduction to the worked-
  examples directory).
- `docs/examples/manage-customer-relationship.md` (the
  worked example; future contributors should treat this
  as the canonical pattern).

#### Changed

- `scripts/check_process_identity.py`:
  - `_fuzzy_name_match` extended to be case-insensitive
    (entry names are conventionally Title Case; identity
    sub-block is conventionally lowercase).
  - `_fuzzy_name_match` extended to normalize doubled
    parentheses (e.g. `((all customer segments))` produced
    by wrapping a scope like `(all customer segments)`).
  - BP-ARC-ID-001: when the scope is already parenthesized,
    the validator does not wrap it again.
- `.github/workflows/process-contribution-report.yml`:
  - Reclassification report generator upgraded (CR-BP-03C §7)
    to cross-check the proposed_entry against BP-ARC-ID-001..005
    and emit a confidence-scored recommendation.
  - Includes migration check (BP-MIG-001..005) in the report
    pipeline.

#### Validators exercised (all PASS)

| Validator | Result |
|---|---|
| `check_process_identity.py` (BP-ARC-ID-001..005) | PASS |
| `check_process_identity.py --self-test` | PASS |
| `check_process_specialization.py` (BP-SPEC-01-001..007) | PASS |
| `check_process_context.py` (PC-001..PC-008) | PASS |
| `check_legacy_migration.py` (BP-MIG-001..005) | PASS |
| `check_legacy_migration.py --self-test` | PASS |
| `check_ecf_conformance.py` | PASS (1 entry conforms) |
| `validate_consumer.py` against `dea-architecture-framework@v0.6.0` | PASS |
| `jsonschema.validate(canonical_entry, entity_schema)` | PASS |
| `jsonschema.validate(cell_charter, process-context_schema)` | PASS |
| `jsonschema.validate(contribution, contribution_schema)` | PASS |
| Report generator (CR-BP-03C §7) | Generated report with status=PASS, 0 recommendations |

### CR-BP-03A: Legacy Field Migration

Resolves three issues with the CR-BP-03 schema that came to
light during implementation:

1. **`relationships` shape corrected** to array-of-relationship-
   instances (per the metamodel's `relationship-instance.json`).
   The CR-BP-03 shape was a structured object with
   `composes` / `realizes` keys; the authoritative metamodel
   shape is a flat array of typed relationship instances with
   full CR-002 provenance, CR-6 lifecycle, and effective_from/to
   temporal validity.
2. **`parent_process` / `child_processes` REMOVED** from the
   catalog schema. These were catalog inventions from CR-BP-01
   (the wrong-premise implementation, since reverted); the
   metamodel's `process.json` does not declare them.
3. **`capabilities_delivered` soft-deprecated**. The metamodel
   still declares this as a simple array of strings (a
   backward-compat shim). CR-BP-03A keeps the field in the
   catalog schema but marks it as soft-deprecated; the canonical
   form is `relationships[relationship_type=realizes]` with
   full provenance.

#### Added

- `change-requests/CR-BP-03A-legacy-migration.md` (md5
  `3e4a951008bf28e0b7d3bd325bcc2949`; byte-identical to working
  folder `/home/hermes/dea-work/process/00_inbox/`).
- `scripts/check_legacy_migration.py` — the migration validator
  enforcing BP-MIG-001..005 (with built-in `--self-test`).

#### Changed

- `schemas/entity.schema.json`:
  - `relationships` shape corrected to array-of-relationship-
    instances; each entry has `source_id`, `target_id`,
    `relationship_type`, plus optional `direction`, `status`,
    `effective_from`/`to`, `asserted_by`, `rationale`, `evidence`,
    and `provenance`.
  - `parent_process` and `child_processes` REMOVED.
  - `capabilities_delivered` retained but documented as
    soft-deprecated; the canonical form is
    `relationships[relationship_type=realizes]`.
- `schemas/contribution.schema.json` — `proposed_entry.relationships`
  shape updated to match the metamodel relationship-instance
  shape (array of instances).
- `contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml` —
  template updated with the relationship-instance shape.
- `docs/architecture.md` — "Structural composition" and
  "Capability realization" sections updated to reflect the
  metamodel-aligned shape; new "The `relationships` shape"
  and "Legacy field migration" sections added.
- `docs/relandscape.md` — "The `relationships` field" and
  "The legacy fields" subsections added.
- `.github/workflows/ci.yml` — adds the Legacy Migration gate
  step (after the Process Identity gate).
- `change-requests/README.md` — CR-BP-03A row added.

#### Architecture-only (no file changes)

- The catalog now aligns with the metamodel's relationship-
  instance shape. Each relationship carries full provenance,
  lifecycle, and temporal validity.
- The catalog's `entities/v1-alpha/` is empty by design
  (CR-BP-02 §22), so the migration validator is forward-looking
  on future entries.

### CR-BP-03: Business Process Architecture

Lands the **4-axis classification**, **process-identity contract**,
and **contribution-driven re-landscape** mechanism on top of
CR-MM-PROC-01 + CR-AR-FMWK-01 + CR-BP-SPEC-BP-01 + CR-BP-02.

**No breaking changes.** CR-BP-03 introduces new fields additively;
existing entries continue to validate. The L0/L1/L2 hierarchy is a
**conceptual model** (not separate top-level directories).

#### Added

- `change-requests/CR-BP-03-business-process-architecture.md`
  (md5 `85697440a09102165099e4f67650b635`; byte-identical to working
  folder `/home/hermes/dea-work/process/00_inbox/`).
- `classifications/process-types.yaml` — the 5-value Mintzberg
  vocabulary with primary organizational component + primary
  purpose for each.
- `classifications/process-specializations.yaml` — the
  catalog-level specialization pattern vocabulary
  (by-customer-segment / by-region / by-product-line / by-tier /
  by-compliance-regime) with worked examples.
- `schemas/identity.schema.json` — the process-identity sub-block
  schema (verb + object + scope + outcome_statement +
  evidence_links). Mirrored inline in
  `schemas/entity.schema.json` to avoid a remote `$ref`.
- `schemas/contribution.schema.json` — the process-contribution
  schema (the input shape for `contributions/processes/`).
- `contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml` —
  the template contributors copy + fill in.
- `contributions/processes/README.md` — the contribution flow
  documentation.
- `scripts/check_process_identity.py` — process-identity validator
  enforcing BP-ARC-ID-001..005 (with built-in `--self-test`).
- `docs/architecture.md` — the L0/L1/L2 structural architecture
  narrative.
- `docs/classification.md` — the 4-axis classification narrative.
- `docs/identity.md` — the process-identity contract narrative.
- `docs/relandscape.md` — the contribution-driven re-landscape
  mechanism.
- `docs/conformance.md` — the conformance gates summary.
- `validation/conformance/README.md` — forward-looking alias for
  the catalog's conformance validation.
- `.github/workflows/process-contribution-report.yml` — CI
  workflow for contribution-driven re-landscape (PRs to
  `contributions/processes/`).

#### Changed

- `schemas/entity.schema.json` — adds the new fields
  additively:
    - `process_type` (5-value enum; default `core`).
    - `process_specialization` (list of parent process ids).
    - `specialization_pattern` (free-text pattern label).
    - `relationships.{composes, realizes}` (canonical OpenDEA
      form).
    - `identity` (inline sub-schema mirroring
      `schemas/identity.schema.json`).
  - The id pattern is loosened to allow two-colon ids
    (`dea:bp:...`); the existing one-colon pattern still matches.
  - All existing fields are preserved; the legacy
    `parent_process` / `child_processes` / `capabilities_delivered`
    are documented as preserved migration aliases.
- `.github/workflows/ci.yml` — adds the Process Identity gate
  step (after the Process Context gate).

#### Architecture-only (no file changes)

- The 4-axis classification (intent / type / specialization /
  audience) is documented in `docs/classification.md` and
  `README.md`. Existing fields (`process_intent`,
  `process_audience`) are preserved; new fields (`process_type`,
  `process_specialization`) are added alongside.
- The L0/L1/L2 hierarchy is conceptual, documented in
  `docs/architecture.md` and `README.md`. There are no separate
  top-level directories for L0 / L1 / L2 entries.
- The re-landscape mechanism is contribution-driven, not
  in-tree. A re-landscape suggestion is generated by the
  contribution report workflow and reviewed by a catalog
  maintainer; the catalog does not auto-rewrite.

### CR-BP-02: Establish Process Context

Lands the **Process Context register + Cell Charter schema** on top of
the kernel + specialization discipline established by CR-MM-PROC-01 +
CR-AR-FMWK-01 + CR-BP-SPEC-BP-01.

**Authority chain (CR-BP-02 depends on the kernel + specialization
tranche):**

- `1665209` — CR-MM-PROC-01 merged on `dea-metamodel` (kernel + specialization).
- `76463b2` — CR-AR-FMWK-01 merged on `dea-architecture-framework` (root model v0.5.0 → v0.6.0).
- `1e4b916` — CR-BP-SPEC-BP-01 merged on `dea-catalog-processes` (Business Process specialization).
- `cb1a410` — CI hotfix (validate-allocation pin v0.2.1 → v0.6.0).
- `v0.6.0` — OpenDEAM root model tag published.

#### Added

- `change-requests/CR-BP-02.md` (md5 `9a56f5b0fc351c23416c51d216d805ef`; byte-identical to working folder `/home/hermes/dea-work/process/00_inbox/CR-BP-02.md`; refined to depend on the kernel + specialization tranche and to re-anchor PC-007/008/AC-07 to the corrected canonical ids).
- `schemas/entities/process-context.schema.json` — the canonical Process Context + Cell Charter schema. References the authoritative ECF vocabulary (CR-ECF-003/004/005) without redefining it.
- `scripts/check_process_context.py` — Process Context validator enforcing PC-001..PC-008 (with built-in `--self-test`).
- `contexts/v1-alpha/README.md` — placeholder documenting that the 49-cell matrix is **empty by design** per CR-BP-02 §22.

#### Changed

- `.github/workflows/ci.yml` — adds the Process Context gate step (after the Business Process specialization gate).
- `README.md` — "Canonical Process Context" section updated to reference the new Process Context Register at `contexts/v1-alpha/`, the schema, and the validator; adds an explicit "Process Context ≠ Business Process" callout.
- `change-requests/README.md` — CR-BP-02 row added.

**Out of scope (gated on its merge):** CR-BP-03 (L0/L1 decomposition
semantics); CR-BP-04 (Activity); CR-BP-05 (Workflow/Task); CR-BP-06
(Business Process criteria); CR-BP-07 (cross-context relationships);
CR-BP-08 (MECE within contexts); CR-BP-09 (Process Discovery
execution); CR-BP-10 (49-cell matrix population).

### CR-BP-SPEC-BP-01: Business Process Specialization Catalog

Re-anchors the catalog on the **kernel + specializations** discipline for
the OpenDEA Process concept. Refines + supersedes the prior CR-BP-01
(which landed as PR #10 on the wrong premise that `dea:BusinessProcess`
is the sole canonical Process identity).

**Authority chain established by this CR (end-to-end):**

```
WSF (org)                                     wsf:Process (Tier-3 derived)
 └─ dea-metamodel (Core authority)              CR-MM-PROC-01; PR #163
     ├─ dea:Process            (abstract Core kernel)
     └─ dea:BusinessProcess    (Core specialization)
        └─ dea-architecture-framework (root model)   CR-AR-FMWK-01; PR #10 + tag v0.6.0
             ├─ dea:entity-process               (abstract kernel; class_alias PRC;
             │                                       discriminator process-kernel)
             └─ dea:entity-business-process      (specialization; class_alias BP;
                                                    specializes PRC)
                └─ dea-catalog-processes (this catalog)   CR-BP-SPEC-BP-01; this PR
```

**Tranche history:**

- `1665209` — CR-MM-PROC-01 merged on `dea-metamodel` (kernel + specialization).
- `76463b2` — CR-AR-FMWK-01 merged on `dea-architecture-framework` (root model v0.5.0 → v0.6.0; consumer-validator abstract-kernel branch; ADR-0006).
- `417114f` — Revert of `a34c7ff` (CR-BP-01 implementation) merged on `dea-catalog-processes`.
- `v0.6.0` — OpenDEAM root model tag published.

**Changes:**

#### Added

- `change-requests/CR-BP-SPEC-BP-01.md` (md5 `5f5aa30e7ebfe2f1c187c300d5136406`; byte-identical to working folder `/home/hermes/dea-work/process/00_inbox/`).
- `docs/governance/process-specialization.md` — the governance narrative for the kernel + specialization contract.
- `scripts/check_process_specialization.py` — new validator enforcing `BP-SPEC-01-001..007` (with built-in `--self-test`).

#### Changed

- `metamodel-pointer.yaml` — pointer now declares the dual contract:
  - Primary `metamodel:` block: `dea:BusinessProcess` (specialization; class_alias BP; layer L3; building_block L3-value-delivery).
  - `metamodel.entities:` list: `dea:entity-process` (kernel; class_alias PRC; discriminator process-kernel; no layer, no dimension).
  - `metamodel.version: v0.6.0` (advances from v0.2.1; the root model carries both ids as of v0.6.0).
- `schemas/entity.schema.json` — `title: "Business Process"` (was `"Process Catalog Entry"`); description now references the WSF / Process-kernel lineage (CR-MM-PROC-01; CR-AR-FMWK-01; CR-BP-SPEC-BP-01).
- `.github/workflows/ci.yml` — adds the Business Process specialization gate step.
- `README.md` — "Purpose" reframed as Business Process **specialization** catalog; governing principle updated to "One kernel. Many valid specializations. One canonical home per specialization."

#### Removed (from the reverted `a34c7ff`; re-anchored here under the corrected premise)

- `change-requests/CR-BP-01.md` — superseded by this CR (the original text remains archived in `/home/hermes/dea-work/process/00_inbox/CR-BP-01.md`).
- `docs/governance/canonical-identity-business-process.md` — replaced by `docs/governance/process-specialization.md`.
- `scripts/check_bp01_canonical.py` — replaced by `scripts/check_process_specialization.py` (extended to `BP-SPEC-01-001..007`; original BP-01-001/002/003 rules folded into the new ruleset).

**Sub-classifications (operational / support / management)** remain
**catalog-internal** via the `process_intent` field. They do not promote
to root-model entities (`dea:entity-operational-process`, etc.). The
validator's `BP-SPEC-01-007` rule enforces this.

**Out of scope (gated on its merge):** CR-BP-02 (Process Context register
+ Cell Charter schema).

## Superseded (do not proceed with these)

- `a34c7ff` (CR-BP-01; PR #10): wrong premise — promoted
  `dea:BusinessProcess` as the sole canonical Process identity. Reverted
  by PR #11 (commit `417114f`). The artifacts (governance doc, validator,
  CI wire) are **preserved** and re-anchored by this CR under the
  corrected kernel + specialization discipline.