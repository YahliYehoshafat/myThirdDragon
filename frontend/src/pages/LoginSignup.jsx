import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './LoginSignup.css';

function LoginSignup({ onLoginSuccess }) {
    const [action, setAction] = useState("Login");
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    // Handles form submission for Login or Sign Up
    const handleSubmit = async () => {
        setError("");
        
        // Basic validation
        if (action === "Sign Up") {
            if (!name || !email || !password) {
                setError("All fields are required.");
                return;
            }
            if (!/^\S+@\S+\.\S+$/.test(email)) {
                setError("Invalid email format.");
                return;
            }
        } else { // Login
            if (!email || !password) {
                setError("Email and password are required.");
                return;
            }
        }

        setLoading(true);
        try {
            const endpoint = action === "Sign Up" ? "signup" : "login";
            const response = await fetch(`http://localhost:5000/${endpoint}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: name, email, password })
            });

            let data = {};
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                data = await response.json();
            } else {
                throw new Error("Invalid server response");
            }

            if (data.success) {
                navigate("/Home", { state: { user: data.user } });
                if (onLoginSuccess) {
                    onLoginSuccess(data.user);
                }
                setName("");
                setEmail("");
                setPassword("");
                setError("");
            } else {
                setError(data.message || "Unknown error occurred.");
            }
        } catch (err) {
            console.error("Fetch error:", err);
            setError("Could not reach server. Please try again later.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="header">
                <div className="text">{action}</div>
                <div className="underline"></div>
            </div>

            <div className="inputs">
                {action === "Sign Up" && (
                    <div className="input">
                        <input
                            type="text"
                            placeholder="Name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>
                )}
                <div className="input">
                    <input
                        type="email"
                        placeholder="Email Id"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div className="input">
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                {error && <div className="error">{error}</div>}
            </div>

            <div className="new-account">
                {action === "Login"
                    ? <>You don't have an account yet? <span onClick={() => setAction("Sign Up")}>Create a new account here!</span></>
                    : <>Already have an account? <span onClick={() => setAction("Login")}>Login here!</span></>
                }
            </div>

            <div className="submit-container">
                <button className="submit" onClick={handleSubmit} disabled={loading}>
                    {loading ? "Please wait..." : action}
                </button>
            </div>
        </div>
    );
}

export default LoginSignup;