import React, { useState } from "react";
import axios from "axios";

const PetitionForm = () => {
  const [file, setFile] = useState(null);
  const [name, setName] = useState(""); // Add name state
  const [phoneNumber, setPhoneNumber] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [extractedText, setExtractedText] = useState("");
  const [department, setDepartment] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");
    setExtractedText("");
    setDepartment("");

    if (!file || !phoneNumber || !name) {
      setError("⚠️ All fields are required!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", name);
    formData.append("phone_number", phoneNumber);

    try {
      setIsLoading(true);
      const response = await axios.post("http://127.0.0.1:5000/api/petitions", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage("✅ Petition submitted successfully!");
      setExtractedText(response.data.extracted_text);
      setDepartment(response.data.department);
    } catch (error) {
      setError("❌ Error submitting petition.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6 rounded-xl shadow-lg bg-white">
      <h2 className="text-3xl font-bold mb-4">📄 Submit Petition</h2>

      {/* Display Error or Success Messages */}
      {error && <p className="text-red-600 bg-red-100 p-3 rounded-md mb-4">{error}</p>}
      {message && <p className="text-green-600 bg-green-100 p-3 rounded-md mb-4">{message}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
      <label className="text-gray-700 font-medium mb-1">📂 Upload Image</label>
      <input
          type="file"
          accept=".jpg,.jpeg,.png,.pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="block w-full p-3 border rounded-md"
          required
        />
        {/* Name Input */}
        <label className="text-gray-700 font-medium mb-1">👤 Enter Your Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter your full name"
          className="block w-full p-3 border rounded-md"
          required
        />

         {/* Phone Number Input */}
        <label className="text-gray-700 font-medium mb-1">📞 Enter Your Phone Number</label>
        <input
          type="text"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          placeholder="+91XXXXXXXXXX"
          className="block w-full p-3 border rounded-md"
          required
        />
        <button
          type="submit"
          disabled={isLoading}
          className="block w-full bg-blue-500 text-white py-3 rounded-md"
        >
          {isLoading ? "⏳ Submitting..." : "🚀 Submit"}
        </button>
      </form>

      {extractedText && (
        <div className="mt-4 bg-gray-100 p-4 rounded-lg">
          <p>📝 <strong>Extracted Text:</strong> {extractedText}</p>
          <p>🏛 <strong>Department:</strong> {department}</p>
        </div>
      )}
    </div>
  );
};

export default PetitionForm;
