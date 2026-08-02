import React, { useState } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function Dashboard() {
    const [statementId, setStatementId] = useState('');
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchAnalytics = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://127.0.0.1:8000/analytics/${statementId}`);
            setData(response.data);
        } catch (error) {
            alert('Error fetching data');
        }
        setLoading(false);
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial' }}>
            <h1>Bank Statement Insights</h1>

            <div>
                <input
                    type="number"
                    placeholder="Enter Statement ID"
                    value={statementId}
                    onChange={(e) => setStatementId(e.target.value)}
                />
                <button onClick={fetchAnalytics} disabled={loading}>
                    {loading ? 'Loading...' : 'Fetch Analytics'}
                </button>
            </div>

            {data && (
                <div>
                    <h2>Financial Summary</h2>
                    <p>Income: ₹{data.financial_summary.income}</p>
                    <p>Expenses: ₹{data.financial_summary.expenses}</p>
                    <p style={{ fontSize: '20px', fontWeight: 'bold' }}>
                        Surplus: ₹{data.financial_summary.surplus}
                    </p>

                    <h2>Spend by Category</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie data={data.spend_by_category} dataKey="total" nameKey="category" cx="50%" cy="50%" outerRadius={100}>
                                {data.spend_by_category.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c'][index % 4]} />
                                ))}
                            </Pie>
                            <Tooltip />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>

                    {data.recommendations.length > 0 && (
                        <div>
                            <h2>Recommendations</h2>
                            {data.recommendations.map((rec, idx) => (
                                <div key={idx} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
                                    <h3>{rec.recommendation}</h3>
                                    <p>{rec.reasoning}</p>
                                    <p>Estimated Annual Impact: ₹{rec.estimated_impact.toFixed(0)}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default Dashboard;