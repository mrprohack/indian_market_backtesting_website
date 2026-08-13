import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BharatBacktest",
  description: "Simple-to-advanced backtesting for Indian markets.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
