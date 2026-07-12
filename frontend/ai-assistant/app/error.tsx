"use client";

import { useEffect } from "react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <main className="flex h-screen w-screen items-center justify-center bg-black p-6">
      <div className="max-w-md w-full border border-cyan-500/30 rounded p-8 text-center">
        <p className="font-mono text-[10px] tracking-widest uppercase text-cyan-400/60 mb-4">
          System Fault
        </p>
        <h1 className="text-cyan-300 text-lg font-semibold tracking-wide mb-2">
          Dashboard Unavailable
        </h1>
        <p className="text-cyan-200/70 text-sm mb-6">
          An unexpected error occurred. Reinitialize to try again.
        </p>
        <button
          type="button"
          onClick={reset}
          className="px-8 py-2 border border-cyan-400 text-cyan-300 text-sm tracking-wide hover:bg-cyan-400 hover:text-black transition"
        >
          Reinitialize
        </button>
      </div>
    </main>
  );
}
