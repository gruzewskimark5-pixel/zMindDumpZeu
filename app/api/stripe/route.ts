import { NextResponse } from 'next/server';
import Stripe from 'stripe';

export async function POST() {
  if (!process.env.STRIPE_SECRET_KEY) {
    console.error('[Stripe] Missing STRIPE_SECRET_KEY environment variable');
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }

  if (!process.env.NEXT_PUBLIC_URL) {
    console.error('[Stripe] Missing NEXT_PUBLIC_URL environment variable');
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }

  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{
        price: 'price_1Qxxxxxxxxxxxx', // placeholder — we'll replace with real test price after first deploy
        quantity: 1,
      }],
      success_url: `${process.env.NEXT_PUBLIC_URL}/success`,
      cancel_url: `${process.env.NEXT_PUBLIC_URL}`,
      metadata: {
        source: 'zMindDumpZeu_beta',
        user_type: 'reentry_vet'
      }
    });

    return NextResponse.json({ url: session.url });
  } catch (error) {
    console.error('[Stripe] Checkout error:', error);
    return NextResponse.json({ error: 'Checkout failed' }, { status: 500 });
  }
}
