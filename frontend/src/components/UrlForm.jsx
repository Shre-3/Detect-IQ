import React, { useState } from "react";
import axios from "axios";

const UrlForm = ({ setResult }) => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(
        "https://detect-iq.onrender.com/predict",
        {
          url,
        }
      ); 
      console.log("Response from backend:", response.data); 

      if (response.data.prediction) {
        setResult({ url: url, prediction: response.data.prediction });
      } else {
        setResult({ error: "Invalid prediction response" });
      }
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: "Failed to connect to the server." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-6 rounded-xl shadow-lg w-full max-w-md"
    >
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter URL..."
        required
        className="p-3 border rounded-lg w-full"
      />

      <button
        type="submit"
        disabled={loading}
        className="mt-3 py-2 px-4 bg-blue-500 text-white rounded-lg"
      >
        {loading ? "Checking..." : "Check URL"}
      </button>
    </form>
  );
};

export default UrlForm;
