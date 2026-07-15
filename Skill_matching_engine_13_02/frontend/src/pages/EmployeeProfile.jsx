import { useEffect, useState } from "react";
import BackButton from "./backbutton";
import "../styles/style.css";

function EmployeeProfile() {

    const user = JSON.parse(localStorage.getItem("user"));

    const [profile, setProfile] = useState(null);
    const [isEditing, setIsEditing] = useState(false);

    
    const [programmingSkills, setProgrammingSkills] = useState([]);
    const [frameworkSkills, setFrameworkSkills] = useState([]);
    const [toolSkills, setToolSkills] = useState([]);
    useEffect(() => {
        fetchProfile();
    }, []);

    async function fetchProfile() {

        try {

            const response = await fetch(
                `http://127.0.0.1:8000/employee/profile/${user.emp_id}`
            );

            if (!response.ok) {
                throw new Error("Failed to fetch profile");
            }

            const data = await response.json();

            setProfile(data);

            
            setProgrammingSkills(

                data.programming_languages.map((skill, index) => ({

                    skill: skill,

                    rating: data.programming_ratings[index]  ?? 1

                }))

            );
            setFrameworkSkills(

                data.frameworks.map((skill, index) => ({

                    skill: skill,

                    rating: data.framework_ratings[index]  ?? 1

                }))

            );

            setToolSkills(

                data.tools_and_ide.map((skill, index) => ({

                    skill: skill,

                    rating: data.tools_and_ide_ratings[index]  ?? 1

                }))

            );
        } catch (error) {

            console.error(error);
            alert("Unable to load employee profile.");

        }
    }

    function updateToolSkill(index, value) {

        const updated = [...toolSkills];

        updated[index].skill = value;

        setToolSkills(updated);

    }

    function updateToolRating(index, value) {

        const updated = [...toolSkills];

        updated[index].rating = Number(value);

        setToolSkills(updated);

    }

    function addToolSkill() {

        setToolSkills([

            ...toolSkills,

            {

                skill: "",

                rating: 1

            }

        ]);

    }

    function removeToolSkill(index) {

        setToolSkills(

            toolSkills.filter((_, i) => i !== index)

        );

    }

    function updateFrameworkSkill(index, value) {

            const updated = [...frameworkSkills];

            updated[index].skill = value;

            setFrameworkSkills(updated);

        }

        function updateFrameworkRating(index, value) {

            const updated = [...frameworkSkills];

            updated[index].rating = Number(value);

            setFrameworkSkills(updated);

        }

        function addFrameworkSkill() {

            setFrameworkSkills([

                ...frameworkSkills,

                {

                    skill: "",

                    rating: 1

                }

            ]);

        }

        function removeFrameworkSkill(index) {

            setFrameworkSkills(

                frameworkSkills.filter((_, i) => i !== index)

            );

        }
    function updateProgrammingSkill(index, value) {

                const updated = [...programmingSkills];

                updated[index].skill = value;

                setProgrammingSkills(updated);

            }

            function updateProgrammingRating(index, value) {

                const updated = [...programmingSkills];

                updated[index].rating = Number(value);

                setProgrammingSkills(updated);

            }

            function addProgrammingSkill() {

                setProgrammingSkills([

                    ...programmingSkills,

                    {

                        skill: "",

                        rating: 1

                    }

                ]);

            }

            function removeProgrammingSkill(index) {

                setProgrammingSkills(

                    programmingSkills.filter((_, i) => i !== index)

                );

            }
    

    async function updateProfile() {

                try {

                    const payload = {

                        programming_languages: programmingSkills.map(item => item.skill),

                        programming_ratings: programmingSkills.map(item => Number(item.rating || 1)),

                        frameworks: frameworkSkills.map(item => item.skill),

                        framework_ratings: frameworkSkills.map(item => Number(item.rating || 1)),

                        tools_and_ide: toolSkills.map(item => item.skill),

                        tools_and_ide_ratings: toolSkills.map(item => Number(item.rating || 1))

                    };

                    console.log("Payload being sent:");
                    console.log(payload);

                    const response = await fetch(
                        `http://127.0.0.1:8000/employee/profile/${user.emp_id}`,
                        {
                            method: "PUT",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(payload)
                        }
                    );

                    if (!response.ok) {

                        const error = await response.json();

                        console.log("Backend Error:");
                        console.log(error);

                        alert(JSON.stringify(error, null, 2));

                        return;
                    }

                    alert("Profile Updated Successfully");

                    setIsEditing(false);

                    fetchProfile();

                } catch (error) {

                    console.error(error);

                    alert("Update Failed");

                }

            }

    return (

        <div className="container">

            <BackButton />

            <h1>Employee Profile</h1>

            {profile ? (

                <>

                    <div className="infoBox">
                         <h3>Employee Name : {profile.name}</h3>
                       
                        <h3>Employee ID : {profile.emp_id}</h3>

                    </div>

                    <div className="infoBox">

                        <h3>Programming Languages</h3>

                        {programmingSkills.map((item,index)=>(

                        <div
                        className="profileRow"
                        key={index}

                        style={{

                        display:"flex",

                        gap:"10px",

                        alignItems:"center",

                        marginBottom:"10px"

                        }}

                        >

                        <input

                        style={{flex:3}}

                        value={item.skill}

                        disabled={!isEditing}

                        onChange={(e)=>updateProgrammingSkill(index,e.target.value)}

                        />

                        <select

                        style={{flex:1}}

                        disabled={!isEditing}

                        value={item.rating}

                        onChange={(e)=>updateProgrammingRating(index,e.target.value)}

                        >

                        <option value={1}>1</option>

                        <option value={2}>2</option>

                        <option value={3}>3</option>

                        <option value={4}>4</option>

                        <option value={5}>5</option>

                        </select>

                        {

                        isEditing && (

                        <button

                        onClick={()=>removeProgrammingSkill(index)}

                        >

                        ❌

                        </button>

                        )

                        }

                        </div>

                        ))}

                        {

                        isEditing && (

                        <button

                        onClick={addProgrammingSkill}

                        >

                        + Add Skill

                        </button>

                        )

                        }

                        </div>

                    <div className="infoBox">

                        <h3>Frameworks</h3>

                        {frameworkSkills.map((item,index)=>(

                        <div
                        className="profileRow"
                        key={index}

                        style={{

                        display:"flex",

                        gap:"10px",

                        alignItems:"center",

                        marginBottom:"10px"

                        }}

                        >

                        <input

                        style={{flex:3}}

                        value={item.skill}

                        disabled={!isEditing}

                        onChange={(e)=>updateFrameworkSkill(index,e.target.value)}

                        />

                        <select

                        style={{flex:1}}

                        disabled={!isEditing}

                        value={item.rating}

                        onChange={(e)=>updateFrameworkRating(index,e.target.value)}

                        >

                        <option value={1}>1</option>
                        <option value={2}>2</option>
                        <option value={3}>3</option>
                        <option value={4}>4</option>
                        <option value={5}>5</option>

                        </select>

                        {

                        isEditing && (

                        <button
                        onClick={()=>removeFrameworkSkill(index)}
                        >
                        ❌
                        </button>

                        )

                        }

                        </div>

                        ))}

                        {

                        isEditing && (

                        <button
                        onClick={addFrameworkSkill}
                        >
                        + Add Framework
                        </button>

                        )

                        }

                        </div>

                    <div className="infoBox">

                        <h3>Tools & IDE</h3>

                        {toolSkills.map((item,index)=>(

                        <div
                        className="profileRow"
                        key={index}

                        style={{

                        display:"flex",

                        gap:"10px",

                        alignItems:"center",

                        marginBottom:"10px"

                        }}

                        >

                        <input

                        style={{flex:3}}

                        value={item.skill}

                        disabled={!isEditing}

                        onChange={(e)=>updateToolSkill(index,e.target.value)}

                        />

                        <select

                        style={{flex:1}}

                        disabled={!isEditing}

                        value={item.rating}

                        onChange={(e)=>updateToolRating(index,e.target.value)}

                        >

                        <option value={1}>1</option>
                        <option value={2}>2</option>
                        <option value={3}>3</option>
                        <option value={4}>4</option>
                        <option value={5}>5</option>

                        </select>

                        {

                        isEditing && (

                        <button
                        onClick={()=>removeToolSkill(index)}
                        >
                        ❌
                        </button>

                        )

                        }

                        </div>

                        ))}

                        {

                        isEditing && (

                        <button
                        onClick={addToolSkill}
                        >
                        + Add Tool
                        </button>

                        )

                        }

                        </div>

                    {
                        isEditing ? (

                            <button onClick={updateProfile}>
                                Save Changes
                            </button>

                        ) : (

                            <button
                                onClick={() => setIsEditing(true)}
                            >
                                Edit Profile
                            </button>

                        )
                    }

                </>

            ) : (

                <p>Loading...</p>

            )}

        </div>

    );

}

export default EmployeeProfile;