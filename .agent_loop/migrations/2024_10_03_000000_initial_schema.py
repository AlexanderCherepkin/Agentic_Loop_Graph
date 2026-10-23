"""Initial schema - Create all core tables for Agentic Loop."""

from alembic import op
import sqlalchemy as sa


def upgrade():
    """Create database schema for Agentic Loop system."""
    
    # Core Agents Table
    op.create_table(
        'agents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False, comment='Agent identifier'),
        sa.Column('type', sa.String(100), nullable=False, comment='e.g., orchestrator, researcher, coder, analyzer'),
        sa.Column('description', sa.Text(), nullable=True, comment='Detailed capabilities and purpose'),
        sa.Column('spec_version', sa.Integer(), nullable=False, default=1, comment='Agent specification version'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('config_hash', sa.String(64), nullable=True, comment='Hash of agent config for change detection'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )
    
    # Tasks Table - Queue of work items
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agent_id', sa.Integer(), sa.ForeignKey('agents.id'), nullable=True, comment='Owner agent'),
        sa.Column('title', sa.String(500), nullable=False, comment='Task title'),
        sa.Column('description', sa.Text(), nullable=True, comment='Full task description and context'),
        sa.Column('status', sa.String(50), nullable=False, default='pending', comment='e.g., pending, running, completed, failed'),
        sa.Column('priority', sa.Integer(), nullable=False, default=1, comment='Priority level 1-10'),
        sa.Column('metadata', sa.JSON(), nullable=True, comment='Additional metadata as JSON'),
        sa.Column('parent_task_id', sa.Integer(), sa.ForeignKey('tasks.id'), nullable=True, comment='Parent task in hierarchy'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    
    # Task Runs Table - Execution history for each task
    op.create_table(
        'task_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('tasks.id'), nullable=True, comment='Associated task'),
        sa.Column('agent_name', sa.String(255), nullable=True, comment='Agent that executed this run'),
        sa.Column('status', sa.String(50), nullable=False, default='running', comment='e.g., running, completed, failed, timeout'),
        sa.Column('progress', sa.Float(), nullable=True, comment='Completion percentage 0-100'),
        sa.Column('output', sa.Text(), nullable=True, comment='Final output or result'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='Error details if failed'),
        sa.Column('input_data', sa.JSON(), nullable=True, comment='Input data passed to agent'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    
    # Memories Table - Persistent agent knowledge and context
    op.create_table(
        'memories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agent_id', sa.Integer(), sa.ForeignKey('agents.id'), nullable=True, comment='Owner agent'),
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('tasks.id'), nullable=True, comment='Related task'),
        sa.Column('content', sa.Text(), nullable=False, comment='Memory content'),
        sa.Column('type', sa.String(50), nullable=False, default='context', comment='e.g., context, fact, preference'),
        sa.Column('metadata', sa.JSON(), nullable=True, comment='Additional metadata as JSON'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )

    
def downgrade():
    """Drop database schema."""
    op.drop_table('memories')
    op.drop_table('task_runs')
    op.drop_table('tasks')
    op.drop_table('agents')