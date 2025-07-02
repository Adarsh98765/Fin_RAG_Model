# reset_db.py

from Model_1.db.models import Base
from Model_1.db.crud import engine  # make sure engine is imported correctly

print("📦 Dropping and recreating all tables...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("✅ Database reset complete.")
