// By Drashti

import { useEffect, useState } from "react";
import axios from "axios";
import BackButton from "./backbutton";
import "../styles/style.css";

function TaskAssigned() {

    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        fetchTasks();

    }, []);

    const fetchTasks = async () => {

        try {

            const user = JSON.parse(localStorage.getItem("user"));

            const res = await axios.get(
                `http://127.0.0.1:8000/task-assigned/${user.emp_id}`
            );

            if (Array.isArray(res.data))
                setTasks(res.data);
            else
                setTasks([res.data]);

        } catch (err) {

            console.log(err);

        }

        setLoading(false);

    };

    //--------------------------------------------
    // Update Local State
    //--------------------------------------------

    const updateField = (index, field, value) => {

        const copy = [...tasks];

        copy[index][field] = value;

        setTasks(copy);

    };

    //--------------------------------------------
    // Save
    //--------------------------------------------

    //--------------------------------------------
    // Save
    //--------------------------------------------

    const saveTask = async (task) => {

        console.log("Task Data:", task);

        try {

            await axios.put(

                "http://127.0.0.1:8000/update-task-status",

                {

                    task_id: task.task_id,   // UUID of tasks table
                    status: task.status,
                    deadline: task.deadline

                }

            );

            alert("Task Updated Successfully");

            fetchTasks();

        }

        catch (err) {

            console.log(err);

            alert("Unable to update");

        }

    };

    //--------------------------------------------

    if (loading)

        return (
            <div className="container">
                <BackButton />
                <h2>Loading...</h2>
            </div>
        );

    //--------------------------------------------

    if (
        tasks.length === 0 ||
        tasks[0].assigned === false ||
        tasks[0].message === "No task assigned yet"
    ) {

        return (

            <div className="container">

                <BackButton />

                <h1>No Task Assigned</h1>

            </div>

        );

    }

    //--------------------------------------------

    return (

        <div
            style={{
                width: "96%",
                margin: "30px auto"
            }}
        >

            <BackButton />

            <h1
                style={{
                    color: "white",
                    textAlign: "center",
                    marginBottom: 40,
                    fontSize: 42
                }}
            >

                My Assigned Tasks

            </h1>

            <div

                style={{

                    display: "grid",

                    gridTemplateColumns:
                        "repeat(auto-fill,minmax(340px,1fr))",

                    gap: 30

                }}

            >

                {tasks.map((task, index) => (

                    <div

                        key={index}

                        style={{

                            background: "#fff",

                            borderRadius: 20,

                            padding: 25,

                            boxShadow:
                                "0 8px 25px rgba(0,0,0,.15)"

                        }}

                    >

                        <h2

                            style={{

                                color: "#6a0dad",

                                minHeight: 70

                            }}

                        >

                            {task.task_name}

                        </h2>

                        <hr />

                        <p>

                            <b>Employee</b>

                            <br />

                            {task.employee_name}

                        </p>

                        <br />

                        <p>

                            <b>Similarity</b>

                            {" "}
                            {Number(task.similarity_score).toFixed(2)}%

                        </p>

                        <progress
                            value={task.similarity_score}
                            max="100"
                            style={{
                                width: "100%",
                                height: 12
                            }}
                        />

                        <br />

                        <br />

                        <p>

                            <b>Workload</b>

                            {" "}
                            {Number(task.workload_score).toFixed(2)}%

                        </p>

                        <progress
                            value={task.workload_score}
                            max="100"
                            style={{
                                width: "100%",
                                height: 12
                            }}
                        />

                        <br />
                        <br />

                        <div

                            style={{

                                display: "flex",

                                justifyContent: "center"

                            }}

                        >

                            <div

                                style={{

                                    width: 110,

                                    height: 110,

                                    borderRadius: "50%",

                                    background: "#6a0dad",

                                    color: "white",

                                    display: "flex",

                                    justifyContent: "center",

                                    alignItems: "center",

                                    fontWeight: "bold",

                                    fontSize: 25

                                }}

                            >

                                {Number(task.final_score).toFixed(2)}%

                            </div>

                        </div>

                        <h3
                            style={{
                                textAlign: "center",
                                color: "#555"
                            }}
                        >

                            Overall Match

                        </h3>

                        <hr />

                        <label>Status</label>

                        <select

                            value={task.status}

                            onChange={(e)=>

                                updateField(

                                    index,

                                    "status",

                                    e.target.value

                                )

                            }

                        >

                            <option>

                                In process

                            </option>

                            <option>

                                Extend deadline

                            </option>

                            <option>

                                Completed

                            </option>

                        </select>

                        <label>

                            Deadline

                        </label>

                        <input

                            type="date"

                            value={task.deadline}

                            onChange={(e)=>

                                updateField(

                                    index,

                                    "deadline",

                                    e.target.value

                                )

                            }

                        />

                        <button

                            style={{

                                width: "100%",

                                marginTop: 20

                            }}

                            onClick={() => saveTask(task)}

                        >

                            Save Changes

                        </button>

                    </div>

                ))}

            </div>

        </div>

    );

}

export default TaskAssigned;