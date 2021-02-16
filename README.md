[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Notify Zulip Action

Send Github Actions workflow status notifications to Zulip regarding failures, warnings or even success.

### Example workflow

```yaml
      - name: Report if failure
        if: always()
        uses: amanagr/notify-zulip-action@master
        with:
          status: ${{ job.status }}
          notify_when: 'failure'
        env:
          ZULIP_BOT_KEY: ${{ secrets.ZULIP_BOT_KEY }}
          STREAM: 'test'
```
