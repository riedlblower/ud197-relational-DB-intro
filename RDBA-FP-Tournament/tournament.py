#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
#    c.execute("DROP TABLE IF EXISTS match_records CASCADE;")
    c.execute("TRUNCATE match_records CASCADE;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
#    c.execute("DROP TABLE IF EXISTS players CASCADE;")
    c.execute("TRUNCATE players CASCADE;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("select count(*) from players;")
    count = c.fetchone()     
    DB.close()
    return count[0]    # return the value rather than one-itemed array


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
# insert into players (name) values ('Michael Sexton');
    SQL = "insert into players (name) values (%s);"
    data = (name,)
    DB = connect()
    c = DB.cursor()
    c.execute(SQL,data)
    DB.commit()
    DB.close()
    return

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
    c.execute(" select players.id as id, players.name as name, sum(case when match_records.winner=players.id then 1 else 0 end) win , sum(case when match_records.loser=players.id or match_records.winner=players.id then 1 else 0 end) matches from players left join match_records on match_records.winner >= 0 group by players.id order by win desc;")
    count = c.fetchall()     
    DB.commit()
    DB.close()
    return count

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    SQL = "insert into match_records values (%s, %s);"
    data = (winner,loser)
    DB = connect()
    c = DB.cursor()
    c.execute(SQL,data)
    DB.commit()
    DB.close()
    return
 
 
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

    DB = connect()
    c = DB.cursor()
    c.execute(" select players.id as id, players.name as name from players left join match_records on players.id = match_records.winner  group by players.id order by count(match_records.winner) desc")
    standings = c.fetchall()
    DB.commit()
    DB.close()
    nextPairings = []
    for i in range (0, len(standings)-1, 2):  # have i increment by two each time
        onePairing = standings[i] + standings[i+1]     # merge two tuples into one tuple
        nextPairings.append(onePairing)
    return nextPairings 



