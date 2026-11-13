'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { parseTests, parseReport, latestReports, withReports, extractReleases, extractTesters } = require('./docs/dashboard/app.js');

const issue = `# Streamen – fortlaufend
### Server / Update-Rückkehr
- [ ] **T01 – Öffentliche Streamen-Seiten erreichbar:** Benutzerseiten öffnen und prüfen.
- [x] **T02 – OBS-Browserquellen:** Browserquellen kontrollieren.
### Fortlaufende Tests
<!-- STREAMEN_TEST_BACKLOG_BEGIN -->
- [ ] **T11 – Panorama-Einblendung**: Bild überprüfen. _(hinzugefügt für v1.3.1)_
<!-- STREAMEN_TEST_BACKLOG_END -->`;

test('parses original and appended checkboxes with areas and origin', () => {
  const tests = parseTests(issue);
  assert.equal(tests.length, 3);
  assert.deepEqual(tests.map(t => t.id), ['T01', 'T02', 'T11']);
  assert.equal(tests[0].title, 'Öffentliche Streamen-Seiten erreichbar');
  assert.equal(tests[0].checked, false);
  assert.equal(tests[1].checked, true);
  assert.equal(tests[2].release, 'v1.3.1');
  assert.equal(tests[2].description, 'Bild überprüfen.');
});

test('pending old test survives new releases unchanged', () => {
  const newer = issue.replace('<!-- STREAMEN_TEST_BACKLOG_END -->', '- [ ] **T12 – Zweite Kamera**: Testen. _(hinzugefügt für v1.3.2)_\n<!-- STREAMEN_TEST_BACKLOG_END -->');
  const tests = withReports(parseTests(newer), []);
  assert.equal(tests.length, 4);
  assert.equal(tests.find(t => t.id === 'T01').status, 'open');
  assert.equal(tests.find(t => t.id === 'T11').status, 'open');
  assert.equal(tests.find(t => t.id === 'T12').status, 'open');
  assert.equal(tests.find(t => t.id === 'T02').status, 'done');
});

test('FAIL and BLOCKIERT comments show problem status', () => {
  const reports = [
    { id: 1, body: '/test T01 FAIL v1.3 – Bild friert ein', user: { login: 'laberfeuer' }, created_at: '2026-11-13T10:00:00Z' },
    { id: 2, body: '/test T11 BLOCKIERT v1.3.1 – Gerät fehlt', user: { login: 'leoburnhard' }, created_at: '2026-11-13T12:00:00Z' }
  ];
  const states = withReports(parseTests(issue), reports, ['laberfeuer', 'leoburnhard']);
  assert.equal(states.find(t => t.id === 'T01').status, 'fail');
  assert.equal(states.find(t => t.id === 'T11').status, 'blocked');
});

test('PASS comment alone never falsely marks unchecked test as passed', () => {
  const states = withReports(parseTests(issue), [{ id: 1, body: '/test T01 PASS v1.3 – Test', user: { login: 'laberfeuer' }, created_at: '2026-11-13T10:00:00Z' }]);
  assert.equal(states.find(t => t.id === 'T01').status, 'open');
});

test('newer comment supersedes old one', () => {
  const a = { id: 1, body: 'T01 FAIL', user: { login: 'laberfeuer' }, created_at: '2026-11-13T10:00:00Z' };
  const b = { id: 2, body: 'T01 PASS', user: { login: 'laberfeuer' }, created_at: '2026-11-13T11:00:00Z' };
  const latest = latestReports([a, b]).get('T01');
  assert.equal(latest.status, 'PASS');
});

test('unauthorized public comments cannot manipulate dashboard status', () => {
  const fake = [{ id: 4, body: '/test T01 FAIL v1.3 – beliebiger Kommentar', user: { login: 'fremder-user' }, created_at: '2026-11-13T12:00:00Z' }];
  assert.equal(withReports(parseTests(issue), fake).find(t => t.id === 'T01').status, 'open');
  assert.equal(withReports(parseTests(issue), fake, ['laberfeuer', 'fremder-user']).find(t => t.id === 'T01').status, 'fail');
});

test('untrusted invalid allowlist falls back to Jan only', () => {
  assert.deepEqual(extractTesters(null), ['laberfeuer']);
});

test('duplicate test IDs fail closed', () => {
  assert.throws(() => parseTests(issue + '\n- [ ] **T01 – Noch einmal**: dup'), /Doppelte Test-ID/);
});

test('version list only uses actual changelog names', () => {
  const files = ['v1.3-changelog.md', 'v1.3.2-changelog.md', 'README.md'].map(name => ({ name, path: 'docs/updates/' + name }));
  const list = extractReleases(files);
  assert.deepEqual(list.map(r => r.version), ['v1.3.2', 'v1.3']);
});

test('plain comment report can still be read', () => {
  const parsed = parseReport({ id: 22, body: 'T01 BLOCKIERT – kein Livestream', user: { login: 'Jan' }, created_at: '2026-11-13T12:00:00Z' });
  assert.equal(parsed.status, 'BLOCKIERT');
});
