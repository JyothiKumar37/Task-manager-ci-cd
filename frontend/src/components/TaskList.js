import React, { useState, useEffect } from "react";
import axios from "axios";

// backend API endpoint (dynamically resolves hostname if REACT_APP_API_URL is not set or default)
const getApiUrl = () => {
  const envUrl = process.env.REACT_APP_API_URL;
  if (envUrl && envUrl.startsWith("http")) {
    return envUrl;
  }
  const hostname = typeof window !== "undefined" && window.location.hostname ? window.location.hostname : "localhost";
  return `http://${hostname}:5000/tasks`;
};

const API_URL = getApiUrl();

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  // Fetch all tasks
  const fetchTasks = async () => {
    const response = await axios.get(API_URL);
    setTasks(response.data);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  // Add new task
  const addTask = async () => {
    if (newTask.trim() === "") return;
    await axios.post(API_URL, { title: newTask, status: "Pending" });
    setNewTask("");
    fetchTasks();
  };

  // Delete task
  const deleteTask = async (id) => {
    await axios.delete(`${API_URL}/${id}`);
    fetchTasks();
  };

  return (
    <div className="task-container">
      <div className="add-task">
        <input
          type="text"
          placeholder="Enter new task..."
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
        />
        <button onClick={addTask}>Add Task</button>
      </div>

      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id}>
            {task.title} - {task.status}
            <button className="delete-btn" onClick={() => deleteTask(task.id)}>
              ❌
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TaskList;

