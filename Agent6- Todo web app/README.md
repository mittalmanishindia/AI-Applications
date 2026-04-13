# Todo Web Application

A modern, responsive, and feature-rich todo list web application built with vanilla HTML, CSS, and JavaScript. This application helps you organize your tasks efficiently with a clean and intuitive user interface.

![Todo App](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Functionality](#functionality)
- [Local Storage](#local-storage)
- [Responsive Design](#responsive-design)
- [Browser Support](#browser-support)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Add Tasks**: Quickly add new tasks to your todo list
- **Mark Complete**: Check off tasks when completed with a simple checkbox
- **Delete Tasks**: Remove tasks you no longer need
- **Filter Tasks**: View all tasks, only active tasks, or only completed tasks
- **Task Counter**: See how many tasks are remaining at a glance
- **Clear Completed**: Remove all completed tasks with one click
- **Persistent Storage**: All tasks are saved to browser's localStorage
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Beautiful UI**: Modern gradient design with smooth animations
- **Input Validation**: Prevents empty tasks from being added
- **XSS Protection**: Sanitizes user input to prevent security vulnerabilities

## 🎯 Demo

Open `index.html` in your web browser to see the application in action. No server or build process required!

## 🛠️ Technologies Used

- **HTML5**: Semantic markup for structure
- **CSS3**: Modern styling with flexbox, gradients, and animations
- **JavaScript (ES6+)**: Vanilla JavaScript for functionality
- **localStorage API**: Client-side data persistence

## 📁 File Structure

```
Agent1- Todo web app/
│
├── index.html          # Main HTML file with app structure
├── styles.css          # All styling and responsive design
├── script.js           # JavaScript functionality and logic
└── README.md           # Project documentation (this file)
```

## 🚀 Installation

1. **Clone or Download** this repository to your local machine:
   ```bash
   git clone <repository-url>
   ```
   Or download as ZIP and extract.

2. **Navigate** to the project folder:
   ```bash
   cd "Agent1- Todo web app"
   ```

3. **Open** `index.html` in your preferred web browser:
   - Double-click the `index.html` file, or
   - Right-click and select "Open with" → your browser, or
   - Use a local development server (optional)

That's it! No dependencies, no build process, no installation required.

## 📖 Usage

### Adding a Task
1. Type your task in the input field
2. Click the "Add Task" button or press Enter
3. Your task appears at the top of the list

### Completing a Task
- Click the checkbox next to a task to mark it as complete
- Completed tasks show with a strikethrough style
- Click again to unmark as complete

### Deleting a Task
- Click the "Delete" button on any task to remove it permanently
- Deletion is immediate and cannot be undone

### Filtering Tasks
Use the filter buttons to view:
- **All**: Shows all tasks (default)
- **Active**: Shows only incomplete tasks
- **Completed**: Shows only completed tasks

### Clearing Completed Tasks
- Click "Clear Completed" at the bottom to remove all completed tasks
- A confirmation dialog will appear
- Button is disabled when there are no completed tasks

## ⚙️ Functionality

### Core Functions

#### `addTask()`
- Validates input is not empty
- Creates new task object with unique ID, text, completion status, and timestamp
- Adds task to the beginning of the list
- Saves to localStorage
- Updates the UI

#### `deleteTask(id)`
- Removes task with specified ID
- Updates localStorage
- Re-renders the task list

#### `toggleTask(id)`
- Toggles completion status of specified task
- Updates localStorage
- Re-renders with updated styling

#### `clearCompletedTasks()`
- Removes all completed tasks after confirmation
- Updates localStorage
- Re-renders the list

#### `renderTasks()`
- Displays filtered tasks based on current filter
- Shows appropriate empty state messages
- Escapes HTML to prevent XSS attacks

#### `updateTaskCount()`
- Calculates and displays number of active tasks
- Updates "Clear Completed" button state

### Data Structure

Each task object contains:
```javascript
{
    id: 1234567890,              // Unique timestamp-based ID
    text: "Task description",    // Task content
    completed: false,            // Completion status
    createdAt: "2025-11-26..."  // ISO timestamp
}
```

## 💾 Local Storage

The application uses the browser's `localStorage` to persist tasks:

- **Key**: `tasks`
- **Value**: JSON stringified array of task objects
- **Persistence**: Data remains until explicitly cleared or browser data is deleted
- **Capacity**: Typically 5-10MB depending on browser

### Storage Functions
- `loadTasks()`: Retrieves tasks from localStorage on page load
- `saveTasks()`: Saves current tasks array to localStorage after any change

## 📱 Responsive Design

The application is fully responsive with breakpoints for different screen sizes:

- **Desktop** (> 600px): Full layout with side-by-side controls
- **Mobile** (≤ 600px): 
  - Stacked input and button layout
  - Vertical footer layout
  - Optimized touch targets
  - Wrapped filter buttons

## 🌐 Browser Support

Compatible with all modern browsers:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Opera (latest)

**Requirements**:
- JavaScript enabled
- localStorage support (available in all modern browsers)

## 🔮 Future Enhancements

Potential features for future versions:

- [ ] Task editing capability
- [ ] Due dates and reminders
- [ ] Task categories/tags
- [ ] Priority levels
- [ ] Drag and drop reordering
- [ ] Search functionality
- [ ] Dark mode toggle
- [ ] Export tasks to JSON/CSV
- [ ] Sync across devices (cloud storage)
- [ ] Task notes/descriptions
- [ ] Subtasks support
- [ ] Keyboard shortcuts
- [ ] Undo/Redo functionality

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate comments.

## 📄 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software as per the license terms.

---

## 🎨 Design Details

### Color Scheme
- **Primary Gradient**: Purple (#667eea) to Dark Purple (#764ba2)
- **Background**: Gradient background for visual appeal
- **Task Items**: Light gray (#f9f9f9) with hover effects
- **Delete Button**: Red (#ff6b6b)

### Typography
- **Font Family**: Segoe UI, system fonts
- **Title**: 2.5rem (responsive to 2rem on mobile)
- **Body Text**: 16px for readability

### Animations
- **Slide In**: Tasks animate in when added
- **Hover Effects**: Smooth transitions on interactive elements
- **Button Press**: Active state feedback

## 🐛 Known Issues

None at this time. If you encounter any issues, please report them in the Issues section.

## 💡 Tips for Users

1. **Use Enter Key**: Quickly add tasks by pressing Enter after typing
2. **Keyboard Navigation**: Tab through controls for keyboard-only operation
3. **Mobile Friendly**: Works great on phones and tablets
4. **Privacy**: All data stays on your device - nothing is sent to any server
5. **Multiple Windows**: Open in multiple tabs/windows - data syncs via localStorage events

## 📧 Contact

For questions, suggestions, or feedback, please reach out or open an issue in the repository.

---

**Enjoy organizing your tasks! 📝✨**

*Last Updated: November 26, 2025*
