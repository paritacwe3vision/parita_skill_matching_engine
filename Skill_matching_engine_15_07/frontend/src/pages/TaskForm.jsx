import { useNavigate } from "react-router-dom";
import BackButton from "./backbutton";
import "../styles/style.css";;
import { useState } from "react";

function TaskForm() {
  const navigate = useNavigate();

  const [taskName, setTaskName] = useState("");
  const [description, setDescription] = useState("");

  const [technology, setTechnology] = useState("");
  const [technologies, setTechnologies] = useState([]);
  const [showTechInput, setShowTechInput] = useState(true);

  const [tool, setTool] = useState("");
  const [tools, setTools] = useState([]);
  const [showToolInput, setShowToolInput] = useState(true);

  const [deadline, setDeadline] = useState("");
  const [startingDate, setStartingDate] = useState("");

  // NEW
  const [complexity, setComplexity] = useState("");
  const [priority, setPriority] = useState("");

  // ===========================
  // Add Technology
  // ===========================
  const handleTechnology = (e) => {
    if (e.key === "Enter" && technology.trim() !== "") {
      e.preventDefault();

      setTechnologies([...technologies, technology.trim()]);
      setTechnology("");
      setShowTechInput(false);
    }
  };

  // ===========================
  // Add Tool
  // ===========================
  const handleTool = (e) => {
    if (e.key === "Enter" && tool.trim() !== "") {
      e.preventDefault();

      setTools([...tools, tool.trim()]);
      setTool("");
      setShowToolInput(false);
    }
  };

  // ===========================
  // Remove Technology
  // ===========================
  const removeTechnology = (index) => {
    setTechnologies(technologies.filter((_, i) => i !== index));
  };

  // ===========================
  // Remove Tool
  // ===========================
  const removeTool = (index) => {
    setTools(tools.filter((_, i) => i !== index));
  };

  // ===========================
  // Submit Task
  // ===========================
  const handleConfirm = async () => {
    if (
      !taskName ||
      !description ||
      technologies.length === 0 ||
      tools.length === 0 ||
      !complexity ||
      !priority ||
      !startingDate ||
      !deadline
    ) {
      alert("Please fill all required fields.");
      return;
    }

    const taskData = {
      task_name: taskName,
      description: description,
      technologies: technologies,
      tools_and_ide: tools,
      complexity: complexity,
      priority: priority,
      starting_date: startingDate,
      deadline: deadline,
    };

    console.log("Sending Task:", taskData);

    try {
      const response = await fetch("http://127.0.0.1:8000/task", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(taskData),
      });

      const result = await response.json();

      console.log(result);

      if (!response.ok) {
        alert(result.detail || "Task creation failed.");
        return;
      }

      alert("Task created successfully!");

      // Clear form
      setTaskName("");
      setDescription("");
      setTechnology("");
      setTechnologies([]);
      setShowTechInput(true);
      setTool("");
      setTools([]);
      setShowToolInput(true);
      setComplexity("");
      setPriority("");
      setStartingDate("");
      setDeadline("");

      navigate("/admin");

    } catch (error) {
      console.error("Error:", error);
      alert("Unable to connect to backend.");
    }
  };

  return (
    <div className="container">
         <BackButton />
      <h1>Task Requirements</h1>

      <label>Task Name</label>
      <input
        type="text"
        value={taskName}
        onChange={(e) => setTaskName(e.target.value)}
        required
      />

      <br />
      <br />

      <label>Description</label>
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />

      <br />
      <br />

      <label>Technologies</label>

      <br />
      <br />

      {showTechInput && (
        <input
          type="text"
          placeholder="Enter technology"
          value={technology}
          onChange={(e) => setTechnology(e.target.value)}
          onKeyDown={handleTechnology}
          required
        />
      )}

      <div>
        {technologies.map((tech, index) => (
          <span
            key={index}
            style={{
              margin: "5px",
              padding: "8px",
              border: "1px solid black",
              display: "inline-block",
            }}
          >
            {tech}
            <button onClick={() => removeTechnology(index)}>✖</button>
          </span>
        ))}

        <button
          type="button"
          onClick={() => setShowTechInput(true)}
        >
          +
        </button>
      </div>

      <br />
      <br />

      <label>Tools</label>

      <br />
      <br />

      {showToolInput && (
        <input
          type="text"
          placeholder="Enter tool"
          value={tool}
          onChange={(e) => setTool(e.target.value)}
          onKeyDown={handleTool}
          required
        />
      )}

      <div>
        {tools.map((item, index) => (
          <span
            key={index}
            style={{
              margin: "5px",
              padding: "8px",
              border: "1px solid black",
              display: "inline-block",
            }}
          >
            {item}
            <button onClick={() => removeTool(index)}>✖</button>
          </span>
        ))}

        <button
          type="button"
          onClick={() => setShowToolInput(true)}
        >
          +
        </button>
      </div>

      <br />
      <br />

      <label>Complexity</label>

      <select
        value={complexity}
        onChange={(e) => setComplexity(e.target.value)}
        required
      >
        <option value="">Select Complexity</option>
        <option value="Very Easy">Very Easy</option>
        <option value="Easy">Easy</option>
        <option value="Medium">Medium</option>
        <option value="Hard">Hard</option>
        <option value="Expert">Expert</option>
      </select>

      <br />
      <br />

      <label>Priority</label>

      <select
        value={priority}
        onChange={(e) => setPriority(e.target.value)}
        required
      >
        <option value="">Select Priority</option>
        <option value="Critical">Critical</option>
        <option value="High">High</option>
        <option value="Medium">Medium</option>
        <option value="Low">Low</option>
        <option value="Very Low">Very Low</option>
      </select>

      <br />
      <br />

      <label>Starting Date</label>

      <input
        type="date"
        value={startingDate}
        onChange={(e) => setStartingDate(e.target.value)}
        required
      />

      <br />
      <br />

      <label>Deadline</label>

      <input
        type="date"
        value={deadline}
        onChange={(e) => setDeadline(e.target.value)}
        required
      />

      <br />
      <br />

      <button onClick={handleConfirm}>
        Confirm
      </button>
    </div>
  );
}

export default TaskForm;