from tortoise import fields, models

class Conversation(models.Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='conversations')
    title = fields.CharField(max_length=200)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id} by {self.user.username}"

class Message(models.Model):
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    
    id = fields.UUIDField(pk=True)
    conversation = fields.ForeignKeyField('models.Conversation', related_name='messages')
    content = fields.TextField()
    role = fields.CharField(max_length=20, choices=[(ROLE_USER, "User"), (ROLE_ASSISTANT, "Assistant")])
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} in conversation {self.conversation.id}"
