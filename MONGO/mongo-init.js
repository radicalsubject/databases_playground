// this user cant auth on admin db, but can on any other db (money_db)
// MONGO INIT user can auth on admin db and cant on money_db?

db.createUser(
    {
        user : "labaggregator-admin",
        pwd: "password",
        roles : [
            {
                "role" : "root",
                "db" : "admin"
            }
        ]
    }
);
