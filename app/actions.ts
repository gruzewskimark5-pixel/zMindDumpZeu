export async function handleSubscribeAction(
  setLoading: (loading: boolean) => void,
  setError: (error: string | null) => void,
  fetchApi: any = globalThis.fetch,
  windowObj: any = globalThis.window
) {
  setLoading(true);
  setError(null);
  try {
    const res = await fetchApi('/api/stripe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!res.ok) {
      throw new Error('Checkout failed. Please try again.');
    }

    const { url } = await res.json();
    if (!url) {
      throw new Error('No checkout URL returned');
    }

    if (windowObj && windowObj.location) {
      windowObj.location.href = url;
    }
  } catch (err) {
    console.error('Checkout error:', err);
    setError('Something went wrong. Please try again.');
  } finally {
    setLoading(false);
  }
}
