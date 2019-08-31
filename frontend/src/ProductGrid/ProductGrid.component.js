import React from "react";

const Quantity = ({ quantity }) =>
  quantity >= 6 ? (
    <div className="quantity inStock">In Stock</div>
  ) : (
    <div className="quantity">{quantity}</div>
  );

const SoldOut = ({ shopName }) => (
  <div className="soldOut">
    <h3>{shopName} has no products in stock right now.</h3>
    <h5>Please check back later.</h5>
  </div>
);

const ProductGrid = ({ data = [], shopName }) => (
  <div className="productGrid">
    {data.length ? (
      data.map(({ location, productName, quantity, image }, index) => (
        <div className="productCard" key={index}>
          {image && <img className="image" src={image} alt={productName} />}
          <div className="productDetails">
            <h3>{productName}</h3>
            <div>{location}</div>
            <Quantity quantity={quantity} />
          </div>
        </div>
      ))
    ) : (
      <SoldOut shopName={shopName} />
    )}
  </div>
);

export default ProductGrid;
