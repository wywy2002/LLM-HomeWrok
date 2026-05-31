import { NextRequest, NextResponse } from 'next/server';
import { getDb, rowToTask } from '@/lib/db';

// PUT /api/tasks/:id — update a task
export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const id = parseInt(params.id, 10);
    if (isNaN(id)) {
      return NextResponse.json({ error: 'invalid task id' }, { status: 400 });
    }

    const body = await request.json();
    const title = String(body.title || '').trim();
    const details = String(body.details || '').trim();
    const completed = body.completed ? 1 : 0;

    if (!title) {
      return NextResponse.json({ error: 'title is required' }, { status: 400 });
    }

    const db = getDb();
    const stmt = db.prepare('UPDATE tasks SET title = ?, details = ?, completed = ? WHERE id = ?');
    const result = stmt.run(title, details, completed, id);

    if (result.changes === 0) {
      return NextResponse.json({ error: 'task not found' }, { status: 404 });
    }

    const row = db.prepare('SELECT id, title, details, completed FROM tasks WHERE id = ?').get(id) as {
      id: number;
      title: string;
      details: string;
      completed: number;
    };

    return NextResponse.json(rowToTask(row));
  } catch {
    return NextResponse.json({ error: 'Failed to update task' }, { status: 500 });
  }
}

// DELETE /api/tasks/:id — delete a task
export async function DELETE(_request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const id = parseInt(params.id, 10);
    if (isNaN(id)) {
      return NextResponse.json({ error: 'invalid task id' }, { status: 400 });
    }

    const db = getDb();
    const stmt = db.prepare('DELETE FROM tasks WHERE id = ?');
    const result = stmt.run(id);

    if (result.changes === 0) {
      return NextResponse.json({ error: 'task not found' }, { status: 404 });
    }

    return new NextResponse(null, { status: 204 });
  } catch {
    return NextResponse.json({ error: 'Failed to delete task' }, { status: 500 });
  }
}
