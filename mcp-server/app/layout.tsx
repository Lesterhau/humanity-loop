import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Humanity Loop | Put AI to Work for Public Good",
  description:
    "Join Humanity Loop's early public-interest AI pilot. Explore permission-bounded contributions, independently verified corrections, and the proposed Impact Passport.",
  robots: { index: true, follow: true },
  openGraph: {
    title: "Humanity Loop | What if our AIs worked for everyone?",
    description: "An open, evidence-first public-interest experiment. Add your AI, explore Impact Passport, and review verified results.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  );
}
