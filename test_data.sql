-- Insert Roles
INSERT INTO "role" (role_id, role_name) VALUES (1, 'Admin');
INSERT INTO "role" (role_id, role_name) VALUES (2, 'Trainer');
INSERT INTO "role" (role_id, role_name) VALUES (3, 'Trained Staff');
INSERT INTO "role" (role_id, role_name) VALUES (4, 'Trainee');

-- Update Users with Password Hashes
UPDATE "user" SET password_hash = '$2b$12$Ni4mamfsbWetZKqgTcd0NOeHkcEQG4IdhFdfUIx/FiEuo1kpzFn16' WHERE user_id = 1;
UPDATE "user" SET password_hash = '$2b$12$NhOtqEqaq2ju9B7ukf2ZiOdy7TSfEBY3duTif7kWKkuEpwWiOmU1q' WHERE user_id = 2;
UPDATE "user" SET password_hash = '$2b$12$V.9Is0xKPfCVazkFFdOJb.LAbgHcRPo/ozwlfaq0Q6qZSz.LyWOVS' WHERE user_id = 3;
UPDATE "user" SET password_hash = '$2b$12$Jw518A5CnaDlYq3ajfSMDuFMoTDfVbFImQPZjeRPFziIH61pHMtyW' WHERE user_id = 4;

-- Insert Shifts
INSERT INTO "shift" (shift_id, shift_date, start_time, end_time, num_trainee_needed, num_trained_needed, num_trainer_needed) 
VALUES 
    (1, '2024-11-01', '08:00:00', '12:00:00', 1, 1, 1),
    (2, '2024-11-02', '13:00:00', '17:00:00', 2, 2, 1),
    (3, '2024-11-03', '09:00:00', '14:00:00', 1, 2, 1);

-- Insert Shift Assignments
INSERT INTO "shift_assignment" (assignment_id, shift_id, user_id, role_id) 
VALUES 
    (1, 1, 2, 2),
    (2, 1, 3, 3),
    (3, 1, 4, 4),
    (4, 2, 2, 2),
    (5, 2, 3, 3),
    (6, 3, 1, 1),
    (7, 3, 4, 4);