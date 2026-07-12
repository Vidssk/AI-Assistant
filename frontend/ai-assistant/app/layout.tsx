import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "N.O.V.A — AI Assistant Dashboard",
  description:
    "Real-time AI assistant command dashboard with live backend telemetry and demo snapshot fallback.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
