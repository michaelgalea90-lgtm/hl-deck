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
- Coin lists in the page mirror hl-scanner's `signals.py` - change both together.


## Page layout (keep current)
1. Countdown bar: candle closes, options expiries, quad witching, FOMC/CPI/jobs. **Extend the FOMC / CPI / NFP date lists each year** (federalreserve.gov, bls.gov schedules).
2. 🔄 Money rotation: `rotation_board.json`, pushed by hl-scanner live.yml after each rotation run.
3. 🧠 Strategies: live rule tiles, then **Paper tests** (`paper_board.json`, pushed hourly by hl-scanner scan.yml). "Being tested" first (crowd fade, OI breakout, whale piling copy, 5-whale copy, BTC 4H, young coins, 2 rotation models), then "Reference" (live rules on paper, ChatGPT votes). The full registry is in hl-scanner CLAUDE.md.
4. Market, Your account, Realised P/L, GMX, Signal radar, Will anything fire?, Live vs backtest.
Published JSON files hold market data or paper results only: never addresses or balances.
