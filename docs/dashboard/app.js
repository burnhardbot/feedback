/* STREAMEN public dashboard. Read-only browser: no tokens, secrets or privileged API writes. */
(function (root) {
  'use strict';

  const REPO = 'burnhardbot/feedback';
  const API = 'https://api.github.com/repos/' + REPO;
  const ISSUE_URL = 'https://github.com/' + REPO + '/issues/16';
  const ISSUE_COMMENT_URL = ISSUE_URL + '#new_comment_field';
  const UPDATE_DIR = 'https://github.com/' + REPO + '/tree/main/docs/updates';
  const DEFAULT_TESTERS = ['laberfeuer'];
  const STATE_LABELS = { open: 'OFFEN', done: 'BESTANDEN', fail: 'FEHLER', blocked: 'BLOCKIERT' };

  function parseTests(markdown) {
    if (typeof markdown !== 'string') throw new TypeError('Testliste muss Text sein');
    const rows = [];
    const ids = new Set();
    let area = 'Weitere Prüfungen';
    for (const line of markdown.split(/\r?\n/)) {
      const heading = /^###\s+(.+)$/.exec(line);
      if (heading) area = heading[1].trim();
      const match = /^- \[([ xX])\] \*\*(T\d{2,4})\s*[–-]\s*([^*]+)\*\*:?\s*(.*)$/.exec(line);
      if (!match) continue;
      const id = match[2];
      if (ids.has(id)) throw new Error('Doppelte Test-ID: ' + id);
      ids.add(id);
      const title = match[3].trim().replace(/:\s*$/, '');
      const description = match[4].trim().replace(/\s*_\(hinzugefügt für [^)]+\)_\s*$/, '');
      const release = /_\(hinzugefügt für ([^)]+)\)_/.exec(match[4]);
      rows.push({ id, title, description, area, checked: match[1].toLowerCase() === 'x', release: release ? release[1] : 'v1.3 (Initialliste)' });
    }
    return rows;
  }

  function parseReport(comment) {
    if (!comment || typeof comment.body !== 'string') return null;
    const match = /(?:^|\n)\s*(?:\/test\s+)?(T\d{2,4})\s+(PASS|FAIL|BLOCKIERT)\b(?:\s+(v\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9.-]+)?))?/i.exec(comment.body);
    if (!match) return null;
    return {
      id: match[1].toUpperCase(), status: match[2].toUpperCase(), version: match[3] || null,
      date: comment.created_at || '', author: (comment.user && comment.user.login) || 'GitHub',
      excerpt: comment.body.replace(/\s+/g, ' ').slice(0, 230), url: comment.html_url || ISSUE_URL,
      commentId: Number(comment.id) || 0
    };
  }

  function latestReports(comments, allowedLogins = DEFAULT_TESTERS) {
    const latest = new Map();
    const allowed = new Set(allowedLogins.map(login => login.toLocaleLowerCase('en-US')));
    for (const comment of Array.isArray(comments) ? comments : []) {
      const report = parseReport(comment);
      if (!report || !allowed.has(report.author.toLocaleLowerCase('en-US'))) continue;
      const prev = latest.get(report.id);
      if (!prev || report.date > prev.date || (report.date === prev.date && report.commentId > prev.commentId)) latest.set(report.id, report);
    }
    return latest;
  }

  function withReports(tests, comments, allowedLogins = DEFAULT_TESTERS) {
    const statuses = latestReports(comments, allowedLogins);
    return tests.map(test => {
      const report = statuses.get(test.id) || null;
      let status = test.checked ? 'done' : 'open';
      if (report && report.status === 'FAIL') status = 'fail';
      if (report && report.status === 'BLOCKIERT') status = 'blocked';
      // PASS comments by themselves are not an actual checkmark or an approved deployment.
      return { ...test, status, report };
    });
  }

  function extractReleases(files) {
    return (Array.isArray(files) ? files : [])
      .filter(file => /^v\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9.-]+)?-changelog\.md$/.test(file.name || ''))
      .map(file => ({ version: file.name.slice(0, -'-changelog.md'.length), path: file.path, url: file.html_url || UPDATE_DIR }))
      .sort((a, b) => b.version.localeCompare(a.version, 'de', { numeric: true }));
  }

  function decodeGithubText(file) {
    if (!file || file.encoding !== 'base64' || typeof file.content !== 'string') throw new Error('Ungültige GitHub-Textdatei');
    const bytes = Uint8Array.from(atob(file.content.replace(/\s/g, '')), c => c.charCodeAt(0));
    return new TextDecoder('utf-8').decode(bytes);
  }

  function extractTesters(file) {
    if (!file) return DEFAULT_TESTERS;
    try {
      const parsed = JSON.parse(decodeGithubText(file));
      if (!Array.isArray(parsed.authorized_testers)) return DEFAULT_TESTERS;
      const candidates = parsed.authorized_testers.filter(login => typeof login === 'string' && /^[A-Za-z0-9-]{1,39}$/.test(login));
      return candidates.includes('laberfeuer') ? candidates : DEFAULT_TESTERS;
    } catch { return DEFAULT_TESTERS; }
  }

  async function githubJson(path) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 12000);
    try {
      const response = await fetch(API + path, {
        headers: { 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' },
        signal: controller.signal, cache: 'no-store'
      });
      if (!response.ok) throw new Error('GitHub API HTTP ' + response.status);
      return { data: await response.json(), next: /<([^>]+)>;\s*rel="next"/.exec(response.headers.get('Link') || '')?.[1] || null };
    } finally { clearTimeout(timer); }
  }

  async function fetchComments() {
    const all = [];
    let page = 1;
    // Avoid endless loops and unexpected API volume; clearly mark incomplete history below.
    while (page <= 6) {
      const response = await githubJson('/issues/16/comments?per_page=100&page=' + page);
      if (!Array.isArray(response.data)) throw new Error('Ungültige Kommentarantwort');
      all.push(...response.data);
      if (!response.next) return { comments: all, complete: true };
      page++;
    }
    return { comments: all, complete: false };
  }

  function el(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function addLink(parent, className, label, url) {
    const link = el('a', className, label);
    link.href = url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    parent.append(link);
    return link;
  }

  function safeUrl(url) {
    try { const parsed = new URL(url); return parsed.protocol === 'https:' && (parsed.hostname === 'github.com' || parsed.hostname === 'api.github.com') ? url : ISSUE_URL; }
    catch { return ISSUE_URL; }
  }

  function statusDisplay(test) { return STATE_LABELS[test.status] || STATE_LABELS.open; }

  function testCard(test) {
    const card = el('article', 'test-card');
    const main = el('div', 'test-main');
    const identity = el('div', 'test-identity');
    identity.append(el('span', 'test-id', test.id), el('h3', 'test-title', test.title));
    main.append(identity, el('span', 'status-pill status-' + test.status, statusDisplay(test)));
    card.append(main);
    if (test.description) card.append(el('p', 'test-description', test.description));
    const meta = el('div', 'test-meta');
    const area = el('span'); area.append(el('strong', '', 'Bereich: '), document.createTextNode(test.area));
    const origin = el('span'); origin.append(el('strong', '', 'Ursprung: '), document.createTextNode(test.release));
    meta.append(area, origin);
    if (test.report) {
      const author = el('span');
      author.append(el('strong', '', 'Letzter Kommentar: '), document.createTextNode(test.report.author));
      meta.append(author);
    }
    card.append(meta);
    if (test.report) {
      const evidence = el('div', 'test-evidence');
      evidence.append(el('strong', '', 'Befund: '), document.createTextNode(test.report.excerpt + ' '));
      addLink(evidence, '', 'Kommentar / Bilder ↗', safeUrl(test.report.url));
      card.append(evidence);
    }
    const bottom = el('div', 'test-card-bottom');
    const buttons = el('div', 'report-buttons');
    for (const [status, caption, className] of [['PASS', '✓ Funktioniert', 'good'], ['FAIL', '× Fehler', 'bad'], ['BLOCKIERT', '◷ Blockiert', '']]) {
      const button = el('button', 'mini-button ' + className, caption);
      button.type = 'button';
      button.addEventListener('click', () => showReportDialog(test, status));
      buttons.append(button);
    }
    bottom.append(buttons);
    addLink(bottom, 'test-evidence-link', 'Kommentieren / Screenshot ↗', ISSUE_COMMENT_URL);
    card.append(bottom);
    return card;
  }

  let state = { tests: [], releases: [], issues: [], version: 'v1.3', commentsComplete: true, loaded: false };

  function filteredTests() {
    const query = document.getElementById('searchInput').value.trim().toLocaleLowerCase('de');
    const status = document.getElementById('statusFilter').value;
    const area = document.getElementById('areaFilter').value;
    return state.tests.filter(test =>
      (status === 'all' || test.status === status) &&
      (area === 'all' || test.area === area) &&
      (!query || [test.id, test.title, test.description, test.area].join(' ').toLocaleLowerCase('de').includes(query))
    );
  }

  function renderTests() {
    const list = document.getElementById('testsList');
    list.replaceChildren();
    const filtered = filteredTests();
    for (const test of filtered) list.append(testCard(test));
    if (!filtered.length) list.append(el('div', 'empty-state', state.tests.length ? 'Keine Prüfpunkte passen zum Filter.' : 'Noch keine Tests vorhanden.'));
    document.getElementById('listResult').textContent = filtered.length + ' von ' + state.tests.length + ' Prüfungen angezeigt';
  }

  function renderStats() {
    const count = status => state.tests.filter(test => test.status === status).length;
    const open = count('open');
    document.getElementById('statOpen').textContent = String(open + count('fail') + count('blocked'));
    document.getElementById('statDone').textContent = String(count('done'));
    document.getElementById('statProblems').textContent = String(count('fail') + count('blocked'));
    document.getElementById('navOpen').textContent = String(open + count('fail') + count('blocked'));
    document.getElementById('allCount').textContent = String(state.tests.length);
    document.getElementById('statVersion').textContent = state.version;
    document.getElementById('statVersionDetail').textContent = 'Changelog – keine Installationsbestätigung';
  }

  function renderAreas() {
    const select = document.getElementById('areaFilter');
    const current = select.value;
    select.replaceChildren(new Option('Alle Bereiche', 'all'));
    for (const area of [...new Set(state.tests.map(test => test.area))]) select.add(new Option(area, area));
    select.value = [...select.options].some(o => o.value === current) ? current : 'all';
  }

  async function showReleaseDetail(release, container) {
    if (container.dataset.loaded === '1') {
      container.hidden = !container.hidden;
      return;
    }
    container.hidden = false;
    container.textContent = 'Changelog wird geladen …';
    try {
      const result = (await githubJson('/contents/' + release.path)).data;
      const markdown = decodeGithubText(result);
      container.replaceChildren();
      const rawLines = markdown.split(/\r?\n/);
      let list = null;
      for (const rawLine of rawLines.slice(0, 125)) {
        const line = rawLine.trim();
        if (!line) { list = null; continue; }
        if (/^#{1,3}\s+/.test(line)) { container.append(el('h4', '', line.replace(/^#+\s*/, ''))); list = null; }
        else if (/^[-*]\s+/.test(line)) {
          if (!list) { list = el('ul'); container.append(list); }
          list.append(el('li', '', line.slice(2)));
        } else { container.append(el('p', '', line.replace(/[>*`]/g, ''))); list = null; }
      }
      addLink(container, '', 'Vollständiges Changelog auf GitHub ↗', safeUrl(release.url));
      container.dataset.loaded = '1';
    } catch { container.textContent = 'Details konnten nicht geladen werden. Bitte den Changelog auf GitHub öffnen.'; }
  }

  function renderReleases() {
    const container = document.getElementById('releaseList');
    container.replaceChildren();
    if (!state.releases.length) { container.append(el('div', 'muted-line', 'Noch keine Changelogs geladen.')); return; }
    for (const release of state.releases.slice(0, 7)) {
      const wrapper = el('div');
      const row = el('button', 'release-item');
      row.type = 'button'; row.style.width = '100%'; row.style.textAlign = 'left';
      row.setAttribute('aria-expanded', 'false');
      const icon = el('span', 'release-icon', '▤');
      const body = el('span', 'release-body');
      body.append(el('strong', '', 'STREAMEN ' + release.version), el('small', '', 'Änderungen anzeigen · Status separat prüfen'));
      row.append(icon, body, el('span', 'release-arrow', '↗'));
      const details = el('div', 'release-details'); details.hidden = true;
      row.addEventListener('click', async () => { await showReleaseDetail(release, details); row.setAttribute('aria-expanded', String(!details.hidden)); });
      wrapper.append(row, details); container.append(wrapper);
    }
  }

  function renderBugs() {
    const container = document.getElementById('bugList'); container.replaceChildren();
    const issues = state.issues.filter(issue => issue.number !== 16 && !issue.pull_request);
    if (!issues.length) { container.append(el('div', 'muted-line', 'Keine weiteren offenen öffentlichen Issues gefunden.')); return; }
    for (const issue of issues.slice(0, 7)) {
      const row = el('a', 'bug-item');
      row.href = safeUrl(issue.html_url); row.target = '_blank'; row.rel = 'noopener noreferrer';
      const body = el('span', 'bug-body');
      body.append(el('strong', '', issue.title || 'Öffentliches Issue'), el('small', '', '#' + issue.number + ' · ' + (issue.state === 'open' ? 'Offen' : 'Geschlossen')));
      row.append(el('span', 'bug-icon', '!'), body, el('span', 'bug-arrow', '↗'));
      container.append(row);
    }
  }

  function toast(text) {
    const box = document.getElementById('toast');
    box.textContent = text; box.hidden = false;
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => { box.hidden = true; }, 3800);
  }

  function showReportDialog(test, status) {
    const dialog = document.getElementById('reportDialog');
    document.getElementById('dialogTitle').textContent = test.id + ' – ' + (status === 'PASS' ? 'Funktioniert' : status === 'FAIL' ? 'Fehler melden' : 'Blockiert');
    document.getElementById('dialogInfo').textContent = test.title + ' · Tatsächliche Version und Prüfbeleg ergänzen. GitHub übernimmt die Identitätsprüfung.';
    const suffix = status === 'PASS' ? ' – geprüft von [Name], [Datum], [Gerät/OBS]' : ' – [Beschreibung/Grund], [Datum], [Gerät/OBS]';
    document.getElementById('reportCommand').value = '/test ' + test.id + ' ' + status + ' ' + state.version + suffix;
    document.getElementById('openComment').href = ISSUE_COMMENT_URL;
    document.getElementById('dialogHint').textContent = 'Nur freigeschaltete GitHub-Tester können den Haken per Kommentarautomatik ändern. Vorher bleibt der Status offen. Screenshots direkt im GitHub-Kommentar anhängen.';
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else { document.getElementById('reportCommand').focus(); toast('Bitte den Befehl kopieren und auf GitHub kommentieren.'); }
  }

  async function copyReport() {
    const input = document.getElementById('reportCommand');
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(input.value);
      toast('Befehl kopiert. Auf GitHub als Kommentar einfügen und Belege ergänzen.');
    } catch {
      input.focus(); input.select();
      toast('Befehl ist markiert. Bitte manuell kopieren (Strg+C).');
    }
  }

  function setSourceState(healthy) {
    const source = document.querySelector('.source-indicator strong');
    if (source) source.textContent = healthy ? 'GitHub verbunden' : 'GitHub nicht erreichbar';
    const dot = document.querySelector('.source-dot');
    if (dot) dot.style.background = healthy ? '#7ddbb1' : '#ff8894';
  }

  async function loadData() {
    const refresh = document.getElementById('refreshButton'); refresh.disabled = true;
    const results = await Promise.allSettled([
      githubJson('/issues/16'),
      fetchComments(),
      githubJson('/contents/docs/updates'),
      githubJson('/issues?state=open&per_page=100'),
      githubJson('/contents/docs/updates/tester-roles.json')
    ]);
    refresh.disabled = false;
    const [issueResult, commentsResult, releasesResult, bugsResult, rolesResult] = results;
    if (issueResult.status === 'fulfilled') {
      try {
        const tests = parseTests(issueResult.value.data.body || '');
        const commentData = commentsResult.status === 'fulfilled' ? commentsResult.value : { comments: [], complete: false };
        const allowed = rolesResult.status === 'fulfilled' ? extractTesters(rolesResult.value.data) : DEFAULT_TESTERS;
        state.tests = withReports(tests, commentData.complete ? commentData.comments : [], allowed);
        state.commentsComplete = commentData.complete;
        state.loaded = true;
        renderAreas(); renderTests();
        document.getElementById('testsError').hidden = true;
        if (!state.commentsComplete) document.getElementById('listResult').textContent += ' · Kommentarhistorie nicht vollständig geladen';
        setSourceState(true);
      } catch {
        document.getElementById('testsList').replaceChildren();
        document.getElementById('testsError').hidden = false;
        document.getElementById('listResult').textContent = 'Testliste konnte nicht verarbeitet werden';
        setSourceState(false);
      }
    } else {
      if (!state.loaded) {
        document.getElementById('testsList').replaceChildren();
        document.getElementById('testsError').hidden = false;
      }
      document.getElementById('listResult').textContent = 'GitHub gerade nicht erreichbar · bestehende Anzeige nicht bestätigt';
      setSourceState(false);
    }
    if (releasesResult.status === 'fulfilled') state.releases = extractReleases(releasesResult.value.data);
    if (bugsResult.status === 'fulfilled') state.issues = bugsResult.value.data;
    state.version = state.releases[0]?.version || 'v1.3';
    renderStats(); renderReleases(); renderBugs();
    document.getElementById('lastLoaded').textContent = 'Abgerufen ' + new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
    if (issueResult.status !== 'fulfilled') toast('GitHub derzeit nicht erreichbar. Direktlink zur Testliste nutzen.');
  }

  function init() {
    document.getElementById('refreshButton').addEventListener('click', loadData);
    for (const id of ['searchInput', 'statusFilter', 'areaFilter']) document.getElementById(id).addEventListener(id === 'searchInput' ? 'input' : 'change', renderTests);
    document.getElementById('copyCommand').addEventListener('click', copyReport);
    for (const link of document.querySelectorAll('.nav-link')) {
      link.addEventListener('click', () => {
        for (const node of document.querySelectorAll('.nav-link')) node.classList.remove('active');
        link.classList.add('active');
      });
    }
    loadData();
    setInterval(() => { if (document.visibilityState === 'visible') loadData(); }, 300000);
  }

  const publicAPI = { parseTests, parseReport, latestReports, withReports, extractReleases, extractTesters };
  if (typeof module !== 'undefined' && module.exports) module.exports = publicAPI;
  if (typeof document !== 'undefined') {
    root.StreamenDashboard = publicAPI;
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
  }
})(typeof window !== 'undefined' ? window : globalThis);
