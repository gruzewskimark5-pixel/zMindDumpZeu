import { NextResponse } from 'next/server';
import Stripe from 'stripe';

// Initialize Stripe outside the handler for potential reuse across warm starts
const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
const stripe = stripeSecretKey ? new Stripe(stripeSecretKey) : null;

export async function POST() {
  if (!stripe) {
    console.error('STRIPE_SECRET_KEY is not defined');
    return NextResponse.json(
      { error: 'Stripe is not properly configured' },
      { status: 500 }
    );
  }

  const nextPublicUrl = process.env.NEXT_PUBLIC_URL;
  if (!nextPublicUrl) {
    console.error('NEXT_PUBLIC_URL is not defined');
    return NextResponse.json(
      { error: 'Site URL is not properly configured' },
      { status: 500 }
    );
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{
        price: 'price_1Qxxxxxxxxxxxx', // placeholder — we'll replace with real test price after first deploy
        quantity: 1,
      }],
      success_url: `${nextPublicUrl}/success`,
      cancel_url: nextPublicUrl,
      metadata: {
        source: 'zMindDumpZeu_beta',
        user_type: 'reentry_vet'
      }
    });

    return NextResponse.json({ url: session.url });
  } catch (error) {
    console.error('Stripe checkout error:', error);
    return NextResponse.json({ error: 'Checkout failed' }, { status: 500 });
  }
}
