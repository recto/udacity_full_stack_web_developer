#!/usr/bin/env python
"""
Tournament module
tournament.py -- implementation of a Swiss-system tournament
"""

import psycopg2


class Tournament(object):
    """ Data structure for the tournament """

    default = "__DEFAULT__"

    def __init__(self, conn, name):
        """
        Constructor of Tournament class.
        :param conn: The database connection.
        :param name: Name of tournament. If this is new, tournament will be
                     created.
        :return:
        """
        self.conn = conn
        self.cur = self.conn.cursor()
        self.t_id = None
        self.t_name = name
        self.__get_tournament(name)
        self.__create_player_standings()

    def close(self):
        """
        close cursor and connection.
        :return:
        """
        # self.cur.execute("drop view standings_%s;", (self.t_id, ))
        self.cur.close()
        self.conn.close()

    def __create_tournament(self, name):
        """
        Create a new tournament with the given name.
        :param name: Name of the new tournament.
        :return:
        """
        self.cur.execute("insert into tournaments (name) values(%s);",
                         (name,))
        self.cur.execute("commit;")

    def __create_player_standings(self):
        """
        Create player standings view of the tournament.
        :return:
        """
        self.cur.execute("create or replace view standings_%s as select \
                          participants.t_id, participants.p_id, sum(points) \
                          from participants left join matches on \
                          participants.p_id = matches.p_id where \
                          participants.t_id = %s group by participants.t_id, \
                          participants.p_id;", (self.t_id, self.t_id))

    def __get_tournament(self, name):
        """
        Get tournament ID for the given tournament.
        :param name: Tournament name.
        :return: Tuple of tournament ID and tournament name.
        """
        if self.t_id:
            pass
        else:
            self.cur.execute("select * from tournaments where name = %s;",
                             (name, ))
            if self.cur.rowcount <= 0:
                self.__create_tournament(name)
            self.cur.execute("select * from tournaments where name = %s;",
                             (name, ))
            row = self.cur.fetchone()
            self.t_id = row[0]
            self.t_name = row[1]
        return self.t_id, self.t_name

    def delete_matches(self):
        """
        Delete matches for the tournament.
        :return:
        """
        self.cur.execute("delete from matches where t_id = %s;",
                         (self.t_id, ))
        self.cur.execute("commit;")

    def delete_players(self):
        """
        Delete players from participants for the tournament. This does not
        remove players from the registered players of the system.
        :return:
        """
        self.cur.execute("delete from participants where t_id = %s;",
                         (self.t_id, ))
        self.cur.execute("commit;")


    def count_players(self):
        """
        Count players, who participate the tournament.
        :return: The number of participants of the tournament.
        """
        self.cur.execute("select count(p_id) from participants where \
                          t_id = %s;",
                         (self.t_id, ))
        return self.cur.fetchone()[0]

    def register_player(self, p_id, name):
        """
        Register a player with the given ID and name.
        :param p_id: Player ID like email address.
        :param name: Player's name.
        :return:
        """
        self.cur.execute("select * from players where id = %s;",
                         (p_id, ))
        if self.cur.rowcount <= 0:
            self.cur.execute("insert into players values (%s, %s);", (p_id, name))
            self.cur.execute("commit;")

    def unregister_player(self, p_id):
        """
        Unregister the player from the system.
        :param p_id: Player ID.
        :return:
        """
        self.cur.execute("delete players where p_id = %s;", (p_id, ))
        self.cur.execute("commit;")

    def participate(self, p_id):
        """
        Add a player to tournament.
        :param p_id: Player ID.
        :return:
        """
        self.cur.execute("insert into participants values (%s, %s);",
                         (self.t_id, p_id))
        self.cur.execute("commit;")

    def player_standings(self):
        """
        Check the current player standings.
        :return:
            A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
        """
        self.cur.execute("select standings.p_id, players.name, sum from \
                          standings_%s standings join players on standings.p_id\
                          = players.id where standings.t_id = %s order by sum \
                          desc;", (self.t_id, self.t_id))
        rows = self.cur.fetchall()
        standings = []
        for row in rows:
            self.cur.execute("select count(id) from matches where t_id = %s\
                              and p_id = %s group by id;", (self.t_id, row[0]))
            gp = self.cur.fetchone()
            if gp is None:
                standings.append((row[0], row[1], 0, 0))
            else:
                standings.append((row[0], row[1], row[2], gp[0]))
        return standings

    def report_match(self, winner, loser):
        """
        Report the match result.
        :param winner: Player ID of the user.
        :param loser: Player ID of the loser.
        :return:
        """
        self.cur.execute("select max(id) from matches;")
        row = self.cur.fetchone()
        match = 1
        if not (row[0] is None):
            match = row[0] + 1

        self.cur.execute("insert into matches values (%s, %s, %s, %s);",
                         (match, self.t_id, winner, 1))
        self.cur.execute("insert into matches values (%s, %s, %s, %s);",
                         (match, self.t_id, loser, 0))
        self.cur.execute("commit;")

    def swiss_pairings(self):
        """
        Pairings for the next round.
        :return:
          A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
        """
        standings = self.player_standings()
        parings = []
        p1 = None
        i = 0

        for player in standings:
            if i % 2 == 1:
                parings.append((p1[0], p1[1], player[0], player[1]))
            elif i == len(standings):
                parings.append((player[0], player[1]))
            else:
                p1 = player

            i += 1

        return parings


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    tournament = Tournament(conn, Tournament.default)
    tournament.delete_matches()
    tournament.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    tournament = Tournament(conn, Tournament.default)
    tournament.delete_players()
    tournament.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    tournament = Tournament(conn, Tournament.default)
    count = tournament.count_players()
    tournament.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    tournament = Tournament(conn, Tournament.default)
    p_id = name.lower().replace(" ", "_") + "@udacity.com"
    tournament.register_player(p_id , name)
    tournament.participate(p_id)
    tournament.close()


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
    conn = connect()
    tournament = Tournament(conn, Tournament.default)
    standings = tournament.player_standings()
    tournament.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    tournament = Tournament(conn, Tournament.default)
    tournament.report_match(winner, loser)


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
    conn = connect()
    tournament = Tournament(conn, Tournament.default)
    return tournament.swiss_pairings()
