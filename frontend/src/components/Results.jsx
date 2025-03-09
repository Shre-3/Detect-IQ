import React from "react";
import { AlertTriangle, ShieldCheck } from "lucide-react";

const Result = ({ result }) => {
  if (result.error) {
    return (
      <div className="bg-[#7f1d1d] border-l-4 border-red-500 text-red-300 p-4 rounded-lg shadow-md flex items-center">
        <AlertTriangle className="h-6 w-6 mr-3 text-red-400" />
        <span className="text-lg font-semibold">{result.error}</span>
      </div>
    );
  }

  return (
    <div className="bg-[#1e293b] border border-[#334155] p-6 rounded-2xl shadow-md transition-transform transform hover:scale-105">
      <h2 className="text-2xl font-bold text-[#06b6d4] flex items-center">
        🔍 URL Analysis Result
      </h2>

      <p className="mt-3 text-[#94a3b8]">
        <strong className="text-[#e2e8f0]">🔗 URL:</strong>{" "}
        <span className="break-all">{result.url}</span>
      </p>

      <p className="mt-2 flex items-center text-lg">
        <strong className="text-[#e2e8f0]">🛡 Prediction:</strong>
        <span className="ml-2 flex items-center">
          {result.prediction?.toLowerCase() === "legitimate" ? (
            <>
              <ShieldCheck className="h-6 w-6 text-green-400 mr-2" />
              <span className="capitalize text-green-300">
                {result.prediction}
              </span>
            </>
          ) : result.prediction?.toLowerCase() === "phishing" ? (
            <>
              <AlertTriangle className="h-6 w-6 text-yellow-400 mr-2" />
              <span className="capitalize text-yellow-300">
                {result.prediction}
              </span>
            </>
          ) : (
            <span className="text-red-400">Invalid prediction</span>
          )}
        </span>
      </p>
    </div>
  );
};

export default Result;
