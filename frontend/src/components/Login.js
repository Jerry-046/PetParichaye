import React from 'react';
import api from '../axios';

const Logout = () => {
    const handleLogout = async () => {
        try {
            const refreshToken = localStorage.getItem('refresh_token');
            await api.post('accounts/logout/', { refresh: refreshToken });
            localStorage.removeItem('token');
            localStorage.removeItem('refresh_token');
            alert('Logged out successfully.');
        } catch (error) {
            alert('Logout failed. Please try again.');
        }
    };

    return (
        <div>
            <h2>Logout</h2>
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default Logout;
