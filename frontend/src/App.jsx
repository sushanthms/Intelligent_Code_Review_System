import React, { useState } from "react";
import Editor from "./components/Editor";
import Results from "./components/Results";
import axios from "axios";

export default function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeCode = async (code) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post("http://localhost:8000/analyze", {
        filename: "submission.py",
        content: code,
      });
      setResults(response.data);
    } catch (err) {
      console.error("Analysis failed:", err);
      setError("Error analyzing code. Please check your backend connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <h1 className="text-3xl font-extrabold text-center text-blue-700 mb-6">
        🧠 Intelligent Code Review System
      </h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 p-3 rounded mb-4 text-center">
          {error}
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-6 max-w-7xl mx-auto">
        <Editor onAnalyze={analyzeCode} loading={loading} />

        {loading ? (
          <div className="flex justify-center items-center bg-white shadow-md rounded-xl p-6">
            <p className="text-blue-600 font-medium animate-pulse">
              Analyzing your code...
            </p>
          </div>
        ) : (
          <Results results={results} />
        )}
      </div>

      
    </div>
  );
}
