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
  lists still in the page (Strategies tiles, hidden radar) mirror hl-scanner's `signals.py` and are
  labelled old rules / reference - change both together.


## Page layout (keep current)
1. Countdown bar: candle closes, options expiries, quad witching, FOMC/CPI/jobs. **Extend the FOMC / CPI / NFP date lists each year** (federalreserve.gov, bls.gov schedules).
2. 🤖 Bots: `bot_board.json` (hl-scanner daily report, `bot2status.public_board`, copied by live.yml's Rotation board steps). bot2 1D/1H status + stale flag + last run, this and next month's coin list, old bot (manage-only) with its old lists collapsed. Also sets the bot2 pills in Strategies. Shows "status unavailable" when the file is missing.
3. 🔄 Money rotation: `rotation_board.json`, pushed by hl-scanner live.yml after each rotation run.
4. 🧠 Strategies: bot2 tiles, then the old bot's rules (OLD RULES, reference), then **Paper tests** (`paper_board.json`, pushed hourly by hl-scanner scan.yml). "Being tested" first (crowd fade, OI breakout, whale piling copy, 5-whale copy, BTC 4H, young coins, 2 rotation models), then "Reference" (live rules on paper, ChatGPT votes). The full registry is in hl-scanner CLAUDE.md.
5. Market, Your account, Realised P/L, GMX, Will anything fire? (bot2's rules on bot2's current-month list from `bot_board.json`; the old % radar is hidden and no longer loads), Live vs backtest (old bot).
Published JSON files hold market data, paper results or bot status labels / public coin lists only: never addresses, balances, sizes, positions or P/L.
