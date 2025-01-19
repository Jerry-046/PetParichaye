import React, { useState } from 'react';
import axios from 'axios';

// CSS styles for basic form layout (you can move this to an external CSS file)
const styles = {
  form: {
    display: 'flex',
    flexDirection: 'column',
    width: '300px',
    margin: '0 auto',
  },
  input: {
    padding: '10px',
    margin: '10px 0',
    border: '1px solid #ccc',
  },
  button: {
    padding: '10px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
  },
  buttonHover: {
    backgroundColor: '#45a049',
  },
  message: {
    textAlign: 'center',
  },
  successMessage: {
    color: 'green',
  },
  errorMessage: {
    color: 'red',
  },
};

const RegisterComponent = () => {
  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    confirm_password: '',
    address: '',          // Added address field
    bio: '',              // Added bio field
    profile_picture: null, // Added profile_picture field
  });
  const [message, setMessage] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleFileChange = (e) => {
    const { name, files } = e.target;
    setFormData({
      ...formData,
      [name]: files[0],  // Handle file input for profile_picture
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Frontend password matching validation
    if (formData.password !== formData.confirm_password) {
      setMessage('Passwords do not match');
      return;
    }

    // Create a FormData object to handle file uploads
    const formDataToSend = new FormData();
    for (const key in formData) {
      formDataToSend.append(key, formData[key]);
    }

    try {
      const response = await axios.post('http://localhost:8000/api/auth/register/', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data', // Set proper content type for file upload
        },
      });

      // Assuming the backend returns a success message or token in response.data
      setMessage(response.data.message || 'User registered successfully');
      console.log('User registered:', response.data); // You can log or handle this data as needed
    } catch (error) {
      // Check if the error is from the server response and display it
      if (error.response && error.response.data) {
        setMessage(`Error: ${error.response.data.detail || 'Error registering user'}`);
      } else {
        setMessage('Network error. Please try again later.');
      }
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
          required
          style={styles.input}
        />
        <input
          type="text"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
          placeholder="First Name"
          required
          style={styles.input}
        />
        <input
          type="text"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
          placeholder="Last Name"
          required
          style={styles.input}
        />
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Password"
          required
          style={styles.input}
        />
        <input
          type="password"
          name="confirm_password"
          value={formData.confirm_password}
          onChange={handleChange}
          placeholder="Confirm Password"
          required
          style={styles.input}
        />
        <input
          type="text"
          name="address"
          value={formData.address}
          onChange={handleChange}
          placeholder="Address"
          style={styles.input}
        />
        <textarea
          name="bio"
          value={formData.bio}
          onChange={handleChange}
          placeholder="Bio"
          style={{ ...styles.input, height: '100px' }} // Adjusting height for bio input
        />
        <input
          type="file"
          name="profile_picture"
          onChange={handleFileChange}
          style={styles.input}
        />
        <button type="submit" style={styles.button}>Register</button>
      </form>

      {message && (
        <p style={{ ...styles.message, ...(message.includes('Error') ? styles.errorMessage : styles.successMessage) }}>
          {message}
        </p>
      )}
    </div>
  );
};

export default RegisterComponent;
