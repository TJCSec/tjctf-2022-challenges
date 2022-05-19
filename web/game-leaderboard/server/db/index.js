const db = require('better-sqlite3')('db/database.db')
const crypto = require('crypto')

db.exec('DROP TABLE IF EXISTS leaderboard; CREATE TABLE leaderboard (profile_id TEXT, name TEXT, score INT);')

const names = ['Super A. Austin', 'g_gamer', 'dn', 'redfrog']
const user = () => crypto.randomBytes(8).toString('hex')
const score = () => Math.round(Math.random() * 100)
const insert = db.prepare('INSERT INTO leaderboard (profile_id, name, score) VALUES (?, ?, ?)');
insert.run(user(), 'superandypancake', -32)
for (let name of names) {
    insert.run(user(), name, score())
}

module.exports = db;
