<?php
header('Content-Type: application/json');

$dbPath = __DIR__ . DIRECTORY_SEPARATOR . 'tasks.sqlite';
$db = new SQLite3($dbPath);
$db->exec('CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  details TEXT NOT NULL DEFAULT "",
  completed INTEGER NOT NULL DEFAULT 0
)');

function read_json_body() {
  $raw = file_get_contents('php://input');
  return $raw ? json_decode($raw, true) : [];
}

function fail($status, $message) {
  http_response_code($status);
  echo json_encode(['error' => $message]);
  exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
  $rows = [];
  $result = $db->query('SELECT id, title, details, completed FROM tasks ORDER BY id DESC');
  while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $row['completed'] = (bool)$row['completed'];
    $rows[] = $row;
  }
  echo json_encode($rows);
  exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $payload = read_json_body();
  $title = trim((string)($payload['title'] ?? ''));
  $details = trim((string)($payload['details'] ?? ''));
  if ($title === '') fail(400, 'title is required');
  $stmt = $db->prepare('INSERT INTO tasks (title, details, completed) VALUES (:title, :details, 0)');
  $stmt->bindValue(':title', $title, SQLITE3_TEXT);
  $stmt->bindValue(':details', $details, SQLITE3_TEXT);
  $stmt->execute();
  http_response_code(201);
  echo json_encode([
    'id' => $db->lastInsertRowID(),
    'title' => $title,
    'details' => $details,
    'completed' => false
  ]);
  exit;
}

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
if ($id <= 0) fail(400, 'valid id is required');

if ($_SERVER['REQUEST_METHOD'] === 'PUT') {
  $payload = read_json_body();
  $title = trim((string)($payload['title'] ?? ''));
  $details = trim((string)($payload['details'] ?? ''));
  $completed = !empty($payload['completed']) ? 1 : 0;
  if ($title === '') fail(400, 'title is required');
  $stmt = $db->prepare('UPDATE tasks SET title = :title, details = :details, completed = :completed WHERE id = :id');
  $stmt->bindValue(':title', $title, SQLITE3_TEXT);
  $stmt->bindValue(':details', $details, SQLITE3_TEXT);
  $stmt->bindValue(':completed', $completed, SQLITE3_INTEGER);
  $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
  $stmt->execute();
  if ($db->changes() === 0) fail(404, 'task not found');
  echo json_encode([
    'id' => $id,
    'title' => $title,
    'details' => $details,
    'completed' => (bool)$completed
  ]);
  exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
  $stmt = $db->prepare('DELETE FROM tasks WHERE id = :id');
  $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
  $stmt->execute();
  if ($db->changes() === 0) fail(404, 'task not found');
  http_response_code(204);
  exit;
}

fail(405, 'method not allowed');
