import React from "react";

const Quantity = ({ quantity }) =>
  quantity >= 6 ? (
    <div className="quantity inStock">In Stock</div>
  ) : (
    <div className="quantity">{quantity}</div>
  );

const ProductGrid = ({ data }) => (
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
);

export default ProductGrid;
