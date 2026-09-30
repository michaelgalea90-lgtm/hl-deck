# Working on hl-deck

Single-page dashboard (`index.html`) for the hl-scanner trading bot. It reads
public Hyperliquid / CoinGecko data in the browser; wallet addresses are
stored in the viewer's browser only. The bot itself lives in
michaelgalea90-lgtm/hl-scanner (see its CLAUDE.md).

## Claude is the boss, ChatGPT is the second opinion
- Every PR gets an automatic ChatGPT review (`gpt_review.yml`); `@gpt <question>`
  in any issue / PR comment gets an answer.
- Before merging: fix each real point it raises or reply on the PR saying why
  not; when it disagrees, Claude decides and writes the reason.
- Check changes in a real browser at phone width (~390px): no horizontal
  scroll, no JS errors.
- bot2's coin list is NOT hardcoded: it comes from `bot_board.json` (monthly top-10). The old bot's
  rules and lists in the page ("Old bot" card, reference only) mirror hl-scanner's `signals.py` -
  change both together.


## Page layout (keep current)
What matters now first; scannable in 5 seconds, longer text only behind toggles. Each area is
one collapsible card (`<details class="dk">`) with a label (status now / fake money / info
only / this browser only / reference) and a one-line summary when closed. Explanations live
in closed "What is this?" toggles (`<details class="why">`), not in paragraphs. Sections sit
in page order in the HTML (no script moves them). All times are shown in Sydney time and say so.
Every data file is optional: a missing file shows "unavailable" in its card, never a JS error.
- Sticky header: name, last-update time, refresh (re-runs every card via `window.hlRefreshers`),
  and the status strip: chips for bot2 1D / 1H status, will anything fire, paper tests, Others
  dominance, old bot. Each card's script sets its own chip (`HLD.chip`); tapping one opens its card.
0. Countdown row: candle closes, options expiries, quad witching, FOMC/CPI/jobs (events at the
   same moment share one card). **Extend the FOMC / CPI / NFP date lists each year** (federalreserve.gov, bls.gov schedules).
1. 🤖 Bots (open by default): `bot_board.json` (hl-scanner daily report, `bot2status.public_board`, copied by live.yml's Rotation board steps). bot2 1D/1H status + stale flag + last run, each sleeve's rules and launch cap, this and next month's coin list, old bot manage-only line, status key. Shows "status unavailable" when the file is missing.
2. 🎯 Will anything fire? (open by default): bot2's rules on bot2's current-month list from `bot_board.json`, live Hyperliquid prices. One row per coin: rule dots + gap to the breakout level for 1D and 1H; tap a coin for each rule in words.
3. 🧪 Paper tests (open by default): `paper_board.json`, pushed hourly by hl-scanner scan.yml. Four totals, then a scoreboard (progress bar to the trade target + average R). "Being tested" first (crowd fade, OI breakout, whale piling copy, 5-whale copy, BTC 4H, young coins, quiet breakout, 2 rotation models), then "Reference" (old bot rules on paper, ChatGPT votes). One tappable line per test. The full registry is in hl-scanner CLAUDE.md.
4. 🌍 Market (info only): alt-season gauge (CoinGecko) + Money rotation (`rotation_board.json`, pushed by hl-scanner live.yml after each rotation run) + sector-watch regime line (`sector_rotation_board.json`, scan.yml) + TradingView catch-up list download (`tradingview_catchup.txt`, only shown when it has tickers). `laggards_board.json` is still published but not shown (laggard hunt switched off).
5. 💰 Your wallet (this browser only): account, positions, realised P/L, GMX, read from an address the viewer types in and keeps in their own browser. The saved sub-account is the OLD bot's.
6. 📚 Old bot (reference): live vs backtest trade check for the old bot's remaining trades, old rules, old coin lists (from `bot_board.json`).
Published JSON files hold market data, paper results or bot status labels / public coin lists only: never addresses, balances, sizes, positions or P/L.
