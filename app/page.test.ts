import test from 'node:test';
import assert from 'node:assert';
import { handleSubscribeAction } from './actions.ts';

// Mocking the environment
const mockFetch = (response: any) => {
  return Promise.resolve({
    ok: response.ok,
    json: () => Promise.resolve(response.body),
  });
};

test('handleSubscribeAction handles missing URL in response', async () => {
  let loadingState = false;
  let errorState: string | null = null;

  const setLoading = (val: boolean) => { loadingState = val; };
  const setError = (val: string | null) => { errorState = val; };
  const mockWindow = {
    location: {
      href: ''
    }
  };

  // Mock successful response but missing url
  const fetchMock = () => mockFetch({
    ok: true,
    body: {}
  });

  await handleSubscribeAction(setLoading, setError, fetchMock, mockWindow);

  assert.strictEqual(loadingState, false, 'Loading should be false after completion');
  assert.strictEqual(errorState, 'Something went wrong. Please try again.', 'Error state should be set correctly');
  assert.strictEqual(mockWindow.location.href, '', 'Should not have redirected');
});

test('handleSubscribeAction redirects on successful response with URL', async () => {
    let loadingState = false;
    let errorState: string | null = null;
    const mockWindow = {
      location: {
        href: ''
      }
    };

    const setLoading = (val: boolean) => { loadingState = val; };
    const setError = (val: string | null) => { errorState = val; };

    const fetchMock = () => mockFetch({
      ok: true,
      body: { url: 'https://checkout.stripe.com/test' }
    });

    await handleSubscribeAction(setLoading, setError, fetchMock, mockWindow);

    assert.strictEqual(loadingState, false, 'Loading should be false after completion');
    assert.strictEqual(errorState, null, 'Error state should be null');
    assert.strictEqual(mockWindow.location.href, 'https://checkout.stripe.com/test', 'Should have redirected to the correct URL');
  });

test('handleSubscribeAction handles fetch failure', async () => {
    let loadingState = false;
    let errorState: string | null = null;
    const mockWindow = {
      location: {
        href: ''
      }
    };

    const setLoading = (val: boolean) => { loadingState = val; };
    const setError = (val: string | null) => { errorState = val; };

    const fetchMock = () => mockFetch({
      ok: false,
      body: { error: 'Internal Server Error' }
    });

    await handleSubscribeAction(setLoading, setError, fetchMock, mockWindow);

    assert.strictEqual(loadingState, false, 'Loading should be false after completion');
    assert.strictEqual(errorState, 'Something went wrong. Please try again.', 'Error state should be set');
    assert.strictEqual(mockWindow.location.href, '', 'Should not have redirected');
  });
