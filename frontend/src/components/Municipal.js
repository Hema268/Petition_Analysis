import React, { useEffect, useState } from "react";
import axios from "axios";

const Municipal = () => {
  const [petitions, setPetitions] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchPetitions(); // Fetch petitions on component load
  }, []);

  // Fetch petitions categorized under 'Municipal'
  const fetchPetitions = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/petitions");
      const municipalPetitions = response.data.filter(
        (petition) => petition.department === "Municipal department"
      );
      setPetitions(municipalPetitions); // Set filtered petitions for Municipal
    } catch (error) {
      console.error("Error fetching petitions:", error);
      setError("❌ Failed to load petitions. Please try again.");
    }
  };

  // Update petition status and send SMS notification
  const updateStatus = async (petitionId, newStatus) => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/petitions/${petitionId}/status`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: newStatus }),
        }
      );

      const data = await response.json();
      if (response.ok) {
        alert(`Status updated successfully! Notification sent to ${data.phone_number}`);
        fetchPetitions(); // Refresh petitions after updating the status
      } else {
        alert(`Failed to update status: ${data.error}`);
      }
    } catch (error) {
      console.error("Error updating status:", error);
      alert("An error occurred while updating the status.");
    }
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto mt-6">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">📜 Municipal Department Petitions</h2>

      {/* Display Error Message if Any */}
      {error && <p className="text-red-600 bg-red-100 p-2 rounded-md">{error}</p>}

      {/* Display Petitions */}
      {petitions.length > 0 ? (
        <ul className="space-y-4">
          {petitions.map((petition) => (
            <li
              key={petition.id}
              className="p-4 border rounded-lg shadow-md bg-gray-50 hover:shadow-lg transition duration-200"
            >
              <h3 className="font-semibold text-lg text-blue-700">{petition.file_name}</h3>
              <p className="text-gray-700 mt-1">
                <strong>📜 Extracted Text:</strong> {petition.extracted_text}
              </p>

              {/* Predicted Results */}
              <div className="mt-3 text-sm bg-blue-50 p-3 rounded-md">
                <p>
                  <strong>🏛 Department (BERT):</strong> {petition.department}
                </p>
                <p>
                  <strong>⚡ Urgency (Random Forest):</strong>{" "}
                  <span
                    className={`${
                      petition.priority === "high" ? "text-red-600 font-bold" : "text-green-600 font-bold"
                    }`}
                  >
                    {petition.priority === "high" ? "🔴 Urgent" : "🟢 Non-Urgent"}
                  </span>
                </p>
              </div>

              {/* Status Update Dropdown */}
              <div className="mt-4 flex items-center gap-4">
                <p className="text-sm font-medium">📌 Status:</p>
                <select
                  className="p-2 border rounded text-gray-700"
                  value={petition.status}
                  onChange={(e) => updateStatus(petition.id, e.target.value)}
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                </select>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-center text-gray-600">📭 No petitions found for the Municipal department.</p>
      )}
    </div>
  );
};

export default Municipal;
