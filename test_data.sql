

    -- Test Data for the Bakery Scheduler Database

-- Insert Roles
INSERT INTO "role" (role_id, role_name) VALUES (1, 'Admin');
INSERT INTO "role" (role_id, role_name) VALUES (2, 'Trainer');
INSERT INTO "role" (role_id, role_name) VALUES (3, 'Trained Staff');
INSERT INTO "role" (role_id, role_name) VALUES (4, 'Trainee');

-- Insert Users
INSERT INTO "user" (user_id, username, email, password_hash, role_id, date_joined) VALUES (1, 'admin_user', 'admin@example.com', '$2b$12$eW5kS0f1MvFEXAmBfM9T5eHk2CNBy0CkyoS3eXZ7oUOOfN98rGFGK', 1, '2024-10-30 10:00:00');
INSERT INTO "user" (user_id, username, email, password_hash, role_id, date_joined) VALUES (2, 'trainer_user', 'trainer@example.com', '$2b$12$gEaJ8T3B5uH5V9VYciU1zOh63mlDt8/VZgWfH5V7p.JnN1E62tu2C', 2, '2024-10-30 11:00:00');
INSERT INTO "user" (user_id, username, email, password_hash, role_id, date_joined) VALUES (3, 'trained_user', 'trained@example.com', '$2b$12$UuH3nmPy6mMlDLyo.aHZ2ObvCeKv04cZNmS4hfr9BRbU5M0mIBN8a', 3, '2024-10-30 12:00:00');
INSERT INTO "user" (user_id, username, email, password_hash, role_id, date_joined) VALUES (4, 'trainee_user', 'trainee@example.com', '$2b$12$OqchXIhclbW.EFQ/JuhphuCF56XvGKg4xB9EDjGvLtX3MAQJkFe2O', 4, '2024-10-30 13:00:00');

-- Insert Shifts
INSERT INTO "shift" (shift_id, shift_date, start_time, end_time, num_trainee_needed, num_trained_needed, num_trainer_needed) VALUES (1, '2024-11-01', '08:00:00', '12:00:00', 1, 1, 1);
INSERT INTO "shift" (shift_id, shift_date, start_time, end_time, num_trainee_needed, num_trained_needed, num_trainer_needed) VALUES (2, '2024-11-02', '13:00:00', '17:00:00', 2, 2, 1);
INSERT INTO "shift" (shift_id, shift_date, start_time, end_time, num_trainee_needed, num_trained_needed, num_trainer_needed) VALUES (3, '2024-11-03', '09:00:00', '14:00:00', 1, 2, 1);

-- Insert Shift Assignments
INSERT INTO "shift_assignment" (assignment_id, shift_id, user_id, role_id) VALUES (1, 1, 2, 2);
INSERT INTO "shift_assignment" (assignment_id, shift_id, user_id, role_id) VALUES (2, 1, 3, 3);
INSERT INTO "shift_assignment" (assignment_id, shift_id, user_id, role_id) VALUES (3, 1, 4, 4);
INSERT INTO "shift_assignment" (assignment_id, shift_id, user_id, role_id) VALUES (4, 2, 2, 2);
INSERT INTO "shift_assignment" (assignment_id, shift_id, user_id, role_id) VALUES (5, 2, 3, 3);
INSERT INTO "shift_assignment" (assignment_id, shift_id, user_id, role_id) VALUES (6, 3, 1, 1);
INSERT INTO "shift_assignment" (assignment_id, shift_id, user_id, role_id) VALUES (7, 3, 4, 4);


-- Based on passwords being username_password e.g. admin_password

-- Update Users with Password Hashes
UPDATE "user" SET password_hash = '$2b$12$Ni4mamfsbWetZKqgTcd0NOeHkcEQG4IdhFdfUIx/FiEuo1kpzFn16' WHERE user_id = 1;
UPDATE "user" SET password_hash = '$2b$12$NhOtqEqaq2ju9B7ukf2ZiOdy7TSfEBY3duTif7kWKkuEpwWiOmU1q' WHERE user_id = 2;
UPDATE "user" SET password_hash = '$2b$12$V.9Is0xKPfCVazkFFdOJb.LAbgHcRPo/ozwlfaq0Q6qZSz.LyWOVS' WHERE user_id = 3;
UPDATE "user" SET password_hash = '$2b$12$Jw518A5CnaDlYq3ajfSMDuFMoTDfVbFImQPZjeRPFziIH61pHMtyW' WHERE user_id = 4;

