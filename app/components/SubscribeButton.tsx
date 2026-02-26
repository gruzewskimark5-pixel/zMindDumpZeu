'use client';

import { useState } from 'react';

export default function SubscribeButton() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubscribe = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/stripe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priceId: 'price_1Qxxxxxxxxxxxx' }) // we'll replace with real test price after deploy
      });

      if (!res.ok) {
        throw new Error('Checkout failed. Please try again.');
      }

      const { url } = await res.json();
      if (!url) {
        throw new Error('No checkout URL returned');
      }

      window.location.href = url;
    } catch (err) {
      console.error('Checkout error:', err);
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={handleSubscribe}
        disabled={loading}
        className="w-full bg-lime-400 hover:bg-lime-300 text-black font-bold text-2xl py-8 rounded-2xl disabled:opacity-50"
      >
        {loading ? "OPENING CHECKOUT..." : "GET LIFETIME ACCESS — $19/mo"}
      </button>

      {error && (
        <p className="text-red-500 mt-2 text-sm text-center">{error}</p>
      )}
    </>
  );
}
