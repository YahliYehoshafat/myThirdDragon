import '../App.css';
import NavBar from '../components/NavBar';
import { useLocation } from "react-router-dom";
import './DashBoard.css';
import LineGraph from '../components/LineGraph';
import React, { useEffect, useState } from "react";
import BarGraph from '../components/BarGraph';

function DashBoard() {
  // Get pet_id from the navigation state
  const location = useLocation();
  const { pet_id } = location.state || {};
  // State to hold fetched metrics for the pet
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    if (!pet_id) return;
    // Fetch metrics from backend when pet_id is available
    const fetchData = async () => {
      try {
        const res = await fetch(`http://localhost:5000/metrics/${pet_id}`);
        const json = await res.json();
        setMetrics(json);
      } catch (err) {
        console.error("Error fetching metrics:", err);
      }
    };

    fetchData();
  }, [pet_id]);
  // Render nothing until metrics are fetched
  if (!metrics) return null;
  return (
    <>
      <NavBar />
      <h1 style={{ marginTop: '120px', fontSize: "90px", textAlign: "center" }}>
        BI
      </h1>
      <div className="dashboard-wrapper">
        <div className="row">
          <div className="box">
            was the pet happiest? {metrics.most_happiness_hour}
          </div>
          <div className="box">
            Which action was performed the most? {metrics.most_popular_action}
          </div>
        </div>
        <div className="row">
          <div className="box">
            How many times was the overall score less than 70? {metrics.overall_score_under}
          </div>
          <div className="box">
            Average time between actions in minute: {metrics.average_time_between_actions}
          </div>
        </div>
        <div className="box center-box">
          happiness average = {metrics.happiness_avg}
        </div>
        <div className="charts">
          <LineGraph
            labels={metrics.get_timestamp}
            pet_data={metrics.points_state}
            label="points state"
          />
          <LineGraph
            labels={metrics.get_timestamp}
            pet_data={metrics.happiness_state}
            label="happiness state"
          />
        </div>
        <div className="charts">
          <BarGraph
            labels={metrics.dates_range}
            pet_data={metrics.actions_performed}
            label="actions performed"
          />
          <BarGraph
            labels={metrics.last_24_hour}
            pet_data={metrics.energy_state}
            label="energy state"
          />
        </div>
      </div>
    </>
  );
}

export default DashBoard;