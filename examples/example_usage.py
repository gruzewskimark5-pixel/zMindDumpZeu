from datetime import datetime, timezone
from jules.client import JulesClient
from jules.models import RivalryEvent

def main():
    client = JulesClient(
        baseurl="https://api.jules.test",
        apikey="test-key"
    )

    # --- Submit a rivalry event ---
    event = RivalryEvent(
        sourceeventid="evt-123",
        playeraid="player-A",
        playerbid="player-B",
        roundid="round-001",
        holenumber=16,
        di=0.62,
        eventtype="LEADCHANGE",
        baseweight=0.20,
        eventts=datetime.now(timezone.utc),
    )

    # Note: This will fail unless a real/mock server is running at baseurl
    try:
        ack = client.submit_event(event)
        print("Event submitted:", ack)
    except Exception as e:
        print("Submission failed (expected if no server):", e)

    # --- Fetch a round ---
    try:
        rnd = client.getround("round-001")
        print("Round:", rnd)
    except Exception as e:
        print("Fetch round failed:", e)

if __name__ == "__main__":
    main()
