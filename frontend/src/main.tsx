import { useState } from "react";
import { createRoot } from "react-dom/client";
import { routes } from "./router/routes";
import { DashboardPage } from "./pages/DashboardPage";
import { DevicesPage } from "./pages/DevicesPage";
import { TasksPage } from "./pages/TasksPage";
import { HazardsPage } from "./pages/HazardsPage";
import { ReportsPage } from "./pages/ReportsPage";
import "./styles.css";

function Page({ route }: { route: string }) {
  if (route === "/dashboard") return <DashboardPage />;
  if (route === "/devices") return <DevicesPage />;
  if (route === "/tasks") return <TasksPage />;
  if (route === "/hazards") return <HazardsPage />;
  return <ReportsPage />;
}

function App() {
  const [active, setActive] = useState<string>(routes[0]?.route ?? "/dashboard");
  const current = routes.find((route) => route.route === active) ?? routes[0];
  return (
    <div className="shell">
      <aside>
        <div className="brand">消防设施巡检维保平台</div>
        <nav>
          {routes.map((route) => (
            <button
              key={route.route}
              className={active === route.route ? "active" : ""}
              onClick={() => setActive(route.route)}
            >
              {route.name}
            </button>
          ))}
        </nav>
      </aside>
      <Page route={current?.route ?? "/dashboard"} />
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
