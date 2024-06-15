

from app.settings import settings
import pugsql

messages_queries = pugsql.module("db/queries/messages")
messages_connection = messages_queries.connect(settings.DATABASE_URL)

