'use client';

import { useState } from 'react';
import { handleSubscribeAction } from './actions';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubscribe = () => handleSubscribeAction(setLoading, setError);

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex flex-col items-center justify-center p-8">
      <div className="text-center max-w-md">
        <div className="text-6xl mb-4">⚡</div>
        <h1 className="text-5xl font-black tracking-tighter mb-2">zMindDumpZeu</h1>
        <p className="text-2xl text-lime-400 mb-8">AI Education for Reentry Warriors</p>

        <div className="bg-zinc-900 p-8 rounded-3xl mb-8 border border-lime-500/30">
          <p className="text-xl font-bold mb-4">DesireZ War Cry</p>
          <p className="text-zinc-400 mb-8">“I survived the streets. Now I’m building the way out.”</p>
          <p className="text-xl font-bold">FaithZ Whisper</p>
          <p className="text-zinc-400">“One lesson. One day. One roof at a time.”</p>
        </div>

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

        <p className="text-xs text-zinc-500 mt-6">First 50 Florida vets = lifetime 50% off + zEXZ housing credits for Revolt</p>
      </div>
    </div>
  );
}
