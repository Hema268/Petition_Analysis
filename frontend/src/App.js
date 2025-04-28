import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, Navigate } from "react-router-dom";
import PetitionForm from "./components/PetitionForm";
import PetitionList from "./components/PetitionList";
import Login from "./components/Login";
import Revenue from "./components/Revenue"; // Import Revenue component
import Municipal from "./components/Municipal"; // Import Municipal component

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [selectedDepartment, setSelectedDepartment] = useState("");

  const handleLogin = (department) => {
    setIsAuthenticated(true);
    setSelectedDepartment(department); // Store the selected department after login
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-500 to-indigo-700 text-white flex justify-center items-center">
      <div className="bg-white text-gray-900 rounded-2xl shadow-2xl max-w-4xl p-10">
        <h1 className="text-4xl font-extrabold mb-4 flex items-center justify-center gap-2">
          📄 Petition Analysis System
        </h1>
        <p className="text-lg text-gray-600 mb-6 text-center">
          Upload petitions, analyze issues, and track resolutions with ease.
        </p>

        <nav className="mb-6 flex justify-center gap-6">
          <Link to="/submit" className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            🚀 Submit Petition
          </Link>
          <Link to="/login" className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600">
            📜 View Petitions
          </Link>
        </nav>

        <Routes>
          <Route path="/submit" element={<PetitionForm />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />

          {/* Redirect based on selected department after login */}
          <Route
            path="/revenue"
            element={isAuthenticated && selectedDepartment === "Revenue" ? <Revenue /> : <Navigate to="/login" />}
          />
          <Route
            path="/municipal"
            element={isAuthenticated && selectedDepartment === "Municipal" ? <Municipal /> : <Navigate to="/login" />}
          />

          {/* Default Route */}
          <Route path="*" element={<h2 className="text-xl font-medium">🏠 Welcome! Choose an option above.</h2>} />
        </Routes>
      </div>
    </div>
  );
}

function AppWrapper() {
  return (
    <Router>
      <App />
    </Router>
  );
}

export default AppWrapper;
