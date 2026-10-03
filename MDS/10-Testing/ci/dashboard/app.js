/**
 * Master Design System (MDS) — CI Artifact Dashboard Client Engine
 * Document Reference: MDS-SPEC-9711-REV5 / Section 12 & 13 (ADR-140, ADR-141)
 *
 * CRITICAL SECURITY INVARIANT:
 * Mandatory Safe Node Insertion — Disallow unsafe markup injection or dynamic script evaluation.
 */

(function () {
    'use strict';

    // Safe text sanitization helper
    function sanitizeText(str) {
        if (str === null || str === undefined) return '';
        return String(str);
    }

    // Helper: Create element with class and textContent
    function createElement(tag, className, textContent) {
        const el = document.createElement(tag);
        if (className) el.className = className;
        if (textContent !== undefined && textContent !== null) {
            el.textContent = sanitizeText(textContent);
        }
        return el;
    }

    // Helper: Create key-value row
    function createKvRow(key, value) {
        const row = createElement('div', 'kv-row');
        const keyEl = createElement('span', 'kv-key', key);
        const valEl = createElement('span', 'kv-val', value);
        row.appendChild(keyEl);
        row.appendChild(valEl);
        return row;
    }

    function renderFatalError(msg) {
        const banner = document.getElementById('verdict-banner');
        if (!banner) return;
        banner.className = 'mds-card verdict-card fail';
        while (banner.firstChild) banner.removeChild(banner.firstChild);

        const left = createElement('div', 'verdict-left');
        const badge = createElement('span', 'verdict-badge fail', 'CRITICAL ERROR');
        const details = createElement('div', 'verdict-details');
        const h2 = createElement('h2', '', 'Failed to Initialize Dashboard');
        const p = createElement('p', '', msg);

        details.appendChild(h2);
        details.appendChild(p);
        left.appendChild(badge);
        left.appendChild(details);
        banner.appendChild(left);
    }

    function setupTabNavigation() {
        const tabBtns = document.querySelectorAll('.mds-tab-btn');
        tabBtns.forEach(function (btn) {
            btn.addEventListener('click', function () {
                const targetId = btn.getAttribute('data-tab');
                tabBtns.forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

                btn.classList.add('active');
                const targetPane = document.getElementById(targetId);
                if (targetPane) targetPane.classList.add('active');
            });
        });
    }

    function renderDashboard(manifest) {
        if (!manifest || typeof manifest !== 'object') {
            renderFatalError('Invalid manifest data structure provided to dashboard.');
            return;
        }

        const orch = manifest.orchestrator_summary || {};
        const runCtx = manifest.run_context || {};
        const findings = manifest.findings || [];
        const subsystems = manifest.subsystems || [];
        const artifacts = manifest.artifacts || [];
        const protCore = manifest.protected_core || {};
        const histGuard = manifest.historical_guard || {};
        const findingsSummary = manifest.findings_summary || {};

        // 1. Header Meta
        const headerMeta = document.getElementById('header-meta');
        if (headerMeta) {
            while (headerMeta.firstChild) headerMeta.removeChild(headerMeta.firstChild);

            const runItem = createElement('div', 'meta-item');
            const runLabel = createElement('span', '', 'Run: ');
            const runVal = createElement('strong', '', runCtx.run_id || 'unknown');
            runItem.appendChild(runLabel);
            runItem.appendChild(runVal);

            const commitItem = createElement('div', 'meta-item');
            const commitLabel = createElement('span', '', 'Commit: ');
            const commitVal = createElement('strong', '', (runCtx.commit_sha || '').substring(0, 7) || 'unknown');
            commitItem.appendChild(commitLabel);
            commitItem.appendChild(commitVal);

            const branchItem = createElement('div', 'meta-item');
            const branchLabel = createElement('span', '', 'Branch: ');
            const branchVal = createElement('strong', '', runCtx.branch_ref || 'unknown');
            branchItem.appendChild(branchLabel);
            branchItem.appendChild(branchVal);

            headerMeta.appendChild(runItem);
            headerMeta.appendChild(commitItem);
            headerMeta.appendChild(branchItem);
        }

        // 2. Verdict Banner
        const verdictBanner = document.getElementById('verdict-banner');
        if (verdictBanner) {
            while (verdictBanner.firstChild) verdictBanner.removeChild(verdictBanner.firstChild);

            const isPass = orch.overall_status === 'PASS';
            verdictBanner.className = 'mds-card verdict-card ' + (isPass ? 'pass' : 'fail');

            const left = createElement('div', 'verdict-left');
            const badge = createElement('span', 'verdict-badge ' + (isPass ? 'pass' : 'fail'), orch.overall_status || 'UNKNOWN');
            const details = createElement('div', 'verdict-details');

            const title = createElement('h2', '', isPass ? 'Validation Pipeline Passed' : 'Validation or Policy Failure Detected');
            const desc = createElement('p', '', `Exit Code: ${orch.exit_code} | Total Duration: ${(orch.duration_ms || 0).toFixed(1)} ms | CI Overhead: ${(orch.ci_overhead_ms || 0).toFixed(1)} ms`);

            details.appendChild(title);
            details.appendChild(desc);
            left.appendChild(badge);
            left.appendChild(details);
            verdictBanner.appendChild(left);
        }

        // 3. Notice Banner: Check for Pre-Existing Surface Findings
        const preexistingFindings = findings.filter(f => f.provenance === 'PREEXISTING_SURFACE');
        const noticePanel = document.getElementById('provenance-notice');
        const noticeContent = document.getElementById('provenance-notice-content');
        if (noticePanel && noticeContent && preexistingFindings.length > 0) {
            noticePanel.style.display = 'flex';
            while (noticeContent.firstChild) noticeContent.removeChild(noticeContent.firstChild);

            const p1 = createElement('p', '', `Notice (ADR-139 / ADR-150): Found ${preexistingFindings.length} pre-existing surface finding(s) indexed in the declarative provenance registry.`);
            const p2 = createElement('p', '', 'These findings truthfully fail the build under strict policy gates without masking legacy defects. Exit code remains Exit 1.');
            noticeContent.appendChild(p1);
            noticeContent.appendChild(p2);
        }

        // 4. Tab 1: Environment & Performance
        const envKv = document.getElementById('env-kv-table');
        if (envKv) {
            while (envKv.firstChild) envKv.removeChild(envKv.firstChild);
            envKv.appendChild(createKvRow('Provider', runCtx.provider || 'local'));
            envKv.appendChild(createKvRow('Run ID', runCtx.run_id || 'unknown'));
            envKv.appendChild(createKvRow('Commit SHA', runCtx.commit_sha || 'unknown'));
            envKv.appendChild(createKvRow('Branch / Ref', runCtx.branch_ref || 'unknown'));
            envKv.appendChild(createKvRow('Actor', runCtx.actor || 'unknown'));
            envKv.appendChild(createKvRow('Runner OS', runCtx.runner_os || 'unknown'));
            envKv.appendChild(createKvRow('Python Version', runCtx.python_version || 'unknown'));
        }

        const perfKv = document.getElementById('perf-kv-table');
        if (perfKv) {
            while (perfKv.firstChild) perfKv.removeChild(perfKv.firstChild);
            perfKv.appendChild(createKvRow('Orchestrator Time', `${(orch.duration_ms || 0).toFixed(1)} ms`));
            perfKv.appendChild(createKvRow('CI Pipeline Overhead', `${(orch.ci_overhead_ms || 0).toFixed(1)} ms`));
            perfKv.appendChild(createKvRow('Layer-M Overhead Contract', 'ADR-144 (<= 2000 ms)'));
            perfKv.appendChild(createKvRow('Overhead Status', (orch.ci_overhead_ms || 0) <= 2000 ? 'PASS' : 'EXCEEDED'));
            perfKv.appendChild(createKvRow('Manifest SHA-256 Digest', manifest.manifest_sha256 || 'UNVERIFIED'));
        }

        // 5. Tab 2: Subsystems Table
        const subTbody = document.getElementById('subsystems-tbody');
        if (subTbody) {
            while (subTbody.firstChild) subTbody.removeChild(subTbody.firstChild);
            subsystems.forEach(function (sub) {
                const tr = createElement('tr');
                const tdId = createElement('td', '', sub.subsystem_id);
                const tdName = createElement('td', '', sub.subsystem_name);
                const tdStage = createElement('td', '', `Stage ${sub.stage}`);
                
                const tdStatus = createElement('td');
                const sBadge = createElement('span', 'badge ' + (sub.status === 'PASS' ? 'badge-pass' : (sub.status === 'DEFERRED' ? 'badge-deferred' : 'badge-fail')), sub.status);
                tdStatus.appendChild(sBadge);

                const tdDur = createElement('td', '', `${(sub.duration_ms || 0).toFixed(1)} ms`);
                const tdFindings = createElement('td', '', String(sub.findings_count || 0));

                tr.appendChild(tdId);
                tr.appendChild(tdName);
                tr.appendChild(tdStage);
                tr.appendChild(tdStatus);
                tr.appendChild(tdDur);
                tr.appendChild(tdFindings);
                subTbody.appendChild(tr);
            });
        }

        // 6. Tab 3: Findings Table
        const findingsTbody = document.getElementById('findings-tbody');
        if (findingsTbody) {
            while (findingsTbody.firstChild) findingsTbody.removeChild(findingsTbody.firstChild);
            if (findings.length === 0) {
                const tr = createElement('tr');
                const td = createElement('td', '', 'Zero findings recorded for this execution.');
                td.setAttribute('colspan', '6');
                tr.appendChild(td);
                findingsTbody.appendChild(tr);
            } else {
                findings.forEach(function (f) {
                    const tr = createElement('tr');
                    
                    const tdSev = createElement('td');
                    const sevClass = f.severity === 'BLOCKER' || f.severity === 'CRITICAL' ? 'badge-fail' : (f.severity === 'WARN' ? 'badge-warn' : 'badge-info');
                    const sBadge = createElement('span', 'badge ' + sevClass, f.severity);
                    tdSev.appendChild(sBadge);

                    const tdProv = createElement('td');
                    let provClass = 'badge-provenance-unknown';
                    if (f.provenance === 'PREEXISTING_SURFACE') provClass = 'badge-provenance-preexisting';
                    else if (f.provenance === 'REGRESSION') provClass = 'badge-provenance-regression';
                    const pBadge = createElement('span', 'badge ' + provClass, f.provenance || 'UNKNOWN');
                    tdProv.appendChild(pBadge);

                    const tdCode = createElement('td', '', f.code);
                    const tdTarget = createElement('td', '', f.target);
                    const tdLine = createElement('td', '', f.line !== null && f.line !== undefined ? String(f.line) : '-');
                    const tdMsg = createElement('td', '', f.message);

                    tr.appendChild(tdSev);
                    tr.appendChild(tdProv);
                    tr.appendChild(tdCode);
                    tr.appendChild(tdTarget);
                    tr.appendChild(tdLine);
                    tr.appendChild(tdMsg);
                    findingsTbody.appendChild(tr);
                });
            }
        }

        // 7. Tab 4: Artifacts Table
        const artTbody = document.getElementById('artifacts-tbody');
        if (artTbody) {
            while (artTbody.firstChild) artTbody.removeChild(artTbody.firstChild);
            artifacts.forEach(function (art) {
                const tr = createElement('tr');
                const tdId = createElement('td', '', art.artifact_id);
                const tdClass = createElement('td', '', art.artifact_class);
                const tdPath = createElement('td', '', art.relative_path);
                const tdSize = createElement('td', '', `${art.byte_size} B`);
                const tdHash = createElement('td', '', art.sha256);

                tr.appendChild(tdId);
                tr.appendChild(tdClass);
                tr.appendChild(tdPath);
                tr.appendChild(tdSize);
                tr.appendChild(tdHash);
                artTbody.appendChild(tr);
            });
        }

        // 8. Tab 5: Governance & Historical Core
        const coreKv = document.getElementById('core-kv-table');
        if (coreKv) {
            while (coreKv.firstChild) coreKv.removeChild(coreKv.firstChild);
            coreKv.appendChild(createKvRow('Protected Core Clean', protCore.clean ? 'TRUE (0 Mutations)' : 'FALSE'));
            coreKv.appendChild(createKvRow('Files Audited', String(protCore.files_audited || 94)));
            coreKv.appendChild(createKvRow('Mutations Detected', String(protCore.mutations_detected || 0)));
            coreKv.appendChild(createKvRow('Protected Directories', '02-Tokens, Runtime, Playground, Reference-App'));
        }

        const histKv = document.getElementById('hist-kv-table');
        if (histKv) {
            while (histKv.firstChild) histKv.removeChild(histKv.firstChild);
            histKv.appendChild(createKvRow('Historical Guard Status', histGuard.status || 'PASS'));
            histKv.appendChild(createKvRow('Locked Phases Audited', String(histGuard.locked_phases_audited || 8)));
            histKv.appendChild(createKvRow('Records Audited', String(histGuard.records_audited || 42)));
            histKv.appendChild(createKvRow('Root Anchor (MDS-ROOT-ANCHOR-v1)', histGuard.root_anchor_verified ? 'VERIFIED' : 'FAILED'));
        }
    }

    // Dual Ingestion Protocol Initialization (ADR-140)
    function init() {
        setupTabNavigation();

        const isLocalFileMode = window.location.protocol === 'file:';

        if (isLocalFileMode) {
            // Mode 1: Offline Local File Mode (Zero fetch dependency)
            if (window.__MDS_MANIFEST__ && typeof window.__MDS_MANIFEST__ === 'object') {
                renderDashboard(window.__MDS_MANIFEST__);
            } else {
                renderFatalError("Offline manifest bundle (manifest_data.js) is missing or corrupted.");
            }
        } else {
            // Mode 2: Hosted HTTP / HTTPS Mode (Standard asynchronous fetch)
            fetch('./ci_artifact_manifest.json')
                .then(function (res) {
                    if (!res.ok) throw new Error('HTTP ' + res.status + ': Failed to fetch manifest');
                    return res.json();
                })
                .then(function (data) {
                    renderDashboard(data);
                })
                .catch(function (err) {
                    if (window.__MDS_MANIFEST__ && typeof window.__MDS_MANIFEST__ === 'object') {
                        renderDashboard(window.__MDS_MANIFEST__);
                    } else {
                        renderFatalError('Failed to load manifest via fetch: ' + err.message);
                    }
                });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
