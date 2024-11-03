import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Landing from "./Landing";
import About from "./About";
import Login from "./components/Login/Login";
import Register from "./components/Login/Register";


function App() {
  return (
      <div>
      <Router>
          <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/" element={<Landing />} />
              <Route path="/about" element={<About />} />
          </Routes>
      </Router>
      </div>
  );
}

export default App;
