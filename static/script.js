// Fetch and display tasks when the page loads
document.addEventListener('DOMContentLoaded', function () {
    fetchTasks();
});

function fetchTasks() {
    fetch('/tasks')
        .then(response => response.json())
        .then(tasks => {
            const taskList = document.getElementById('taskList');
            taskList.innerHTML = ''; // Clear the list before adding new tasks
            tasks.forEach(task => {
                const taskItem = document.createElement('li');
                taskItem.textContent = task.title;
                if (task.completed) {
                    taskItem.classList.add('completed');
                }

                // Delete button
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.onclick = () => deleteTask(task.id);
                taskItem.appendChild(deleteButton);

                // Complete button
                if (!task.completed) {
                    const completeButton = document.createElement('button');
                    completeButton.textContent = 'Complete';
                    completeButton.onclick = () => completeTask(task.id);
                    taskItem.appendChild(completeButton);
                }

                taskList.appendChild(taskItem);
            });
        });
}

function addTask() {
    const taskInput = document.getElementById('taskInput');
    const title = taskInput.value.trim();
    if (title === '') {
        alert('Task title cannot be empty');
        return;
    }

    fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: title, completed: false })
    })
    .then(response => response.json())
    .then(task => {
        fetchTasks(); // Refresh the task list
        taskInput.value = ''; // Clear the input
    });
}

function deleteTask(taskId) {
    fetch(`/tasks/${taskId}`, {
        method: 'DELETE'
    })
    .then(() => {
        fetchTasks(); // Refresh the task list
    });
}

function completeTask(taskId) {
    fetch(`/tasks/${taskId}/complete`, {
        method: 'PATCH'
    })
    .then(() => {
        fetchTasks(); // Refresh the task list
    });
}
