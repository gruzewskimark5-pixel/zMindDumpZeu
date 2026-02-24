import { NextResponse } from 'next/server';
import Stripe from 'stripe';

export async function POST() {
  const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
  if (!stripeSecretKey) {
    console.error('[Stripe] Checkout error: Missing STRIPE_SECRET_KEY');
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }

  const stripe = new Stripe(stripeSecretKey);

  try {
    const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
    const STRIPE_PRICE_ID = process.env.STRIPE_PRICE_ID;
    const NEXT_PUBLIC_URL = process.env.NEXT_PUBLIC_URL;

    if (!STRIPE_SECRET_KEY) {
      console.error('[Stripe] Checkout error: STRIPE_SECRET_KEY is not defined');
      return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }

    if (!STRIPE_PRICE_ID) {
      console.error('[Stripe] Checkout error: STRIPE_PRICE_ID is not defined');
      return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }

    if (!NEXT_PUBLIC_URL) {
      console.error('[Stripe] Checkout error: NEXT_PUBLIC_URL is not defined');
      return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }

    const stripe = new Stripe(STRIPE_SECRET_KEY);

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
