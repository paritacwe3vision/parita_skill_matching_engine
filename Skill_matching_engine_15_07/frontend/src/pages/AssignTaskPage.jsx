import { useEffect, useState } from "react";
import BackButton from "./backbutton";
import "../styles/style.css";
import axios from "axios";

function AssignTaskPage() {

    const [tasks, setTasks] = useState([]);

    useEffect(() => {

        axios
            .get("http://127.0.0.1:8000/admin-task-assignments")
            .then((res) => {
                setTasks(res.data);
            })
            .catch((err) => {
                console.log(err);
            });

    }, []);

    return (

        <div className="container">
              <BackButton />

            <h1>Assigned Tasks</h1>

            <table border="1" cellPadding="10">

                <thead>

                    <tr>

                        <th>Employee Name</th>
                        <th>Task Name</th>
                        <th>Deadline</th>

                    </tr>

                </thead>

                <tbody>

                    {tasks.map((item, index) => (

                        <tr key={index}>

                            <td>{item.employee}</td>
                            <td>{item.task}</td>
                            <td>{item.deadline}</td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>

    );

}

export default AssignTaskPage;