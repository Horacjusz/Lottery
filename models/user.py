# models/user.py

class User:
    def __init__(self, ID = None, name = "default_name", username = None, password = "None", choosable=True, spouse=None, assignment=None, wishlist=[], reserved_items=[]):
        if ID is None :
            from services.encryption_service import decrypt_data
            data = decrypt_data()
            ID = str(max(int(id) for id in data) + 1)
        if username is None :
            username = f"user_{ID}"
        self.ID = ID
        self.name = name
        self.username = username
        self.password = password
        self.choosable = choosable
        self.spouse = spouse
        self.assignment = assignment
        self.wishlist = wishlist
        self.reserved_items = reserved_items
        
    
    def __str__(self) -> str:
        return f"ID: {self.ID}, Name: {self.name}, Username: {self.username}, Password: {self.password}, Choosable: {self.choosable}, Spouse: {self.spouse}, Assignment: {self.assignment}\nWishlist: {self.wishlist}\nReserved Items: {self.reserved_items}"

    @classmethod
    def from_dict(cls, data):
        return cls(
            ID=data.get('id'),
            name=data.get('name'),
            username=data.get('username'),
            password=data.get('password'),
            choosable=data.get('choosable'),
            spouse=data.get('spouse'),
            assignment=data.get('assignment'),
            wishlist=data.get('wishlist'),
            reserved_items=data.get('reserved_items')
        )

    def edit_name(self, new_name):
        self.name = new_name

    def edit_username(self, new_username):
        self.username = new_username

    def edit_password(self, new_password):
        self.password = new_password

    def edit_choosable(self, choosable_status):
        self.choosable = choosable_status

    def edit_spouse(self, new_spouse):
        self.spouse = new_spouse

    def edit_wishlist(self, new_wishlist):
        self.wishlist = new_wishlist

    def edit_reserved_items(self, new_reserved_items):
        self.reserved_items = new_reserved_items

    def edit_assignment(self, new_assignment):
        self.assignment = new_assignment

    def to_dict(self):
        return {
            "id": self.ID,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "choosable": self.choosable,
            "spouse": self.spouse,
            "assignment": self.assignment,
            "wishlist": self.wishlist,
            "reserved_items": self.reserved_items
        }
