#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament user=USER password=PASSWORD")


def deleteMatches():
    """Remove all the match records from the database."""

    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    DB.close()
    deleteresultsdisplay()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()
    deleteresultsdisplay()

def deleteresultsdisplay():
    """Remove all the resultsdisplay records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM resultsdisplay")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    sql = """SELECT count(player) AS num
             FROM resultsdisplay"""
    c.execute(sql)
    players = c.fetchone()[0]
    DB.close()
    return players

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    player = "INSERT INTO players (name) VALUES (%s) RETURNING id"
    resultsdisplay = """INSERT INTO resultsdisplay (player,name,score,matches)
                        VALUES (%s,%s,%s,%s)"""
    c.execute(player, (name,))
    playerid = c.fetchone()[0]
    c.execute(resultsdisplay, (playerid,name,0,0))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    players = """SELECT r.player, p.name, r.score, r.matches
                 FROM resultsdisplay AS r
                 INNER JOIN players AS p on p.id = r.player
                 ORDER BY r.score DESC,  r.matches DESC"""
    c.execute(players)
    ranks = []
    for row in c.fetchall():
        ranks.append(row)
    DB.close()
    return ranks

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
   Args:
     winner:  the id number of the player who won
     loser:  the id number of the player who lost
   """

    win_score =1
    lose_score =0

    DB = connect()
    c = DB.cursor()
    ins = "INSERT INTO matches (winner, loser) VALUES (%s,%s)"
    win = """UPDATE resultsdisplay
             SET score = score+%s, matches = matches+1 WHERE player = %s"""
    los = """UPDATE resultsdisplay
             SET score = score+%s, matches = matches+1 WHERE player = %s"""
    c.execute(ins, (winner, loser))
    c.execute(win, (win_score, winner))
    c.execute(los, (lose_score, loser))
    DB.commit()
    DB.close()
#code snippet from https://benjaminbrandt.com/relational-databases-final-project
def validPair(player1, player2):
    """Checks if two players have already played against each other

    Args:
        player1: the id number of first player to check
        player2: the id number of potentail paired player


    Return true if valid pair, false if not
    """
    DB = connect()
    c = DB.cursor()
    sql = """SELECT winner, loser
             FROM matches
             WHERE ((winner = %s AND loser = %s)
                    OR (winner = %s AND loser = %s))"""
    c.execute(sql, (player1, player2, player2, player1))
    matches = c.rowcount
    DB.close()
    if matches > 0:
        return False
    return True
#code snippet from https://benjaminbrandt.com/relational-databases-final-project
def checkPairs(ranks, id1, id2):
    """Checks if two players have already had a match against each other.
    If they have, recursively checks through the list until a valid match is
    found.

    Args:

        ranks: list of current ranks from swissPairings()
        id1: player needing a match
        id2: potential matched player

    Returns id of matched player or original match if none are found.
    """
    if id2 >= len(ranks):
        return id1 + 1
    elif validPair(ranks[id1][0], ranks[id2][0]):
        return id2
    else:
        return checkPairs(ranks, id1, (id2 + 1))
#code snippet from https://benjaminbrandt.com/relational-databases-final-project
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ranks = playerStandings()
    pairs = []

    numPlayers = countPlayers()


    while len(ranks) > 1:
        validMatch = checkPairs(ranks,0,1)
        player1 = ranks.pop(0)
        player2 = ranks.pop(validMatch - 1)
        pairs.append((player1[0],player1[1],player2[0],player2[1]))

    return pairs
