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
