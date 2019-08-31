import React from "react";
import "./App.css";

const App = ({ data }) => (
  <div className="App">
    <div className="logo">Logo Placeholder</div>
    <div className="productGrid">
      {data.map(({ location, productName, quantity }, index) => (
        <div className="productCard" key={index}>
          <h3>{productName}</h3>
          <div>{location}</div>
          <div className="quantity">{quantity}</div>
        </div>
      ))}
    </div>
  </div>
);

export default App;
