import React, { useState } from 'react';

export default function Editor({ onAnalyze, loading }) {
  const [code, setCode] = useState('print("Hello, world!")');

  return (
    <div className="bg-white shadow-md rounded-xl p-4 flex flex-col">
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="flex-1 border border-gray-300 rounded-lg p-3 font-mono text-sm mb-4 focus:ring focus:ring-blue-200"
        rows={14}
        placeholder="Paste your Python code here..."
      />
      <button
        onClick={() => onAnalyze(code)}
        disabled={loading}
        className={`py-2 rounded-lg text-white font-semibold ${
          loading ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {loading ? 'Analyzing...' : 'Run Analysis'}
      </button>
    </div>
  );
}
