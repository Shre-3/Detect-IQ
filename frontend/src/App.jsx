import React, { useState } from "react";
import "./index.css"; // Ensure Tailwind CSS is properly configured
import UrlForm from "./components/UrlForm";
import Result from "./components/Results";

// Import Lucide Icons
import { Shield } from "lucide-react";

const App = () => {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0f172a] to-[#1e293b] p-6">
      <div className="bg-[#1e293b] shadow-lg rounded-2xl p-8 w-full max-w-lg border border-[#334155]">
        {/* Header Section */}
        <div className="flex flex-col items-center mb-6 space-y-3">
          {/* 🔥 Cool Shield Icon 🔥 */}
          <Shield className="h-14 w-14 text-[#06b6d4] drop-shadow-[0px_0px_10px_#06b6d4] rotate-[-3deg]" />

          <h1 className="text-3xl font-bold text-[#e2e8f0]">Detect-IQ</h1>
          <p className="text-[#94a3b8] text-sm text-center">
            Secure your browsing with real-time URL detection.
          </p>
        </div>

        {/* URL Input Form */}
        <UrlForm setResult={setResult} />

        {/* Results Section */}
        {result && (
          <div className="mt-6">
            <Result result={result} />
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
