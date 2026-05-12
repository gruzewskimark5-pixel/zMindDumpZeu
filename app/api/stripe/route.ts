import { NextResponse } from 'next/server';
import Stripe from 'stripe';

let stripe: Stripe | null = null;

export async function POST() {
  const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
  const STRIPE_PRICE_ID = process.env.STRIPE_PRICE_ID;
  const NEXT_PUBLIC_URL = process.env.NEXT_PUBLIC_URL;

  const required = { STRIPE_SECRET_KEY, STRIPE_PRICE_ID, NEXT_PUBLIC_URL };

  for (const [key, value] of Object.entries(required)) {
    if (!value) {
      console.error(`[Stripe] Checkout error: ${key} is not defined`);
      return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
  }

  if (!stripe) {
    stripe = new Stripe(STRIPE_SECRET_KEY!);
  }
  const stripeClient = stripe;

  try {
    const session = await stripeClient.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{
        price: STRIPE_PRICE_ID!,
        quantity: 1,
      }],
      success_url: `${NEXT_PUBLIC_URL}/success`,
      cancel_url: `${NEXT_PUBLIC_URL}`,
      metadata: {
        source: 'zMindDumpZeu_beta',
        user_type: 'reentry_vet'
      }
    });

    return NextResponse.json({ url: session.url });
  } catch (error) {
    const message = error instanceof Error ? error.message : error;
    console.error('[Stripe] Checkout error:', message);
    return NextResponse.json({ error: 'Checkout failed' }, { status: 500 });
  }
}
