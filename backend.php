<?php
header("Content-Type: application/json");

// Dummy user data (Replace this with a database if needed)
$users = [
    ["username" => "user1", "password" => "password123"],
    ["username" => "user2", "password" => "password456"]
];

// Handle incoming requests
$request = $_GET['action'] ?? '';

switch ($request) {
    case 'register':
        registerUser();
        break;
    case 'login':
        loginUser();
        break;
    case 'books':
        fetchBooks();
        break;
    default:
        echo json_encode(["error" => "Invalid request"]);
        break;
}

function registerUser() {
    $data = json_decode(file_get_contents("php://input"), true);
    if (empty($data['username']) || empty($data['password'])) {
        echo json_encode(["error" => "Username and password are required"]);
        return;
    }
    echo json_encode(["success" => "User registered (simulated)"]);
}

function loginUser() {
    global $users;
    $data = json_decode(file_get_contents("php://input"), true);
    foreach ($users as $user) {
        if ($user["username"] === $data["username"] && $user["password"] === $data["password"]) {
            echo json_encode(["success" => "Login successful"]);
            return;
        }
    }
    echo json_encode(["error" => "Invalid credentials"]);
}

function fetchBooks() {
    $books = file_get_contents("books.json"); // Reads books from JSON file
    echo $books;
}
?>
