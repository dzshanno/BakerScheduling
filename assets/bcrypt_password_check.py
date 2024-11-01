import bcrypt

passwords = {
    "admin_user": "admin_password",
    "trainer_user": "trainer_password",
    "trained_staff": "staff_password",
    "trainee_user": "trainee_password",
}

for user, password in passwords.items():
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    print(f"User: {user}, Hashed Password: {hashed.decode()}")


# User: admin_user, Hashed Password: $2b$12$Ni4mamfsbWetZKqgTcd0NOeHkcEQG4IdhFdfUIx/FiEuo1kpzFn16
# User: trainer_user, Hashed Password: $2b$12$NhOtqEqaq2ju9B7ukf2ZiOdy7TSfEBY3duTif7kWKkuEpwWiOmU1q
# User: trained_staff, Hashed Password: $2b$12$V.9Is0xKPfCVazkFFdOJb.LAbgHcRPo/ozwlfaq0Q6qZSz.LyWOVS
# User: trainee_user, Hashed Password: $2b$12$Jw518A5CnaDlYq3ajfSMDuFMoTDfVbFImQPZjeRPFziIH61pHMtyW
