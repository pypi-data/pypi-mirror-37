# Copyright 2015 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""add description for execution

Revision ID: 004
Revises: 003
Create Date: 2015-06-10 14:23:54.494596

"""

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'executions_v2',
        sa.Column('description', sa.String(length=255), nullable=True)
    )
