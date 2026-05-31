import { NextRequest, NextResponse } from 'next/server';
import { getDb, rowToTask } from '@/lib/db';

// GET /api/tasks — list all tasks
export async function GET() {
  try {
    const db = getDb();
    const rows = db.prepare('SELECT id, title, details, completed FROM tasks ORDER BY id DESC').all() as Array<{
      id: number;
      title: string;
      details: string;
      completed: number;
    }>;
    return NextResponse.json(rows.map(rowToTask));
  } catch (err) {
    return NextResponse.json({ error: 'Failed to fetch tasks' }, { status: 500 });
  }
}

// POST /api/tasks — create a new task
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const title = String(body.title || '').trim();
    const details = String(body.details || '').trim();

    if (!title) {
      return NextResponse.json({ error: 'title is required' }, { status: 400 });
    }
    if (title.length > 120) {
      return NextResponse.json({ error: 'title must be 120 characters or fewer' }, { status: 400 });
    }
    if (details.length > 500) {
      return NextResponse.json({ error: 'details must be 500 characters or fewer' }, { status: 400 });
    }

    const db = getDb();
    const stmt = db.prepare('INSERT INTO tasks (title, details, completed) VALUES (?, ?, 0)');
    const result = stmt.run(title, details);

    const row = db.prepare('SELECT id, title, details, completed FROM tasks WHERE id = ?').get(result.lastInsertRowid) as {
      id: number;
      title: string;
      details: string;
      completed: number;
    };

    return NextResponse.json(rowToTask(row), { status: 201 });
  } catch {
    return NextResponse.json({ error: 'Failed to create task' }, { status: 500 });
  }
}
