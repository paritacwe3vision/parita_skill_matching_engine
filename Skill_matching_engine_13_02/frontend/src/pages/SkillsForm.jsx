import { useNavigate } from "react-router-dom";
import BackButton from "./backbutton";
import "../styles/style.css";
import { useState } from "react";
import axios from "axios";

function SkillsForm() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const [experience, setExperience] = useState("");

  // Languages
  const [language, setLanguage] = useState("");
  const [languageRating, setLanguageRating] = useState("");
  const [languages, setLanguages] = useState([]);
  const [showInput, setShowInput] = useState(true);

  // Frameworks
  const [framework, setFramework] = useState("");
  const [frameworkRating, setFrameworkRating] = useState("");
  const [frameworks, setFrameworks] = useState([]);
  const [showFrameworkInput, setShowFrameworkInput] = useState(true);

  // Tools
  const [tool, setTool] = useState("");
  const [toolRating, setToolRating] = useState("");
  const [tools, setTools] = useState([]);
  const [showToolInput, setShowToolInput] = useState(true);

  // ---------------- LANGUAGE ----------------
  const handleLanguage = (e) => {
    if (e.key === "Enter") {
      if (language.trim() === "") return;

      if (!["1", "2", "3", "4", "5"].includes(languageRating)) {
        alert("Rating must be between 1-5");
        return;
      }

      e.preventDefault();

      setLanguages([
        ...languages,
        {
          name: language,
          rating: languageRating,
        },
      ]);

      setLanguage("");
      setLanguageRating("");
      setShowInput(false);
    }
  };

  const removeLanguage = (index) => {
    setLanguages(languages.filter((_, i) => i !== index));
  };

  const addLanguageField = () => {
    setShowInput(true);
  };

  // ---------------- FRAMEWORK ----------------
  const handleFramework = (e) => {
    if (e.key === "Enter") {
      if (framework.trim() === "") return;

      if (!["1", "2", "3", "4", "5"].includes(frameworkRating)) {
        alert("Rating must be between 1-5");
        return;
      }

      e.preventDefault();

      setFrameworks([
        ...frameworks,
        {
          name: framework,
          rating: frameworkRating,
        },
      ]);

      setFramework("");
      setFrameworkRating("");
      setShowFrameworkInput(false);
    }
  };

  const removeFramework = (index) => {
    setFrameworks(frameworks.filter((_, i) => i !== index));
  };

  const addFrameworkField = () => {
    setShowFrameworkInput(true);
  };

  // ---------------- TOOLS ----------------
  const handleTool = (e) => {
    if (e.key === "Enter") {
      if (tool.trim() === "") return;

      if (!["1", "2", "3", "4", "5"].includes(toolRating)) {
        alert("Rating must be between 1-5");
        return;
      }

      e.preventDefault();

      setTools([
        ...tools,
        {
          name: tool,
          rating: toolRating,
        },
      ]);

      setTool("");
      setToolRating("");
      setShowToolInput(false);
    }
  };

  const removeTool = (index) => {
    setTools(tools.filter((_, i) => i !== index));
  };

  const addToolField = () => {
    setShowToolInput(true);
  };

  // ---------------- CONFIRM ----------------
  const handleConfirm = async () => {
    if (
      !name ||
      !email ||
      !role ||
      !experience ||
      languages.length === 0 ||
      frameworks.length === 0 ||
      tools.length === 0
    ) {
      alert("Please fill all fields");
      return;
    }

    try {
      const user = JSON.parse(localStorage.getItem("user"));

      const payload = {
        user_id: user.id,
        emp_id: Number(user.emp_id),

        name,
        email,
        role,
        experience_years: Number(experience),

        programming_languages: languages.map(i => i.name),
        programming_ratings: languages.map(i => Number(i.rating)),

        frameworks: frameworks.map(i => i.name),
        framework_ratings: frameworks.map(i => Number(i.rating)),

        tools_and_ide: tools.map(i => i.name),
        tools_and_ide_ratings: tools.map(i => Number(i.rating))
      };

      console.log("PAYLOAD SENT TO BACKEND:", payload);

      const response = await axios.post(
        "http://127.0.0.1:8000/employee",
        payload
      );

      alert(response.data.message);
      navigate("/employee");

    } catch (error) {
      console.log(error);
      alert(error.response?.data?.detail || error.message);
    }
  };

  return (
    <div className="container">
        <BackButton />
      <h1>Employee Details</h1>

      <input
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <br /><br />

      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <br /><br />

      <input
        placeholder="Current Role"
        value={role}
        onChange={(e) => setRole(e.target.value)}
        required
      />
      <br /><br />

      <input
        placeholder="Experience"
        value={experience}
        onChange={(e) => setExperience(e.target.value)}
        required
      />
      <br /><br />

      {/* ---------------- LANGUAGES ---------------- */}
      <h2>Programming Languages</h2>

      {showInput && (
        <div className="inputRow">
          <div>
            <label>Language</label>
            <input
              placeholder="Enter language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              onKeyDown={handleLanguage}
              required
            />
          </div>

          <div>
            <label>Rating out of 5</label>
            <input
              placeholder="1-5"
              value={languageRating}
              onChange={(e) => setLanguageRating(e.target.value)}
              onKeyDown={handleLanguage}
              required
            />
          </div>
        </div>
      )}

      <div>
        {languages.map((lang, index) => (
          <div className="tag" key={index}>
            <span>{lang.name}</span>
            <span className="ratingBox">{lang.rating}/5</span>
            <button onClick={() => removeLanguage(index)}>✖</button>
          </div>
        ))}

        <button className="addButton" onClick={addLanguageField}>
          +
        </button>
      </div>

      {/* ---------------- FRAMEWORKS ---------------- */}
      <h2>Frameworks</h2>

      {showFrameworkInput && (
        <div className="inputRow">
          <div>
            <label>Framework</label>
            <input
              placeholder="Enter framework"
              value={framework}
              onChange={(e) => setFramework(e.target.value)}
              onKeyDown={handleFramework}
              required
            />
          </div>

          <div>
            <label>Rating out of 5</label>
            <input
              placeholder="1-5"
              value={frameworkRating}
              onChange={(e) => setFrameworkRating(e.target.value)}
              onKeyDown={handleFramework}
              required
            />
          </div>
        </div>
      )}

      <div>
        {frameworks.map((item, index) => (
          <div className="tag" key={index}>
            <span>{item.name}</span>
            <span className="ratingBox">{item.rating}/5</span>
            <button onClick={() => removeFramework(index)}>✖</button>
          </div>
        ))}

        <button className="addButton" onClick={addFrameworkField}>
          +
        </button>
      </div>

      {/* ---------------- TOOLS ---------------- */}
      <h2>Tools & IDE</h2>

      {showToolInput && (
        <div className="inputRow">
          <div>
            <label>Tools & IDE</label>
            <input
              placeholder="Enter tool"
              value={tool}
              onChange={(e) => setTool(e.target.value)}
              onKeyDown={handleTool}
              required
            />
          </div>

          <div>
            <label>Rating out of 5</label>
            <input
              placeholder="1-5"
              value={toolRating}
              onChange={(e) => setToolRating(e.target.value)}
              onKeyDown={handleTool}
              required
            />
          </div>
        </div>
      )}

      <div>
        {tools.map((item, index) => (
          <div className="tag" key={index}>
            <span>{item.name}</span>
            <span className="ratingBox">{item.rating}/5</span>
            <button onClick={() => removeTool(index)}>✖</button>
          </div>
        ))}

        <button className="addButton" onClick={addToolField}>
          +
        </button>
      </div>

      <br /><br />

      <button onClick={handleConfirm}>
        Confirm
      </button>
    </div>
  );
}

export default SkillsForm;