from .customer import Customer

class Admin(Customer):
    def __init__(self, id, name, username):
        super().__init__(id, name, username)
        self.role = "admin"
