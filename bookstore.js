// Step 2: switch to the bookstore database
// use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list authors and books
db.authors.find()
db.books.find()

// Step 6: insert two new books
db.books.insertMany([
  { title: "Persuasion", published_year: 1817, author_ids: ["author_001"] },
  { title: "The Hobbit", published_year: 1937, author_ids: ["author_004"] }
])

// Step 7: add missing authors
db.authors.insertOne({
  _id: "author_004",
  name: "J.R.R. Tolkien",
  nationality: "British",
  bio: {
    short: "English author and philologist.",
    long: "John Ronald Reuel Tolkien was an English writer and professor best known for The Hobbit and The Lord of the Rings."
  }
})

// Step 8: filter books by a list of authors
db.books.find({ author_ids: { $in: ["author_001", "author_004"] } })
