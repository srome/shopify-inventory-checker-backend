import React from "react";
import ProductGrid from "./ProductGrid";
import "./App.css";

const App = ({ apiUrl, logoUrl, shopName }) => (
  <div className="App">
    <div className="logoContainer">
      {logoUrl ? (
        <img className="logo" src={logoUrl} alt={shopName} title={shopName} />
      ) : (
        <h2>{shopName}</h2>
      )}
    </div>
    <ProductGrid apiUrl={apiUrl} />
  </div>
);

export default App;
