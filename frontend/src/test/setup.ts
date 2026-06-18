import '@testing-library/jest-dom';

// jsdom does not implement EventSource. Provide a no-op stub so hooks that
// open an SSE connection can be exercised without a real network.
class MockEventSource {
  static CONNECTING = 0;
  static OPEN = 1;
  static CLOSED = 2;
  readyState = MockEventSource.OPEN;
  onmessage: ((e: MessageEvent) => void) | null = null;
  onerror: ((e: Event) => void) | null = null;
  close() {
    this.readyState = MockEventSource.CLOSED;
  }
}

globalThis.EventSource = MockEventSource as unknown as typeof EventSource;
