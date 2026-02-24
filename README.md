# zMindDumpZeu

## zPulse Event Bus Backend

This component logs system events to Google Sheets.

### Development Setup

1. Place your `google-credentials.json` in the root directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests (Mocked)

To verify functionality without external dependencies:

```bash
python3 -m src.test_eventbus
```

### Docker

Build and run:

```bash
docker build -t zpulse-eventbus .
docker run -p 8000:8000 zpulse-eventbus
```
