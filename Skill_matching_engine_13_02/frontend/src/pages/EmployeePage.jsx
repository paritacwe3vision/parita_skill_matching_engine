import { useNavigate } from "react-router-dom";
import BackButton from "./backbutton";
import "../styles/style.css";

function EmployeePage() {

  const navigate = useNavigate();

  const user = JSON.parse(
    localStorage.getItem("user")
  );

  return (

    <div className="container">
         <BackButton />

      <h1>Employee</h1>

      <div>

        <h3>
          Employee Name : {user?.username}
        </h3>

        <h3>
          Role : {user?.role}
        </h3>

      </div>

      <div>

        <div className="buttonRow">

        <button
              onClick={() => navigate("/skills-form")}
              disabled={user?.skills_completed}
          >
              {user?.skills_completed
                  ? "Skills Already Submitted"
                  : "Skills Form"}
          </button>
          <button
            onClick={() => navigate("/task-assigned")}
          >
            Task Assign
          </button>

            <button
            onClick={() => navigate("/employee-profile")}
         >
              Add Employee Profile
            </button>

        </div>

      </div>

    </div>

  );

}

export default EmployeePage;