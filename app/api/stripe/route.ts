import { NextResponse } from 'next/server';
import Stripe from 'stripe';

const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
const STRIPE_PRICE_ID = process.env.STRIPE_PRICE_ID;
const NEXT_PUBLIC_URL = process.env.NEXT_PUBLIC_URL;

if (!STRIPE_SECRET_KEY) {
  throw new Error('STRIPE_SECRET_KEY is not defined');
}

const stripe = new Stripe(STRIPE_SECRET_KEY);

export async function POST() {
  try {
    if (!STRIPE_PRICE_ID) {
      throw new Error('STRIPE_PRICE_ID is not defined');
    }

    if (!NEXT_PUBLIC_URL) {
      throw new Error('NEXT_PUBLIC_URL is not defined');
    }

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{
        price: STRIPE_PRICE_ID,
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
    console.error('[Stripe] Checkout error:', error);
    return NextResponse.json({ error: 'Checkout failed' }, { status: 500 });
  }
}
