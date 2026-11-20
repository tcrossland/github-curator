// Tests for skills/repo-review/scorecard-template.html: fill it as Step 5 says,
// run its script against a minimal stand-in for the DOM, and check the markup
// for each mode (single review, overview, triage).
// Run: node --test tests/*.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const TEMPLATE = readFileSync(fileURLToPath(new URL('../skills/repo-review/scorecard-template.html', import.meta.url)), 'utf8');

// As Step 5: replace __TITLE__ and __DATA__, escaping every </ in the JSON.
const fill = (data) => TEMPLATE.replace('__TITLE__', data.title).replace('__DATA__', JSON.stringify(data).replace(/<\//g, '<\\/'));

// Run the page's script and return the HTML it writes into #app.
const render = (data) => {
  const page = fill(data);
  const json = page.match(/<script type="application\/json" id="data">([\s\S]*?)<\/script>/)[1];
  const script = page.match(/<script>\n([\s\S]*?)<\/script>/)[1];
  const els = {};
  const el = (id) => (els[id] ??= { innerHTML: '', textContent: '', value: '', parentNode: {}, addEventListener() {}, setAttribute() {}, select() {} });
  const document = { getElementById: (id) => (id === 'data' ? { textContent: json } : el(id)), querySelectorAll: () => [] };
  new Function('document', 'navigator', script)(document, {});
  return { html: els.app.innerHTML, els };
};

const question = (i, status) => ({ short: `Q${i}`, status, question: `Question ${i}?`, finding: 'Finding.', quotes: [{ text: 'A quoted line', source: 'README.md, line 1' }], fix: 'Fix.' });

const review = {
  title: 'Repo review: demo', subject: 'owner/demo at abc123', date: '2026-11-19',
  recommendation: {
    action: 'archive', why: 'Stopped, still worth showing.', signals: ['last commit 2017-05-04'], caveat: 'Archiving makes issues read-only.',
    before: { title: 'Before archiving', items: [{ text: 'Notice', status: 'todo', note: 'README.md line 1' }, { text: 'Picture', status: 'n/a' }] },
    feature: { recommended: true, why: 'Best evidence.', pinned: false, pins: ['owner/a', 'owner/b'], before: { title: 'Before featuring', items: [{ text: 'Pinned', status: 'todo' }] } },
  },
  similar: { asOf: '2026-11-19', items: [{ name: 'other/tool', link: 'https://github.com/other/tool', stars: 1, pushed: '2025-01-01', archived: false, description: 'Same job', relation: 'Maintained' }] },
  outcomes: { asOf: '2026-11-19', source: 'GitHub API', items: [{ label: 'Stars', value: '3' }], lists: [{ label: 'Stargazers', entries: [] }, { label: 'Top referrers', entries: [], empty: 'None in the last 14 days' }] },
  verdict: { question: '1', fix: 'Rewrite the opening.', why: 'It matters most.' },
  questions: [question(1, 'fail'), ...[2, 3, 4, 5, 6].map((i) => question(i, 'pass')), question(7, 'flagged')],
  fixPrompt: { header: 'HEADER', footer: 'FOOTER', items: [{ question: 'Hook', status: 'fail', text: 'FAIL' }, { question: 'Before archiving', status: 'before', text: 'BEFORE' }] },
  footer: 'Statuses.',
};

test('single review shows the recommendation, feature, similar repos and every question', () => {
  const { html, els } = render(review);
  assert.match(html, /<p class="act">Archive<\/p>/);
  assert.match(html, /class="st todo">To do</);
  assert.match(html, /class="st na">N\/A</);
  assert.match(html, /class="fv yes">Yes <span>· not pinned now/);
  assert.match(html, /Pinned now \(2 of 6\)/);
  assert.match(html, /1 star · pushed 2025-01-01/);
  assert.equal((html.match(/<article class="row /g) || []).length, 7);
  assert.match(html, /5 pass<\/span>.*1 fail<\/span>.*1 flagged<\/span>/);
  assert.match(html, /data-f="before"/);
  assert.equal(els['fp-text'].value, 'HEADER\n\nFAIL\n\nBEFORE\n\nFOOTER');
});

test('draft replies get their own filter, and only when there are any', () => {
  assert.doesNotMatch(render(review).html, /data-f="reply"/);
  const items = [...review.fixPrompt.items, { question: 'Waiting on you', status: 'reply', text: 'REPLY' }];
  const { html, els } = render({ ...review, fixPrompt: { ...review.fixPrompt, items } });
  assert.match(html, /data-f="before"[^>]*>Before<\/button><button type="button" data-f="reply" aria-pressed="false">Replies<\/button>/);
  assert.equal(els['fp-text'].value, 'HEADER\n\nFAIL\n\nBEFORE\n\nREPLY\n\nFOOTER');
});

test('empty outcome lists use their own message, or None', () => {
  const { html } = render(review);
  assert.match(html, /<h3>Stargazers<\/h3><ul><li class="none">None<\/li>/);
  assert.match(html, /<h3>Top referrers<\/h3><ul><li class="none">None in the last 14 days<\/li>/);
});

test('text from the run is escaped, and </script> in the data does not end the block', () => {
  const { html } = render({ ...review, subject: '<b>bold</b> </script><i>' });
  assert.match(html, /&lt;b&gt;bold&lt;\/b&gt; &lt;\/script&gt;&lt;i&gt;/);
});

test('timings show in a closed section at the foot, with totals', () => {
  const timings = [{ step: 'Get the draft', seconds: 42, calls: 12 }, { step: 'Similar repos', seconds: 125, calls: 3, searches: 4 }, { step: 'Build', seconds: 8, calls: 0 }];
  const { html } = render({ ...review, timings });
  assert.match(html, /<details class="timings"><summary>Timings · 2 min 55 s in all<\/summary>/);
  assert.match(html, /<tr><td>Similar repos<\/td><td class="num">2 min 05 s<\/td><td class="num">3<\/td><td class="num">4<\/td><\/tr>/);
  assert.match(html, /<tr><td>Get the draft<\/td><td class="num">42 s<\/td><td class="num">12<\/td><td class="num">0<\/td><\/tr>/);
  assert.match(html, /<tfoot><tr><td>Total<\/td><td class="num">2 min 55 s<\/td><td class="num">15<\/td><td class="num">4<\/td><\/tr><\/tfoot>/);
  assert.ok(html.indexOf('class="timings"') < html.indexOf('<footer>'));
});

test('timings without searches have no searches column, unknown calls show a dash, and the total is a lower bound', () => {
  const { html } = render({ ...review, timings: [{ step: 'Forks', seconds: 300, calls: null }, { step: 'Build', seconds: 5, calls: 1 }] });
  assert.doesNotMatch(html, /Searches/);
  assert.match(html, /<tr><td>Forks<\/td><td class="num">5 min 00 s<\/td><td class="num">–<\/td><\/tr>/);
  assert.match(html, /<td>Total<\/td><td class="num">5 min 05 s<\/td><td class="num">at least 1<\/td>/);
});

test('with no call counts at all, the total is a dash too', () => {
  const { html } = render({ ...review, timings: [{ step: 'Forks', seconds: 30, calls: null }] });
  assert.match(html, /<td>Total<\/td><td class="num">30 s<\/td><td class="num">–<\/td>/);
});

test('no timings, no section', () => {
  assert.doesNotMatch(render(review).html, /timings/);
});

test('overview shows pins and the recommendation column', () => {
  const { html } = render({
    overview: true, title: 'Portfolio overview', subject: '1 repo', date: '2026-11-19', verdict: { fix: 'x', why: 'y' },
    pins: { current: ['owner/a'], recommended: ['owner/a', 'owner/b'], source: 'GraphQL', why: 'Add b.' },
    repos: [{ name: 'owner/b', link: '#', action: 'keep', feature: true, todo: 2, statuses: Array(7).fill('pass'), fix: 'f', stars: 1, views: 0, scorecard: '#' }],
    timings: [{ step: 'owner/b', seconds: 600, calls: 80 }, { step: 'Build', seconds: 20, calls: 0 }],
  });
  assert.match(html, /Timings · 10 min 20 s in all/);
  assert.match(html, /<h3>Recommended<\/h3><ol><li>owner\/a<\/li><li>owner\/b<\/li><\/ol>/);
  assert.match(html, /<td class="act">Keep · featured · 2 to do<\/td>/);
});

test('triage splits clear deletes from repos to review and lists the commands', () => {
  const repo = (name, sure, action) => ({ name, link: '#', visibility: 'public', kind: 'fork', pinned: false, pushed: '2015-01-01', stars: 0, signals: ['0 commits ahead'], action, sure, reason: 'r', question: sure === 'review' ? 'q?' : undefined });
  const { html } = render({
    triage: true, title: 'Repo triage', subject: '3 repos', date: '2026-11-19',
    repos: [repo('t/a', 'review', 'archive'), repo('t/b', 'clear', 'delete'), repo('t/c', 'clear', 'delete')],
    commands: ['gh repo delete t/b', 'gh repo delete t/c'], commandsNote: 'Needs delete_repo.',
    next: '/github-curator:repo-review overview #', nextNote: 'None left.', footer: 'API only.',
    timings: [{ step: 'List repos', seconds: 3, calls: 1 }, { step: 'Forks', seconds: 61, calls: 120, searches: 17 }],
  });
  assert.match(html, /Timings · 1 min 04 s in all/);
  assert.match(html, /<td>Total<\/td><td class="num">1 min 04 s<\/td><td class="num">121<\/td><td class="num">17<\/td>/);
  assert.match(html, /2 clear deletes · 1 to review/);
  assert.match(html, /1 likely archive/);
  assert.match(html, /To review, most at stake first <span>\(1\)<\/span>/);
  assert.match(html, /Clear deletes <span>\(2\)<\/span>/);
  assert.match(html, /gh repo delete t\/b\ngh repo delete t\/c<\/textarea>/);
  assert.match(html, /None left\./);
});
