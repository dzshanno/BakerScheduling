-- SQL Script to Create and Populate Bakery Scheduler PostgreSQL Database

-- Create Roles Table
CREATE TABLE IF NOT EXISTS role (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

-- Create Users Table
CREATE TABLE IF NOT EXISTS "user" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role_id INTEGER REFERENCES role(role_id),
    date_joined TIMESTAMP DEFAULT current_timestamp
);

-- Create Shifts Table
CREATE TABLE IF NOT EXISTS shift (
    shift_id SERIAL PRIMARY KEY,
    shift_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    num_trainee_needed INTEGER DEFAULT 0,
    num_trained_needed INTEGER DEFAULT 0,
    num_trainer_needed INTEGER DEFAULT 0
);

-- Create Shift Assignments Table
CREATE TABLE IF NOT EXISTS shift_assignment (
    assignment_id SERIAL PRIMARY KEY,
    shift_id INTEGER REFERENCES shift(shift_id),
    user_id INTEGER REFERENCES "user"(user_id),
    role_id INTEGER REFERENCES role(role_id),
    status VARCHAR(50) NOT NULL
);

-- Insert Roles
INSERT INTO role (role_name) VALUES ('Admin') ON CONFLICT (role_name) DO NOTHING;
INSERT INTO role (role_name) VALUES ('Trainer') ON CONFLICT (role_name) DO NOTHING;
INSERT INTO role (role_name) VALUES ('Trained Staff') ON CONFLICT (role_name) DO NOTHING;
INSERT INTO role (role_name) VALUES ('Trainee') ON CONFLICT (role_name) DO NOTHING;


--test data
-- Insert Users
INSERT INTO "user" (username, email, password_hash, role_id, date_joined) VALUES 
('admin_user', 'admin@example.com', '$2b$12$Ni4mamfsbWetZKqgTcd0NOeHkcEQG4IdhFdfUIx/FiEuo1kpzFn16', 1, '2024-10-30 10:00:00') 
ON CONFLICT (username) DO NOTHING;
INSERT INTO "user" (username, email, password_hash, role_id, date_joined) VALUES 
('trainer_user', 'trainer@example.com', '$2b$12$NhOtqEqaq2ju9B7ukf2ZiOdy7TSfEBY3duTif7kWKkuEpwWiOmU1q', 2, '2024-10-30 11:00:00') 
ON CONFLICT (username) DO NOTHING;
INSERT INTO "user" (username, email, password_hash, role_id, date_joined) VALUES 
('trained_user', 'trained@example.com', '$2b$12$V.9Is0xKPfCVazkFFdOJb.LAbgHcRPo/ozwlfaq0Q6qZSz.LyWOVS', 3, '2024-10-30 12:00:00') 
ON CONFLICT (username) DO NOTHING;
INSERT INTO "user" (username, email, password_hash, role_id, date_joined) VALUES 
('trainee_user', 'trainee@example.com', '$2b$12$Jw518A5CnaDlYq3ajfSMDuFMoTDfVbFImQPZjeRPFziIH61pHMtyW', 4, '2024-10-30 13:00:00') 
ON CONFLICT (username) DO NOTHING;

-- Insert Shifts
INSERT INTO shift (shift_date, start_time, end_time, num_trainee_needed, num_trained_needed, num_trainer_needed) VALUES 
('2024-11-01', '08:00:00', '12:00:00', 1, 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO shift (shift_date, start_time, end_time, num_trainee_needed, num_trained_needed, num_trainer_needed) VALUES 
('2024-11-02', '13:00:00', '17:00:00', 2, 2, 1) ON CONFLICT DO NOTHING;
INSERT INTO shift (shift_date, start_time, end_time, num_trainee_needed, num_trained_needed, num_trainer_needed) VALUES 
('2024-11-03', '09:00:00', '14:00:00', 1, 2, 1) ON CONFLICT DO NOTHING;

-- Insert Shift Assignments
INSERT INTO shift_assignment (shift_id, user_id, role_id, status) VALUES (1, 2, 2, 'Assigned') ON CONFLICT DO NOTHING;
INSERT INTO shift_assignment (shift_id, user_id, role_id, status) VALUES (1, 3, 3, 'Assigned') ON CONFLICT DO NOTHING;
INSERT INTO shift_assignment (shift_id, user_id, role_id, status) VALUES (2, 4, 4, 'Available') ON CONFLICT DO NOTHING;
INSERT INTO shift_assignment (shift_id, user_id, role_id, status) VALUES (2, 2, 2, 'Assigned') ON CONFLICT DO NOTHING;
INSERT INTO shift_assignment (shift_id, user_id, role_id, status) VALUES (3, 3, 3, 'Available') ON CONFLICT DO NOTHING;
INSERT INTO shift_assignment (shift_id, user_id, role_id, status) VALUES (3, 1, 1, 'Confirmed') ON CONFLICT DO NOTHING;
INSERT INTO shift_assignment (shift_id, user_id, role_id, status) VALUES (3, 4, 4, 'No-show') ON CONFLICT DO NOTHING;
