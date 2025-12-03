import './App.css';
import { AppHeader } from './components/AppHeader.jsx';
import { AppFooter } from './components/AppFooter.jsx';
import { StatsPanel } from './components/StatsPanel.jsx';
import { HydroSummary } from './components/HydroSummary.jsx';
import { CountryTable } from './components/CountryTable.jsx';
import { ResourceTimeseries } from './components/ResourceTimeseries.jsx';
import { ClimateTimeline } from './components/ClimateTimeline.jsx';
import { SnapshotTrigger } from './components/SnapshotTrigger.jsx';

function App() {
  return (
    <div className="app-shell">
      <AppHeader />
      <main>
        <section>
          <h2>Vue d’ensemble</h2>
          <StatsPanel />
        </section>

        <section className="grid-two">
          <div>
            <h2>Hydro sites</h2>
            <HydroSummary />
          </div>
          <div>
            <h2>Snapshot asynchrone</h2>
            <SnapshotTrigger />
          </div>
        </section>

        <section>
          <h2>Countries (pagination API)</h2>
          <CountryTable />
        </section>

        <section className="grid-two">
          <ResourceTimeseries />
          <ClimateTimeline />
        </section>
      </main>
      <AppFooter />
    </div>
  );
}

export default App;
