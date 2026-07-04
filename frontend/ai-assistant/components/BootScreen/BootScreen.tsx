"use client";

import Frame from "@/components/Frame/Frame";

interface BootScreenProps {
  onActivate: () => void;
}

export default function BootScreen({
  onActivate,
}: BootScreenProps) {

  return (
    <div>

      {/* Top Right */}
      {/* <div className="absolute top-8 right-10 text-cyan-300">
        AI MARK I
      </div> */}

      {/* Center */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">

        {/* Blender planet will be behind this */}
        <h1 className="text-6xl font-bold text-cyan-300 tracking-widest">
          JARVIS
        </h1>

        <p className="mt-4 text-cyan-200">
          Artificial Intelligence System
        </p>

        <button
          onClick={onActivate}
          className="
            mt-12
            px-12
            py-3
            border
            border-cyan-400
            text-cyan-300
            hover:bg-cyan-400
            hover:text-black
            transition
          "
        >
          ACTIVATE
        </button>

      </div>

    </div>
  );
}