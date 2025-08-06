import React, { useEffect, useState } from "react";
import axios from "axios";
import MapView from "./MapView";

function App() {
  const [dcs, setDcs] = useState([]);
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(true);

  // Use your deployed backend URL or environment variable
  const apiUrl = process.env.REACT_APP_API_URL || "";

  useEffect(() => {
    const fetchNodes = async () => {
      setLoading(true);
      try {
        const res = await axios.get(`${apiUrl}/api/nodes`);
        setDcs(res.data.filter(n => n.type === "DistributionCenter"));
        setStores(res.data.filter(n => n.type === "Store"));
      } catch (err) {
        setDcs([]);
        setStores([]);
      }
      setLoading(false);
    };
    fetchNodes();
  }, [apiUrl]);

  return (
    <div>
      <header style={{ background: "#2563eb", color: "white", padding: 20, textAlign: "center" }}>
        <h1 style={{ margin: 0, fontSize: 32, fontWeight: 600 }}>
          🏭 Supply Chain Digital Twin
        </h1>
        <p style={{ margin: "8px 0 0 0", opacity: 0.9, fontSize: 16 }}>
          US Map Visualization of Distribution Centers and Stores
        </p>
      </header>
      <div style={{ margin: 24 }}>
        {loading ? (
          <div>Loading map...</div>
        ) : (
          <MapView dcs={dcs} stores={stores} shipments={[]} highlight={null} />
        )}
      </div>
    </div>
  );
}

export default App;
