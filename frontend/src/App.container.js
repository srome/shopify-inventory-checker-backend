import React, { useEffect, useState } from "react";
import App from "./App.component";
import "./App.css";

const AppContainer = ({ apiUrl }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState({});
  useEffect(() => {
    fetch(apiUrl, {
      method: "GET"
    })
      .then(res => res.json())
      .then(response => {
        setData(response);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setError(true);
        setLoading(false);
      });
  }, [apiUrl, loading]);

  if (error) {
    return <div>Error</div>;
  }

  return loading ? <div>Loading</div> : <App data={data} />;
};

export default AppContainer;
