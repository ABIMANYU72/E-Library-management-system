document.addEventListener("DOMContentLoaded", function () {
    updateBorrowedList(); // Only borrowed books list updates on load
});

function searchBooks() {
    const query = document.getElementById("search").value.toLowerCase();
    
    fetch("backend.php?action=books")
        .then(res => res.json())
        .then(books => {
            localStorage.setItem("books", JSON.stringify(books)); // Cache books in localStorage
            displayBooks(books, query);
        })
        .catch(error => console.error("Error fetching books:", error));
}

function displayBooks(books, query) {
    const bookList = document.getElementById("book-list");
    bookList.innerHTML = "";

    books.forEach(book => {
        if (
            book.title.toLowerCase().includes(query) || 
            book.author.toLowerCase().includes(query) || 
            book.category.toLowerCase().includes(query)
        ) {
            const bookItem = document.createElement("div");
            bookItem.innerHTML = `<strong>${book.title}</strong> by ${book.author} 
                <button onclick="borrowBook('${book.title}')">Borrow</button>`;
            bookList.appendChild(bookItem);
        }
    });
}

function borrowBook(title) {
    let borrowedBooks = JSON.parse(localStorage.getItem("borrowedBooks")) || [];
    let borrowDates = JSON.parse(localStorage.getItem("borrowDates")) || {};

    if (borrowedBooks.length >= 3) {
        alert("You can only borrow up to 3 books at a time.");
        return;
    }

    if (!borrowedBooks.includes(title)) {
        borrowedBooks.push(title);
        borrowDates[title] = new Date().toISOString();
        localStorage.setItem("borrowedBooks", JSON.stringify(borrowedBooks));
        localStorage.setItem("borrowDates", JSON.stringify(borrowDates));
        updateBorrowedList();
    }
}

function updateBorrowedList() {
    const borrowedBooks = JSON.parse(localStorage.getItem("borrowedBooks")) || [];
    const borrowedList = document.getElementById("borrowed-books");
    borrowedList.innerHTML = "";

    borrowedBooks.forEach(book => {
        const listItem = document.createElement("li");
        listItem.innerHTML = `${book} <button onclick="returnBook('${book}')">Return</button>`;
        borrowedList.appendChild(listItem);
    });

    checkDueDates();
}

function returnBook(title) {
    let borrowedBooks = JSON.parse(localStorage.getItem("borrowedBooks")) || [];
    let borrowDates = JSON.parse(localStorage.getItem("borrowDates")) || {};

    borrowedBooks = borrowedBooks.filter(book => book !== title);
    delete borrowDates[title];

    localStorage.setItem("borrowedBooks", JSON.stringify(borrowedBooks));
    localStorage.setItem("borrowDates", JSON.stringify(borrowDates));
    updateBorrowedList();
}

function checkDueDates() {
    let borrowDates = JSON.parse(localStorage.getItem("borrowDates")) || {};
    let today = new Date();

    Object.keys(borrowDates).forEach(book => {
        let borrowDate = new Date(borrowDates[book]);
        if (!isNaN(borrowDate.getTime())) {
            let dueDate = new Date(borrowDate);
            dueDate.setDate(dueDate.getDate() + 14);
            let daysLeft = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));

            if (daysLeft === 3) {
                alert(`Reminder: "${book}" is due in 3 days!`);
            } else if (daysLeft < 0) {
                alert(`Overdue: "${book}" is overdue! Please return it.`);
            }
        }
    });
}

// User authentication functions
function loginUser(username, password) {
    fetch("backend.php?action=login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
        headers: { "Content-Type": "application/json" }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem("user", username);
            alert("Login successful!");
        } else {
            alert("Invalid username or password.");
        }
    })
    .catch(error => console.error("Login error:", error));
}

function logoutUser() {
    localStorage.removeItem("user");
    alert("Logged out successfully!");
}
