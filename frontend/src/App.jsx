import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
    const [formData, setFormData] = useState({
        season: '',
        city: '',
        team1: '',
        team2: '',
        toss_winner: '',
        toss_decision: '',
        venue: ''
    });

    const [prediction, setPrediction] = useState(null);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setPrediction(null);

        try {
            const response = await axios.post('http://127.0.0.1:5000/predict', formData);
            setPrediction(response.data.prediction);
        } catch (err) {
            setError(err.response ? err.response.data.error : "Server error. Check your Flask backend.");
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
            <h1 className="text-3xl font-bold mb-6">Match Winner Prediction</h1>
            <form className="space-y-4 w-80" onSubmit={handleSubmit}>
                {Object.keys(formData).map((key) => (
                    <div key={key}>
                        <label className="block mb-1 font-semibold capitalize">{key}</label>
                        <input
                            type="text"
                            name={key}
                            value={formData[key]}
                            onChange={handleChange}
                            className="w-full p-2 border border-gray-300 rounded"
                            required
                        />
                    </div>
                ))}
                <button
                    type="submit"
                    className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
                >
                    Predict Winner
                </button>
            </form>

            {prediction && (
                <div className="mt-6 p-4 bg-green-200 text-green-800 rounded">
                    Predicted Winner: <strong>{prediction}</strong>
                </div>
            )}

            {error && (
                <div className="mt-6 p-4 bg-red-200 text-red-800 rounded">
                    Error: {error}
                </div>
            )}
        </div>
    );
};

export default App;
