import React from "react";
import { Helmet } from "react-helmet";
import ProductGrid from "./ProductGrid";
import "./App.css";

const App = ({ apiUrl, logoUrl, shopName }) => (
  <>
    <Helmet>
      <title>{`${shopName} Inventory`}</title>
    </Helmet>
    <div className="App">
      <div className="logoContainer">
        {logoUrl ? (
          <img className="logo" src={logoUrl} alt={shopName} title={shopName} />
        ) : (
          <h2>{shopName}</h2>
        )}
      </div>
      <ProductGrid apiUrl={apiUrl} shopName={shopName} />
    </div>
  </>
);

export default App;
