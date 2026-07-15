import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import EmployeePage from "./pages/EmployeePage";
import AdminPage from "./pages/AdminPage";
import SkillsForm from "./pages/SkillsForm";
import TaskForm from "./pages/TaskForm";
import TaskAssigned from "./pages/TaskAssigned"; // Drashti - 02-07-2026
import AssignTaskPage from "./pages/AssignTaskPage"; // New
import EmployeeDetailsPage from "./pages/EmployeeDetailsPage"; // New
import EmployeeProfile from "./pages/EmployeeProfile";
function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Login Page */}
        <Route
          path="/"
          element={<Login />}
        />

        {/* Signup Page */}
        <Route
          path="/signup"
          element={<Signup />}
        />

        {/* Employee Dashboard */}
        <Route
          path="/employee"
          element={<EmployeePage />}
        />

        {/* Admin Dashboard */}
        <Route
          path="/admin"
          element={<AdminPage />}
        />

        {/* Employee Skills Form */}
        <Route
          path="/skills-form"
          element={<SkillsForm />}
        />

        {/* Task Form */}
        <Route
          path="/task-form"
          element={<TaskForm />}
        />

        {/* Drashti - Task Assigned Page */}
        <Route
          path="/task-assigned"
          element={<TaskAssigned />}
        />

        {/* mili Admin - Assign Task Page */}
        <Route
          path="/assign-task"
          element={<AssignTaskPage />}
        />

        {/* mili Admin - Employee Details Page */}
        <Route
          path="/employee-details"
          element={<EmployeeDetailsPage />}
        />
        <Route
        path="/employee-profile"
         element={<EmployeeProfile />}
       />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
