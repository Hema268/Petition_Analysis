import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api';

export const submitPetition = (formData) =>
  axios.post(`${API_URL}/petitions`, formData, {
    headers: {
      'Content-Type': 'application/json' ,
    },
  });

export const getPetitions = () => axios.get(`${API_URL}/petitions`);
