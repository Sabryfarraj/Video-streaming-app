import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSignup, setIsSignup] = useState(false);
    const [validationErrors, setValidationErrors] = useState({
        username: '',
        password: ''
    });

    const validateForm = () => {
        const errors = {
            username: '',
            password: ''
        };

        // Username validation
        if (username.length < 3) {
            errors.username = 'Username must be at least 3 characters long';
        } else if (username.length > 20) {
            errors.username = 'Username must be less than 20 characters';
        } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            errors.username = 'Username can only contain letters, numbers, and underscores';
        }

        // Password validation
        if (password.length < 8) {
            errors.password = 'Password must be at least 8 characters long';
        } else if (!/[A-Z]/.test(password)) {
            errors.password = 'Password must contain at least one uppercase letter';
        } else if (!/[a-z]/.test(password)) {
            errors.password = 'Password must contain at least one lowercase letter';
        } else if (!/[0-9]/.test(password)) {
            errors.password = 'Password must contain at least one number';
        }

        setValidationErrors(errors);
        return !errors.username && !errors.password;
    };

    const handleAuth = async (e) => {
        e.preventDefault();
        setError('');

        if (isSignup && !validateForm()) {
            return;
        }

        const endpoint = isSignup ? '/signup' : '/login';

        try {
            // Prepare request body
            let requestBody;
            let requestHeaders;

            if (isSignup) {
                // For signup, send JSON
                requestBody = JSON.stringify({ username, password });
                requestHeaders = {
                    'Content-Type': 'application/json',
                };
            } else {
                // For login, send form data
                const formData = new URLSearchParams();
                formData.append('username', username);
                formData.append('password', password);
                requestBody = formData.toString();
                requestHeaders = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                };
            }

            console.log('Sending request to:', endpoint);
            const response = await fetch(`http://localhost:8000${endpoint}`, {
                method: 'POST',
                headers: requestHeaders,
                body: requestBody
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Authentication failed');
            }

            const data = await response.json();
            console.log('Response data:', data);

            if (data.access_token) {
                localStorage.setItem('token', data.access_token);
                setIsLoggedIn(true);
            }
        } catch (error) {
            console.error('Auth error:', error);
            setError(error.message);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setIsLoggedIn(false);
    };

    const VideoList = () => {
        const [videos, setVideos] = useState([]);
        const [selectedVideo, setSelectedVideo] = useState(null);
        const [loading, setLoading] = useState(true);
        const [error, setError] = useState(null);

        useEffect(() => {
            fetch('http://localhost:8001/videos')
                .then(res => res.json())
                .then(data => {
                    console.log('Received videos:', data);
                    setVideos(data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error('Error fetching videos:', err);
                    setError(err.message);
                    setLoading(false);
                });
        }, []);

        if (loading) return <div className="loading">Loading videos...</div>;
        if (error) return <div className="error-message">Error: {error}</div>;

        return (
            <div className="video-container">
                {selectedVideo ? (
                    <div className="video-player">
                        <button
                            className="back-button"
                            onClick={() => setSelectedVideo(null)}
                        >
                            Back to List
                        </button>
                        <h2>{videos.find(v => v.id === selectedVideo).title}</h2>
                        <video
                            key={selectedVideo}
                            controls
                            width="100%"
                            className="main-video"
                            onError={(e) => console.error('Video error:', e)}
                        >
                            <source
                                src={`http://localhost:8002/stream/${videos.find(v => v.id === selectedVideo).location}`}
                                type="video/mp4"
                            />
                            Your browser does not support the video tag.
                        </video>
                    </div>
                ) : (
                    <div className="video-grid">
                        {videos.map(video => (
                            <div key={video.id} className="video-card">
                                <div className="video-thumbnail" onClick={() => setSelectedVideo(video.id)}>
                                    <div className="thumbnail-placeholder">
                                        <span className="play-icon">▶</span>
                                    </div>
                                </div>
                                <h3>{video.title}</h3>
                                <button onClick={() => setSelectedVideo(video.id)}>
                                    Play Video
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="App">
            {!isLoggedIn ? (
                <div className="auth-container">
                    <h1>Video Streaming App</h1>
                    <form onSubmit={handleAuth} className="auth-form">
                        <h2>{isSignup ? 'Sign Up' : 'Login'}</h2>
                        {error && <div className="error-message">{error}</div>}
                        <div className="form-group">
                            <input
                                type="text"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                            {validationErrors.username && (
                                <div className="validation-error">{validationErrors.username}</div>
                            )}
                        </div>
                        <div className="form-group">
                            <input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                            {validationErrors.password && (
                                <div className="validation-error">{validationErrors.password}</div>
                            )}
                        </div>
                        <button type="submit" className="auth-button">
                            {isSignup ? 'Sign Up' : 'Login'}
                        </button>
                        <button
                            type="button"
                            className="switch-auth"
                            onClick={() => {
                                setIsSignup(!isSignup);
                                setValidationErrors({ username: '', password: '' });
                                setError('');
                            }}
                        >
                            {isSignup ? 'Already have an account? Login' : 'Need an account? Sign Up'}
                        </button>
                    </form>
                </div>
            ) : (
                <>
                    <nav className="navbar">
                        <h1>Video Streaming App</h1>
                        <button onClick={handleLogout} className="logout-button">
                            Logout
                        </button>
                    </nav>
                    <VideoList />
                </>
            )}
        </div>
    );
}

export default App;