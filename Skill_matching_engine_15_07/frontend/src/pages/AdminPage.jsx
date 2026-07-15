import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import BackButton from "./backbutton";
import "../styles/style.css";
import axios from "axios";

function AdminPage() {

    const navigate = useNavigate();

    const [admin, setAdmin] = useState({
        username: "",
        role: ""
    });

    useEffect(() => {

        const user = JSON.parse(localStorage.getItem("user"));

        if (!user) return;

        axios
            .get(`http://127.0.0.1:8000/user/${user.id}`)
            .then((res) => {

                setAdmin(res.data);

            })
            .catch((err) => {

                console.log(err);

            });

    }, []);

    return (

        <div className="container">
              <BackButton />

            <h1>Admin</h1>

            <div>

                <h3>Name : {admin.username}</h3>

                <h3>Role : {admin.role}</h3>

            </div>

            <div className="buttonRow">

                <button
                    onClick={() => navigate("/task-form")}
                >
                    Task Form
                </button>

                <button
                    onClick={() => navigate("/assign-task")}
                >
                    Assign Task
                </button>

                <button
                    onClick={() => navigate("/employee-details")}
                >
                    Employee Details
                </button>

            </div>

        </div>

    );

}

export default AdminPage;