import { useEffect, useState } from "react";
import BackButton from "./backbutton";
import "../styles/style.css";
import axios from "axios";

function EmployeeDetailsPage() {

    const [employees, setEmployees] = useState([]);

    useEffect(() => {

        axios
            .get("http://127.0.0.1:8000/employees")
            .then((res) => {
                setEmployees(res.data);
            })
            .catch((err) => {
                console.log(err);
            });

    }, []);

    return (

        <div className="employeeContainer">
               <BackButton />

            <h1>Employee Details</h1>

            <div className="tableContainer">

                <table border="1" cellPadding="10">

                    <thead>

                        <tr>

                            <th>Emp ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Experience</th>

                        </tr>

                    </thead>

                    <tbody>

                        {employees.map((emp) => (

                            <tr key={emp.emp_id}>

                                <td>{emp.emp_id}</td>
                                <td>{emp.name}</td>
                                <td>{emp.email}</td>
                                <td>{emp.role}</td>
                                <td>{emp.experience_years} Years</td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>

    );

}

export default EmployeeDetailsPage;