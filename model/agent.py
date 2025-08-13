from tortoise import fields, models

class KnowledgeBaseEntry(models.Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='knowledge_entries', null=True)
    content = fields.TextField()
    title = fields.CharField(max_length=200)
    source = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.title