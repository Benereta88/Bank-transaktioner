# Bank-transaktioner
Hantera dataflöden via strukturerade applikationer och databaser, med testning, validering, migrationer, transaktioner med rollbacks, med workflow management.
# requirements.txt
 
# Core libraries
Pandas>=2.0.0 # För att läsa och manipulera CSV-data
sqlalchemy>=2.0.0 # ORM för databaskoppling
psycopg2-binary>=2.9 # PostgresSQL-drivrutin
 
# Data validation
Pydantic>=2.0 # Validering av transaktioner
 
# Workflow orchestration
Prefect>=2.10 # Automatisering av arbetsflöden
 
# Database migrations
alembic>=1.10           # Versionshantering av DB-schema
 
# Logging
loguru>=0.7.0           # Avancerad loggning
 
# Development tools
Jupyterlab>=4.0 # Notebook för analys och rapport
pytest>=7.0 # Enhetstester
 
# Optional: Data quality framework
great_expectations>=0.18  # Validera datakvalitet
 
