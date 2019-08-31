import React from "react";
import "./App.css";

const Quantity = ({ quantity }) =>
  quantity >= 6 ? (
    <div className="quantity inStock">In Stock</div>
  ) : (
    <div className="quantity">{quantity}</div>
  );

const App = ({ data, logoUrl, shopName }) => (
  <div className="App">
    <div className="logoContainer">
      {logoUrl ? (
        <img className="logo" src={logoUrl} alt={shopName} title={shopName} />
      ) : (
        <h2>{shopName}</h2>
      )}
    </div>
    <div className="productGrid">
      {data.map(({ location, productName, quantity, image }, index) => (
        <div className="productCard" key={index}>
          {image && <img className="image" src={image} alt={productName} />}
          <div className="productDetails">
            <h3>{productName}</h3>
            <div>{location}</div>
            <Quantity quantity={quantity} />
          </div>
        </div>
      ))}
    </div>
  </div>
);

export default App;
