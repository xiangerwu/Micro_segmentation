import './App.css';
import HostsTable from './HostsTable';
import IntentChart from './DashboardComponent/IntentChart';
import Navigation from './Navigation';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Navigation />
      <Routes>
        <Route path="/" element={<HostsTable />} />
        <Route path="/dashboard" element={<IntentChart />} />

      </Routes>
    
      
    </Router>
  );
}

export default App;
