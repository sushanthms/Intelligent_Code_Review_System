import React from "react";

export default function Results({ results }) {
  if (!results || Object.keys(results).length === 0) {
    return (
      <div className="bg-white shadow-md rounded-xl p-6">
        <p className="text-gray-500 text-center">No results yet.</p>
      </div>
    );
  }

  // Safely extract data
  const filename = results.filename || "Unknown File";
  const metrics = results.metrics || {};
  const score = results.score?.score ?? "N/A";
  const issues = results.issues || [];

  return (
    <div className="bg-white shadow-md rounded-xl p-6 space-y-4">
      <h2 className="text-2xl font-bold mb-2 text-blue-700">
        Results for {filename}
      </h2>

      {/* 🧮 Score Section */}
      <div className="bg-blue-50 p-3 rounded-lg">
        <p className="font-semibold">Score: {score}</p>
      </div>

      {/* 📊 Metrics Section */}
      <div className="bg-gray-50 p-3 rounded-lg">
        <h3 className="text-lg font-semibold mb-1">Metrics:</h3>
        {Object.keys(metrics).length === 0 ? (
          <p className="text-gray-500 italic">No metrics available</p>
        ) : (
          <ul className="list-disc list-inside space-y-1">
            {Object.entries(metrics).map(([key, value]) => (
              <li key={key}>
                <span className="font-medium">{key}:</span> {String(value)}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* 🚨 Issues Section */}
      <div className="bg-red-50 p-3 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">Issues:</h3>
        {issues.length === 0 ? (
          <p className="text-green-600 font-semibold">
            ✅ No issues found! Great job!
          </p>
        ) : (
          <ul className="space-y-3">
            {issues.map((issue, idx) => (
              <li
                key={idx}
                className="border border-red-300 rounded-lg p-3 bg-white"
              >
                <p className="font-semibold text-red-700">
                  Line {issue.lineno}: {issue.title} ({issue.severity})
                </p>
                <p className="text-gray-700 mt-1">
                  <strong>Snippet:</strong> {issue.snippet}
                </p>
                <p className="text-gray-700">
                  <strong>Why:</strong> {issue.why}
                </p>
                <p className="text-gray-700">
                  <strong>Fix:</strong> {issue.fix}
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
