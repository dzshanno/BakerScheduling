CREATE TABLE Roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name VARCHAR(50) NOT NULL
);

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    role_id INTEGER,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

CREATE TABLE Shifts (
    shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    num_trainee_needed INTEGER DEFAULT 0,
    num_trained_needed INTEGER DEFAULT 0,
    num_trainer_needed INTEGER DEFAULT 0
);

CREATE TABLE ShiftAssignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_id INTEGER,
    user_id INTEGER,
    role_id INTEGER,
    FOREIGN KEY (shift_id) REFERENCES Shifts(shift_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);
