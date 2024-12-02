document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const tasksList = document.getElementById('tasks-list');
    // delete button 
    const deleteAllButton = document.getElementById('delete-all-tasks');
    console.log(deleteAllButton, "delete button");
    // Helper function to get access token
    function getAccessToken() {
        return localStorage.getItem('access_token');
    }
    function getCSRFToken() {
        const csrfToken = document.cookie.match(/csrftoken=([^;]+)/);
        return csrfToken ? csrfToken[1] : null;
    }
    // delete all tasks

    if (deleteAllButton) {
        deleteAllButton.addEventListener('click', (e) => {
            console.log('Delete All Button Clicked!'); // Verify click event
            e.preventDefault(); // Prevent any default form submission
            deleteAllTasks();
        });
    } else {
        console.error('Delete All Button not found in the DOM');
    }

    async function deleteAllTasks() {
        console.log('Delete All Tasks Function Called'); // Additional logging
        try {
            const confirmDelete = confirm('Are you sure you want to delete all tasks? This action cannot be undone.');
            
            if (!confirmDelete) return;

            const response = await axios.delete('/api/tasks/delete-all/', {
                headers: { 
                    'Authorization': `Bearer ${getAccessToken()}`,
                    'Content-Type': 'application/json'
                }
            });

            console.log('Delete All Response:', response);
            alert(response.data.message);
            fetchTasks();
        } catch (error) {
            console.error('Full Delete All Error:', error);
            
            if (error.response) {
                console.error('Error Response:', error.response.data);
                console.error('Error Status:', error.response.status);
                alert(`Failed to delete tasks: ${error.response.data.detail || 'Unknown error'}`);
            } else {
                console.error('Error:', error.message);
                alert('Error deleting tasks: ' + error.message);
            }
        }
    }



    // fetchTasks
    async function fetchTasks() {
        try {
            const response = await axios.get('/api/tasks/', {
                headers: { 'Authorization': `Bearer ${getAccessToken()}` }
            });
            displayTasks(response.data);
        } catch (error) {
            console.error('Error fetching tasks', error);
        }
    }

    // displayTasks
    function displayTasks(tasks) {
        tasksList.innerHTML = tasks.map(task => `
            <div class="card mb-2">
                <div class="card-body">
                    <h5 class="card-title">${task.title}</h5>
                    <p class="card-text">${task.description || 'No description'}</p>
                    <p>Priority: ${task.priority}</p>
                    <button class="btn btn-danger delete-task" data-id="${task.id}">Delete</button>
                </div>
            </div>
        `).join('');

        // Add event listeners to delete buttons
        document.querySelectorAll('.delete-task').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const taskId = e.target.dataset.id;
                console.log(taskId);
                try {
                    const response = await axios.delete(`/api/tasks/${taskId}/`, {
                        headers: { 'Authorization': `Bearer ${getAccessToken()}`,'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken() }
                    });
                    console.log('Delete response:', response);
                    fetchTasks();
                } catch (error) {
                    console.error('Error deleting task', error);
                }
            });
        });
    }

    // createTask
    if (taskForm) {
        taskForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const description = document.getElementById('description').value;
            const priority = document.getElementById('priority').value;

            try {
                await axios.post('/api/tasks/', 
                    { title, description, priority }, 
                    { headers: { 'Authorization': `Bearer ${getAccessToken()}` } }
                );
                taskForm.reset();
                fetchTasks();
            } catch (error) {
                console.error('Error creating task', error);
            }
        });
    }

    // Logout
    document.getElementById('logout-btn').addEventListener('click', async (e) => {
        e.preventDefault();
        const accessToken = localStorage.getItem('access_token');
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            alert('No refresh token found.');
            return;
        }
        const csrfToken = getCSRFToken();
        if (!csrfToken) {
            alert('CSRF token is missing.');
            return;
        }
        try {
            
            // const response = await axios.post('/api/logout/', {
            //     refresh_token: refreshToken
            // });
            const response = await axios.post('/api/logout/', 
            {
                refresh_token: refreshToken
            }, 
            {
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'X-CSRFToken': csrfToken
                }
            })
            alert(response.data.message);
            localStorage.removeItem('refresh_token'); 
            localStorage.removeItem('access_token');
            window.location.href = '/login'; 
        } catch (error) {
            console.error('Logout failed:', error.response?.data || error.message);
            alert('Logout failed. Please try again.');
        }
    });

    // fetchTask at start
    fetchTasks();
});