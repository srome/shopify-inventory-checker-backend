import React from "react";
import "./App.css";

const Quantity = ({ quantity }) =>
  quantity >= 6 ? (
    <div className="quantity inStock">In Stock</div>
  ) : (
    <div className="quantity">{quantity}</div>
  );

const App = ({ data }) => (
  <div className="App">
    <div className="logo">Logo Placeholder</div>
    <div className="productGrid">
      {data.map(({ location, productName, quantity }, index) => (
        <div className="productCard" key={index}>
          <h3>{productName}</h3>
          <div>{location}</div>
          <Quantity quantity={quantity} />
        </div>
      ))}
    </div>
  </div>
);

export default App;
