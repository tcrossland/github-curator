// Tests for skills/repo-review/scorecard-template.html: fill it as Step 5 says,
// run its script against a minimal stand-in for the DOM, and check the markup
// for each mode (single review, overview, triage, quick, profile).
// Run: node --test tests/*.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const TEMPLATE = readFileSync(fileURLToPath(new URL('../skills/repo-review/scorecard-template.html', import.meta.url)), 'utf8');

// As Step 5: replace __TITLE__ and __DATA__, escaping every </ in the JSON.
const fill = (data) => TEMPLATE.replace('__TITLE__', data.title).replace('__DATA__', JSON.stringify(data).replace(/<\//g, '<\\/'));

// Run the page's script and return the HTML it writes into #app. Each element
// keeps its listeners as on<type>, so a test can click it.
const render = (data, navigator = {}) => {
  const page = fill(data);
  const json = page.match(/<script type="application\/json" id="data">([\s\S]*?)<\/script>/)[1];
  const script = page.match(/<script>\n([\s\S]*?)<\/script>/)[1];
  const els = {};
  const el = (id) => (els[id] ??= { innerHTML: '', textContent: '', value: '', parentNode: {}, addEventListener(type, f) { this['on' + type] = f; }, setAttribute() {}, select() {} });
  const document = { getElementById: (id) => (id === 'data' ? { textContent: json } : el(id)), querySelectorAll: () => [] };
  new Function('document', 'navigator', 'setTimeout', script)(document, navigator, () => {});
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

test('a review shows the audience it used, and none when the run gives none', () => {
  assert.match(render({ ...review, audience: 'researchers' }).html, /<span>owner\/demo at abc123<\/span><span>For researchers<\/span>/);
  assert.doesNotMatch(render(review).html, /<span>For /);
});

test('the verdict names its question, and none when the fix comes from no question', () => {
  assert.match(render(review).html, /Most important fix · question 1</);
  const leave = { ...review, recommendation: { ...review.recommendation, action: 'make-private', before: undefined }, verdict: { question: '', fix: 'Leave it private.', why: 'Not worth showing.' } };
  const { html } = render(leave);
  assert.match(html, /<span class="label">Most important fix<\/span>/);
  assert.doesNotMatch(html, /· question/);
});

test('a similar repo shows how it relates to the repo under review, with no statuses', () => {
  const item = { ...review.similar.items[0], overlap: 'same', alive: 'maintained', mention: 'alternative', difference: 'Matches on a key column', foundBy: ['`csv-diff`', 'data validation'], borrow: 'A one-line result at the top' };
  const elsewhere = { name: 'Elsewhere', link: 'https://example.org', overlap: 'partial', difference: 'Runs offline', mention: 'named' };
  const { html } = render({ ...review, similar: { ...review.similar, items: [item, elsewhere] } });
  assert.match(html, /<span class="tags"><span class="tag">Same job<\/span><span class="tag">Maintained<\/span><span class="tag">Name as an alternative<\/span><\/span>/);
  assert.match(html, /<span class="rel"><b>This repo adds<\/b> Matches on a key column<\/span>/);
  assert.match(html, /<span class="rel"><b>Found by<\/b> <code>csv-diff<\/code>, data validation<\/span>/);
  assert.match(html, /<span class="rel"><b>Worth borrowing<\/b> A one-line result at the top<\/span>/);
  assert.match(html, /<span class="tag">Overlaps<\/span><span class="tag">Named in the README<\/span><\/span><span class="rel"><b>This repo adds<\/b> Runs offline/);
  assert.doesNotMatch(html, /class="q (pass|fail|flagged)"/);
});

test('an archived similar repo gets no Maintained or Quiet tag, since its meta says archived', () => {
  const item = { ...review.similar.items[0], archived: true, alive: 'archived', overlap: 'adjacent', mention: 'no' };
  const { html } = render({ ...review, similar: { ...review.similar, items: [item] } });
  assert.match(html, /pushed 2025-01-01 · archived/);
  assert.match(html, /<span class="tags"><span class="tag">Neighbouring job<\/span><span class="tag">No need to name<\/span><\/span>/);
});

test('the fix prompt comes straight after the questions\' strip, before the sections that start closed', () => {
  const changes = { since: '2026-11-19', items: ['Q1 now fails', 'New `topic`'] };
  const { html } = render({ ...review, changes });
  assert.match(html, /<details class="fold changes"><summary><span class="label">Since last check · 2026-11-19<\/span> <span class="cnt">2 changes<\/span><\/summary><div class="fbody"><ul><li>Q1 now fails<\/li><li>New <code>topic<\/code><\/li><\/ul><\/div><\/details>/);
  assert.match(html, /<details class="fold sig"><summary><span class="ct">Signals<\/span> <span class="cnt">1<\/span><\/summary><div class="fbody"><ul class="signals"><li>last commit 2017-05-04<\/li><\/ul>/);
  assert.match(html, /<details class="fold chk"><summary><span class="ct">Before archiving<\/span> <span class="cnt">1 to do · 1 n\/a<\/span><\/summary>/);
  assert.match(html, /<details class="fold chk"><summary><span class="ct">Before featuring<\/span> <span class="cnt">1 to do<\/span><\/summary>/);
  assert.match(html, /<details class="fold outcomes"><summary><span class="label">Outcomes · context, not scored<\/span><\/summary>/);
  assert.match(html, /<details class="fold outcomes sim"><summary><span class="label">Similar repos · context, not scored<\/span> <span class="cnt">1 repo<\/span><\/summary>/);
  assert.doesNotMatch(html, /<details[^>]* open/);
  const at = (s) => html.indexOf(s);
  assert.ok(at('class="strip"') < at('class="fixp"'));
  assert.ok(at('class="fixp"') < at('class="fold outcomes"'));
  assert.ok(at('class="fold outcomes"') < at('class="fold outcomes sim"'));
  assert.ok(at('class="fold outcomes sim"') < at('class="rows"'));
});

test('draft replies get their own filter, and only when there are any', () => {
  assert.doesNotMatch(render(review).html, /data-f="reply"/);
  const items = [...review.fixPrompt.items, { question: 'Waiting on you', status: 'reply', text: 'REPLY' }];
  const { html, els } = render({ ...review, fixPrompt: { ...review.fixPrompt, items } });
  assert.match(html, /data-f="before"[^>]*>Before<\/button><button type="button" data-f="reply" aria-pressed="false">Replies<\/button>/);
  assert.equal(els['fp-text'].value, 'HEADER\n\nFAIL\n\nBEFORE\n\nREPLY\n\nFOOTER');
});

test('outcomes link to the traffic history page, and only to a claude.ai artifact', () => {
  assert.doesNotMatch(render(review).html, /Traffic history/);
  const url = 'https://claude.ai/artifact/YS5xnw166Fi27myFgNDjrv';
  const { html } = render({ ...review, outcomes: { ...review.outcomes, history: url } });
  assert.match(html, /<span class="asof">GitHub API · read 2026-11-19 · <a href="https:\/\/claude\.ai\/artifact\/YS5xnw166Fi27myFgNDjrv" target="_blank" rel="noopener">Traffic history<\/a><\/span>/);
  const code = render({ ...review, outcomes: { ...review.outcomes, history: 'https://claude.ai/code/artifact/0b6f2c1e-5a1d-4c55-9a2e-7f0d3c9b8e11' } }).html;
  assert.match(code, /href="https:\/\/claude\.ai\/code\/artifact\/0b6f2c1e-5a1d-4c55-9a2e-7f0d3c9b8e11"/);
  for (const bad of ['javascript:alert(1)', 'https://example.com/artifact/x', 'https://claude.ai/artifact/x" onmouseover="y']) {
    assert.doesNotMatch(render({ ...review, outcomes: { ...review.outcomes, history: bad } }).html, /Traffic history/);
  }
});

test('empty outcome lists use their own message, or None', () => {
  const { html } = render(review);
  assert.match(html, /<h3>Stargazers<\/h3><ul><li class="none">None<\/li>/);
  assert.match(html, /<h3>Top referrers<\/h3><ul><li class="none">None in the last 14 days<\/li>/);
});

test('stargazers whose profiles could not be read show Not available, as SKILL.md words it, not None in the same field', () => {
  // The wording the skill gives for the list when no profile could be read.
  const skill = readFileSync(fileURLToPath(new URL('../skills/repo-review/SKILL.md', import.meta.url)), 'utf8');
  const example = skill.match(/"Stargazers worth a look" when profiles were read[^(]*\(when no profile could be read, "Not available: " and the reason, such as "(Not available: [^"]+)"\)/);
  assert.ok(example, 'SKILL.md gives the Not available wording for Stargazers worth a look');
  const lists = [{ label: 'Stargazers worth a look', entries: [], empty: example[1] }, { label: 'Stargazers', entries: ['2026-11-01 · `someone` · 3 followers · activity not available · profile page summary'] }];
  const { html } = render({ ...review, outcomes: { ...review.outcomes, lists } });
  assert.match(html, /<h3>Stargazers worth a look<\/h3><ul><li class="none">Not available: GitHub refused the profile pages<\/li>/);
  assert.doesNotMatch(html, /None in the same field/);
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

test('each overview row with findings copies the same fix prompt as its scorecard\'s "All"', async () => {
  const scorecard = render(review).els['fp-text'].value;
  const repo = (name, extra) => ({ name, link: '#', action: 'keep', feature: false, todo: 0, statuses: Array(7).fill('pass'), fix: 'f', stars: 0, views: 0, scorecard: '#', ...extra });
  const copied = [];
  const { html, els } = render({
    overview: true, title: 'Portfolio overview', subject: '2 repos', date: '2026-11-19', verdict: { fix: 'x', why: 'y' },
    repos: [repo('owner/clean'), repo('owner/demo', { statuses: review.questions.map((q) => q.status), fixPrompt: review.fixPrompt })],
  }, { clipboard: { writeText: (t) => { copied.push(t); return Promise.resolve(); } } });
  assert.doesNotMatch(html, /id="ovfp-0"/);
  assert.match(html, /<button type="button" class="fpcopy" id="ovfp-1" aria-label="Copy the fix prompt for owner\/demo">Copy<\/button>/);
  assert.match(html, /Paste it into a Claude Code session in that repo/);
  els['ovfp-1'].onclick();
  assert.deepEqual(copied, [scorecard]);
  await Promise.resolve();
  assert.equal(els['ovfp-1'].textContent, 'Copied');
});

test('when the overview\'s copy is blocked, the row shows the prompt to copy by hand', () => {
  const { els } = render({
    overview: true, title: 'Portfolio overview', subject: '1 repo', date: '2026-11-19', verdict: { fix: 'x', why: 'y' },
    repos: [{ name: 'owner/demo', link: '#', statuses: Array(7).fill('fail'), fix: 'f', stars: 0, views: 0, scorecard: '#', fixPrompt: review.fixPrompt }],
  });
  els['ovfp-0'].onclick();
  assert.equal(els['ovfpr-0'].hidden, false);
  assert.equal(els['ovfpt-0'].value, render(review).els['fp-text'].value);
});

test('overview without fix prompts has no note', () => {
  const { html } = render({ overview: true, title: 'Portfolio overview', subject: '0 repos', date: '2026-11-19', verdict: { fix: 'x', why: 'y' }, repos: [] });
  assert.doesNotMatch(html, /ovnote|fpcopy/);
});

test('triage splits clear deletes from repos to review and lists the commands', () => {
  const repo = (name, sure, action) => ({ name, link: '#', visibility: 'public', kind: 'fork', pinned: false, pushed: '2015-01-01', stars: 0, signals: ['0 commits ahead'], action, sure, reason: 'r', question: sure === 'review' ? 'q?' : undefined });
  const { html } = render({
    triage: true, title: 'Repo triage', subject: '3 repos', date: '2026-11-19',
    repos: [repo('t/a', 'review', 'archive'), repo('t/b', 'clear', 'delete'), repo('t/c', 'clear', 'delete')],
    commands: ['gh repo delete t/b', 'gh repo delete t/c'], commandsNote: 'Needs delete_repo.',
    next: '/github-curator:repo-review portfolio #', nextNote: 'None left.', footer: 'API only.',
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
  assert.doesNotMatch(html, /Since last triage/);
});

test('each triage row to review copies its own review command, and clear deletes have none', () => {
  const repo = (name, sure, link) => ({ name, link, visibility: 'public', kind: 'fork', stars: 0, signals: [], action: sure === 'clear' ? 'delete' : 'archive', sure, reason: 'r' });
  const { html } = render({ triage: true, title: 'Repo triage', subject: '3 repos', date: '2026-11-22',
    repos: [repo('t/a', 'review', 'https://github.com/t/a'), repo('t/b', 'clear', 'https://github.com/t/b'), repo('t/c', 'review', '#')] });
  assert.match(html, /<div class="rcmd"><code id="rc-t-0">\/github-curator:repo-review https:\/\/github.com\/t\/a<\/code><button type="button" class="copy" data-copy="rc-t-0" aria-label="Copy the review command for t\/a">Copy<\/button><\/div>/);
  assert.match(html, /<code id="rc-t-2">\/github-curator:repo-review t\/c<\/code>/);
  assert.doesNotMatch(html, /repo-review https:\/\/github.com\/t\/b/);
  assert.equal((html.match(/class="rcmd"/g) || []).length, 2);
});

test('triage\'s changes since the last triage start closed, with their count', () => {
  const { html } = render({ triage: true, title: 'Repo triage', subject: '0 repos', date: '2026-11-21', repos: [], changes: { since: '2026-11-19', items: ['t/a archived'] } });
  assert.match(html, /<details class="fold changes"><summary><span class="label">Since last triage · 2026-11-19<\/span> <span class="cnt">1 change<\/span><\/summary>/);
});

const quickRepo = (name, statuses, extra = {}) => ({
  name, link: `https://github.com/${name}`, visibility: 'public', pinned: false, pushed: '2026-11-01', stars: 2, action: 'keep', fix: 'Add topics.', question: 'Worth featuring?',
  questions: ['Hook', 'Findable', 'Getting started'].map((short, i) => ({ short, status: statuses[i], note: `${short} note`, quotes: [{ text: `${short} line`, source: 'README.md, line 1' }] })),
  ...extra,
});

test('quick review lists each repo with its three statuses, provisional action and fix', () => {
  const { html } = render({
    quick: true, title: 'Quick review', subject: '2 repos', date: '2026-11-22',
    repos: [quickRepo('me/a', ['fail', 'flagged', 'pass'], { pinned: true }), quickRepo('me/b', ['pass', 'pass', 'fail'], { visibility: 'private', stars: 1, action: 'publish' })],
    next: '/github-curator:repo-review portfolio https://github.com/me/a', nextNote: 'None left.',
    timings: [{ step: 'List repos', seconds: 5, calls: 1, searches: 1 }, { step: 'Build', seconds: 3, calls: 0 }],
    footer: 'Provisional.',
  });
  assert.match(html, /<span class="label">Quick review · provisional<\/span><p class="fix">2 repos · 2 with a fail<\/p><p class="why">Hook: 1 pass, 1 fail, 0 flagged · Findable: 1 pass, 0 fail, 1 flagged · Getting started: 1 pass, 1 fail, 0 flagged<\/p>/);
  assert.match(html, /<a href="https:\/\/github.com\/me\/a">me\/a<\/a><div class="tsub">public · pinned · 2 stars · pushed 2026-11-01<\/div>/);
  assert.match(html, /<div class="tsub">private · 1 star · pushed 2026-11-01<\/div>/);
  assert.match(html, /<div class="qi"><span class="q fail">Hook · Fail<\/span> <span class="qn">Hook note<\/span><\/div><div class="qi"><span class="q flagged">Findable · Flagged<\/span>/);
  assert.match(html, /<td class="act">Keep<\/td><td>Add topics\.<div class="tq">Worth featuring\?<\/div><details class="ev"><summary>Evidence<\/summary><blockquote class="fail">Hook line<cite>Hook · README.md, line 1<\/cite><\/blockquote>/);
  assert.match(html, /<td class="act">Publish<\/td>/);
  assert.equal((html.match(/<tr><td class="num">/g) || []).length, 2);
  assert.match(html, /<span class="label">Review them in full<\/span>/);
  assert.match(html, /<code id="next-cmd">\/github-curator:repo-review portfolio https:\/\/github.com\/me\/a<\/code>/);
  assert.match(html, /Timings · 8 s in all/);
  assert.match(html, /<footer>Provisional\.<\/footer>/);
  assert.doesNotMatch(html, /Since last quick review|class="strip"|class="fixp" aria-label="Fix prompt"/);
});

test('each quick row with a fail or flag copies its own review command, and a row that passes has none', () => {
  const { html } = render({ quick: true, title: 'Quick review', subject: '3 repos', date: '2026-11-22',
    repos: [quickRepo('me/a', ['pass', 'flagged', 'pass']), quickRepo('me/b', ['pass', 'pass', 'pass']), quickRepo('me/c', ['fail', 'pass', 'pass'])] });
  assert.match(html, /<\/details><div class="rcmd"><code id="rc-q-0">\/github-curator:repo-review https:\/\/github.com\/me\/a<\/code><button type="button" class="copy" data-copy="rc-q-0" aria-label="Copy the review command for me\/a">Copy<\/button><\/div><\/td><\/tr>/);
  assert.match(html, /<code id="rc-q-2">\/github-curator:repo-review https:\/\/github.com\/me\/c<\/code>/);
  assert.doesNotMatch(html, /rc-q-1|repo-review https:\/\/github.com\/me\/b/);
});

test('quick review shows changes since the last one, closed, and no next command when all pass', () => {
  const { html } = render({
    quick: true, title: 'Quick review', subject: '1 repo', date: '2026-11-22',
    changes: { since: '2026-11-15', items: ['me/a: Findable flagged → pass'] },
    repos: [quickRepo('me/a', ['pass', 'pass', 'pass'], { fix: 'No change', question: null })],
  });
  assert.match(html, /<details class="fold changes"><summary><span class="label">Since last quick review · 2026-11-15<\/span> <span class="cnt">1 change<\/span>/);
  assert.match(html, /1 repo · 0 with a fail/);
  assert.doesNotMatch(html, /next-cmd/);
});

test('a pin the profile page summary may have left out shows as unknown, in the feature call and in rows', () => {
  const feature = { recommended: true, why: 'Best evidence.', pinned: 'unknown', pins: ['owner/a', 'owner/b', 'owner/c', 'owner/d'], pinsSource: 'profile page summary, may not be complete' };
  const { html } = render({ ...review, recommendation: { ...review.recommendation, feature } });
  assert.match(html, /class="fv yes">Yes <span>· pin unknown<\/span>/);
  assert.match(html, /<b>Pins read \(4, may be incomplete\):<\/b> owner\/a/);
  assert.doesNotMatch(html, /not pinned now|Pinned now \(/);
  const quick = render({ quick: true, title: 'Quick review', subject: '1 repo', date: '2026-11-23', repos: [quickRepo('me/a', ['pass', 'pass', 'pass'], { pinned: 'unknown' })] });
  assert.match(quick.html, /<div class="tsub">public · pin unknown · 2 stars/);
  const triage = render({ triage: true, title: 'Repo triage', subject: '1 repo', date: '2026-11-23',
    repos: [{ name: 't/a', link: '#', visibility: 'public', kind: 'fork', pinned: 'unknown', stars: 0, signals: [], action: 'archive', sure: 'review', reason: 'r' }] });
  assert.match(triage.html, /public · fork · pin unknown/);
});

test('fewer than six pins from the profile page summary are never shown as the whole list', () => {
  const source = 'profile page summary, may not be complete';
  const feature = { recommended: false, why: 'Thin.', pinned: true, pins: ['owner/a', 'owner/b', 'owner/c', 'owner/d'], pinsSource: source };
  const { html } = render({ ...review, recommendation: { ...review.recommendation, feature } });
  assert.match(html, /<b>Pins read \(4, may be incomplete\):<\/b> owner\/a/);
  assert.doesNotMatch(html, /Pinned now \(/);
  const overview = render({ overview: true, title: 'Portfolio overview', subject: '1 repo', date: '2026-11-23', verdict: { fix: 'x', why: 'y' },
    pins: { current: ['owner/a', 'owner/b'], recommended: ['owner/a'], source, why: 'Keep a.' }, repos: [] });
  assert.match(overview.html, /<h3>Pins read, may be incomplete<\/h3>/);
  assert.doesNotMatch(overview.html, /<h3>Pinned now<\/h3>/);
});

test('a Pinned item the review couldn\'t settle shows as Check and is counted apart from To do', () => {
  const feature = { recommended: true, why: 'Best evidence.', pinned: null, before: { title: 'Before featuring', items: [{ text: 'Pinned', status: 'check', note: 'The pins couldn\'t be read' }, { text: 'Licence', status: 'done' }] } };
  const { html } = render({ ...review, recommendation: { ...review.recommendation, feature } });
  assert.match(html, /class="fv yes">Yes <span>· pins not read<\/span>/);
  assert.match(html, /<span class="st check">Check<\/span><span class="it">Pinned<span>The pins couldn't be read<\/span>/);
  assert.match(html, /1 check · 1 done/);
});

const profile = {
  profile: true, title: 'Profile review: owner', subject: 'bio, 4 pins, profile README at abc123', link: 'https://github.com/owner', linkText: 'owner',
  date: '2026-11-24', rerun: '/github-curator:repo-review profile',
  verdict: { question: '2', fix: 'Pin owner/a.', why: 'It is the strongest work.' },
  questions: [{ short: 'Introduction', status: 'pass', question: 'Who?', finding: 'F.', quotes: [{ text: 'I build tools.', source: 'GitHub profile bio, read via the API' }], fix: 'No change' },
              { short: 'Pins', status: 'fail', question: 'Pins?', finding: 'F.', quotes: [], fix: 'Pin owner/a.' },
              { short: 'Facts', status: 'flagged', question: 'Facts?', finding: 'F.', quotes: [], fix: 'Fix a link.' }],
  pins: { current: ['owner/b', 'owner/c'], source: 'pinned items, read via GraphQL', recommended: ['owner/a', 'owner/b'], why: 'Swap c for a.',
          basis: 'Portfolio overview of 2026-11-21', changes: [{ name: 'owner/a', change: 'pin', why: 'Featured on its scorecard.' }, { name: 'owner/c', change: 'drop', why: 'Its scorecard says not to feature it.' }] },
  draft: { readme: 'I build <tools>.\n\n- [a](https://github.com/owner/a)', readmeNote: 'Drops the stats card.', bio: 'I build data tools.', bioNote: '19 characters.', where: '`README.md` in `owner/owner`' },
  contributions: { line: '3 merged pull requests', named: ['`other/lib` · fixed a parser'], note: 'Employers left out.' },
  next: '/github-curator:repo-review portfolio https://github.com/owner/d', nextNote: '1 more',
};

test('profile review shows its three questions, the pins with a reason per change, and the drafts to copy', () => {
  const { html } = render(profile);
  assert.equal((html.match(/<article class="row /g) || []).length, 3);
  assert.match(html, /1 pass<\/span>.*1 fail<\/span>.*1 flagged<\/span>/);
  assert.match(html, /Most important fix · question 2</);
  assert.match(html, /<h3>Pinned now<\/h3><ol><li>owner\/b<\/li><li>owner\/c<\/li><\/ol>/);
  assert.match(html, /<span class="pc pin">Pin<\/span><span><code>owner\/a<\/code> Featured on its scorecard\.<\/span>/);
  assert.match(html, /<span class="pc drop">Drop<\/span>/);
  assert.match(html, /Portfolio overview of 2026-11-21/);
  assert.match(html, /<code id="draft-bio">I build data tools\.<\/code><button type="button" class="copy" data-copy="draft-bio">/);
  assert.match(html, /<textarea id="draft-readme" readonly aria-label="Draft profile README">I build &lt;tools&gt;\.\n\n- \[a\]/);
  assert.match(html, /Review these to rank them/);
  assert.match(html, /Contributions · context, not scored/);
  assert.match(html, /<code>other\/lib<\/code> · fixed a parser/);
  assert.doesNotMatch(html, /class="rec /);
});

test('a profile review without drafts, contributions or a next command leaves those sections out', () => {
  const { html } = render({ ...profile, draft: undefined, contributions: undefined, next: undefined });
  assert.doesNotMatch(html, /Drafts, for you to paste|Contributions ·|Review these to rank them/);
  assert.match(html, /Profile pins · up to 6/);
});

test('a pin the profile summary may have left out is marked check', () => {
  const pins = { ...profile.pins, source: 'profile page summary, may not be complete', changes: [{ name: 'owner/a', change: 'check', why: 'The summary named 2 of 6 pins; check the profile.' }] };
  const { html } = render({ ...profile, pins });
  assert.match(html, /<span class="pc check">Check<\/span><span><code>owner\/a<\/code> The summary named 2 of 6 pins; check the profile\.<\/span>/);
  assert.match(html, /<h3>Pins read, may be incomplete<\/h3>/);
});

test('a bio that needs no change is shown without a copy button', () => {
  const { html } = render({ ...profile, draft: { ...profile.draft, bio: 'No change', bioNote: 'The bio passes Introduction.' } });
  assert.match(html, /<h3 class="dh">Bio<\/h3><p>No change<\/p><p class="note">The bio passes Introduction\.<\/p>/);
  assert.doesNotMatch(html, /draft-bio/);
  assert.match(html, /data-copy="draft-readme"/);
});

test('a single review shows no profile sections, even with pins in its data', () => {
  assert.doesNotMatch(render({ ...review, pins: profile.pins }).html, /Profile pins · up to 6/);
});
