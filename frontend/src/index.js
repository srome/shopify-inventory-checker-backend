import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import * as serviceWorker from "./serviceWorker";

const apiUrl = process.env.REACT_APP_API_URL;
const logoUrl = process.env.REACT_APP_LOGO_URL;
const shopName = process.env.REACT_APP_SHOP_NAME;
ReactDOM.render(
  <App apiUrl={apiUrl} logoUrl={logoUrl} shopName={shopName} />,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
