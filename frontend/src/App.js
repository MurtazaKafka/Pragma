import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Landing from "./Landing";
import About from "./About";


function App() {
  return (
      <div>
      <Router>
          <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/about" element={<About />} />
          </Routes>
      </Router>
      </div>
  );
}

export default App;
