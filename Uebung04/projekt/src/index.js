import React from "react";
import ReactDomClient from "react-dom/client";
import App from "./App"
import "./App.css"

const root = ReactDomClient.createRoot(document.getElementById("root"));
root.render(<><App /></>)

