import { useState } from "react";
import { useNavigate } from "react-router-dom";
import BackButton from "./backbutton";
import "../styles/style.css";
import axios from "axios";

function Signup() {

  const navigate = useNavigate();

  const [role, setRole] = useState("employee");
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSignup = async (e) => {

    e.preventDefault();

    if (loading) return;

    if (
      !form.username.trim() ||
      !form.email.trim() ||
      !form.password ||
      !form.confirmPassword
    ) {
      alert("Please fill in all fields.");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(form.email.trim())) {
      alert("Please enter a valid email address.");
      return;
    }

    if (form.password.length < 6) {
      alert("Password must be at least 6 characters.");
      return;
    }

    if (form.password !== form.confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    try {

      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/signup",
        {
          username: form.username.trim(),
          email: form.email.trim().toLowerCase(),
          password: form.password,
          role: role,
        }
      );

      const user = res.data.data[0];

      localStorage.setItem(
        "user",
        JSON.stringify(user)
      );

      alert("Signup Successful");

      setForm({
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
      });

      if (role === "employee") {
        navigate("/skills-form");
      } else {
        navigate("/admin");
      }

    } catch (error) {

      console.log(error.response);

      alert(
        error.response?.data?.detail ||
        "Signup Failed"
      );

    } finally {

      setLoading(false);

    }
  };

  return (

    <div className="container">
        <BackButton />

      <h1>Signup</h1>

      <form onSubmit={handleSignup}>

        <label>Username</label>

        <input
          type="text"
          name="username"
          value={form.username}
          onChange={handleChange}
          placeholder="Enter username"
          disabled={loading}
          required
        />

        <br /><br />

        <label>Email</label>

        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          placeholder="Enter email"
          disabled={loading}
          required
        />

        <br /><br />

        <label>Password</label>

        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          placeholder="Enter password"
          disabled={loading}
          required
        />

        <br /><br />

        <label>Confirm Password</label>

        <input
          type="password"
          name="confirmPassword"
          value={form.confirmPassword}
          onChange={handleChange}
          placeholder="Confirm password"
          disabled={loading}
          required
        />

        <br /><br />

        <label>Choose Role</label>

        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          disabled={loading}
        >
          <option value="employee">Employee</option>
          <option value="admin">Admin</option>
        </select>

        <br /><br />

        <button
          type="submit"
          disabled={loading}
        >
          {loading ? "Signing Up..." : "Signup"}
        </button>

      </form>

    </div>

  );
}

export default Signup;