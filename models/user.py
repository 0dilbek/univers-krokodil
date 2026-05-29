from tortoise import Model, fields

class User(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField(unique=True)  # Telegram user ID
    full_name = fields.CharField(max_length=100, default="", null=True)
    is_bot = fields.BooleanField(default=False)
    mention = fields.TextField()
    def __str__(self):
        return self.full_name

class Transfers(Model):
    id = fields.BigIntField(pk=True)
    from_user = fields.ForeignKeyField("models.User", related_name="transfers_from")
    to_user = fields.ForeignKeyField("models.User", related_name="transfers_to")
    amount = fields.BigIntField()
    type = fields.CharField(max_length=50)  # "diamond", "dollar"
    caption = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

class Blocked_user(Model):
    user = fields.ForeignKeyField("models.User", related_name="blocked_users", on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)

class Profile(Model):
    user = fields.ForeignKeyField("models.User", related_name="profile", on_delete=fields.CASCADE, unique=True)
    dollar = fields.BigIntField(default=0)
    diamond = fields.BigIntField(default=0)
    himoya = fields.IntField(default=0)
    hujjat = fields.IntField(default=0)
    qotildan_himoya = fields.IntField(default=0)
    osishdan_himoya = fields.IntField(default=0)
    miltiq = fields.IntField(default=0)
    doridan_himoya = fields.IntField(default=0)
    maska = fields.IntField(default=0)
    wins = fields.BigIntField(default=0)
    slip_himoya = fields.IntField(default=0)
    geroy_himoya = fields.IntField(default=0)
    games_count = fields.BigIntField(default=0)
    on_himoya = fields.BooleanField(default=True)
    on_hujjat = fields.BooleanField(default=True)
    on_qotildan_himoya = fields.BooleanField(default=True)
    on_osishdan_himoya = fields.BooleanField(default=True)
    on_miltiq = fields.BooleanField(default=True)
    on_doridan_himoya = fields.BooleanField(default=True)
    on_maska = fields.BooleanField(default=True)
    on_slip_himoya = fields.BooleanField(default=True)
    on_geroy_himoya = fields.BooleanField(default=True)
