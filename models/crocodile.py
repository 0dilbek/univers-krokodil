from tortoise import fields, models


class CrocodileProfile(models.Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("models.User", related_name="crocodile_profile")
    rating = fields.IntField(default=1000)
    points = fields.IntField(default=0)
    games_count = fields.IntField(default=0)
    rounds_explained = fields.IntField(default=0)
    correct_answers = fields.IntField(default=0)
    wins = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "crocodile_profiles"


class CrocodileWord(models.Model):
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=255, unique=True)
    language = fields.CharField(max_length=8, default="uz")
    category = fields.CharField(max_length=64, null=True)
    difficulty = fields.CharField(max_length=16, default="medium")
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "crocodile_words"


class CrocodileChat(models.Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True, index=True)
    chat_type = fields.CharField(max_length=32)
    title = fields.CharField(max_length=255, null=True)
    username = fields.CharField(max_length=128, null=True)
    members_count = fields.IntField(null=True)
    invite_link = fields.CharField(max_length=512, null=True)
    is_active = fields.BooleanField(default=True)
    last_synced_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "crocodile_chats"


class CrocodileGame(models.Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(index=True)
    chat_type = fields.CharField(max_length=32)
    status = fields.CharField(max_length=16, default="waiting", index=True)
    category = fields.CharField(max_length=64, null=True)
    starter = fields.ForeignKeyField("models.User", related_name="started_crocodile_games")
    current_explainer = fields.ForeignKeyField(
        "models.User", related_name="explaining_crocodile_games", null=True
    )
    current_word = fields.ForeignKeyField("models.CrocodileWord", related_name="games", null=True)
    round_number = fields.IntField(default=0)
    message_id = fields.IntField(null=True)
    word_message_id = fields.IntField(null=True)
    round_started_at = fields.DatetimeField(null=True)
    claim_available_at = fields.DatetimeField(null=True)
    last_activity_at = fields.DatetimeField(null=True)
    last_correct_user = fields.ForeignKeyField(
        "models.User", related_name="last_correct_crocodile_games", null=True
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    finished_at = fields.DatetimeField(null=True)

    class Meta:
        table = "crocodile_games"


class CrocodileRound(models.Model):
    id = fields.IntField(pk=True)
    game = fields.ForeignKeyField("models.CrocodileGame", related_name="rounds")
    word = fields.ForeignKeyField("models.CrocodileWord", related_name="rounds")
    explainer = fields.ForeignKeyField("models.User", related_name="explained_crocodile_rounds")
    winner = fields.ForeignKeyField(
        "models.User", related_name="won_crocodile_rounds", null=True
    )
    round_number = fields.IntField()
    status = fields.CharField(max_length=16, default="active")
    started_at = fields.DatetimeField(auto_now_add=True)
    claim_available_at = fields.DatetimeField(null=True)
    finished_at = fields.DatetimeField(null=True)
    answer_message_id = fields.IntField(null=True)

    class Meta:
        table = "crocodile_rounds"


class CrocodileGuess(models.Model):
    id = fields.IntField(pk=True)
    round = fields.ForeignKeyField("models.CrocodileRound", related_name="guesses")
    user = fields.ForeignKeyField("models.User", related_name="crocodile_guesses")
    message_id = fields.IntField()
    text = fields.CharField(max_length=512)
    is_correct = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "crocodile_guesses"


class CrocodileScore(models.Model):
    id = fields.IntField(pk=True)
    game = fields.ForeignKeyField("models.CrocodileGame", related_name="scores")
    user = fields.ForeignKeyField("models.User", related_name="crocodile_scores")
    points = fields.IntField(default=0)
    correct_answers = fields.IntField(default=0)
    rounds_explained = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "crocodile_scores"
        unique_together = (("game", "user"),)
