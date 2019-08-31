import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App.container";
import * as serviceWorker from "./serviceWorker";

const apiUrl = process.env.REACT_APP_API_URL;
ReactDOM.render(<App apiUrl={apiUrl} />, document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
