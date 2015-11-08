#!/usr/bin/env python
"""
Test cases for tournament.py
"""

from tournament import *


def testDeleteMatches():
    """ test deleteMatches. """
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def test_delete_matches(tournament):
    """
    Test delete_matches().
    :param tournament: Tournament
    :return:
    """
    tournament.delete_matches()
    print "101. Old matches for the given tournament can be deleted."


def test_delete(tournament):
    """
    Test delete_players()
    :param tournament: Tournament.
    :return:
    """
    tournament.delete_matches()
    tournament.delete_players()
    print "102. Player records can be deleted."


def test_register(tournament):
    """
    Test register_player and participate.
    :param tournament: Tournament.
    :return:
    """
    tournament.delete_matches()
    tournament.delete_players()
    tournament.register_player("chandra.nalaar@gmail.com", "Chandra Nalaar")
    tournament.participate("chandra.nalaar@gmail.com")
    c = tournament.count_players()
    if c != 1:
        raise ValueError(
            "After one player registers, count_players() should be 1.")
    print "104. After registering a player, count_players() returns 1."


def test_count(tournament):
    """
    Test count_players before adding any player.
    :param tournament: Tournament.
    :return:
    """
    tournament.delete_matches()
    tournament.delete_players()
    c = tournament.count_players()
    if c == '0':
        raise TypeError(
            "count_players() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, count_players should return zero.")
    print "103. After deleting, count_players() returns zero."


def test_register_count_delete(tournament):
    """
    Test count_players after adding/deleting players.
    :param tournament: Tournament.
    :return:
    """
    tournament.delete_matches()
    tournament.delete_players()
    tournament.register_player("markov.chaney@gmail.com", "Markov Chaney")
    tournament.participate("markov.chaney@gmail.com")
    tournament.register_player("joe.malik@gmail.com", "Joe Malik")
    tournament.participate("joe.malik@gmail.com")
    tournament.register_player("mao.tsu-hsi@gmail.com", "Mao Tsu-hsi")
    tournament.participate("mao.tsu-hsi@gmail.com")
    tournament.register_player("atlanta.hope@gmail.com", "Atlanta Hope")
    tournament.participate("atlanta.hope@gmail.com")
    c = tournament.count_players()
    if c != 4:
        raise ValueError(
            "After registering four players, count_players should be 4.")
    tournament.delete_players()
    c = tournament.count_players()
    if c != 0:
        raise ValueError("After deleting, count_players should return zero.")
    print "105. Players can be registered and deleted."


def test_standings_before_matches(tournament):
    """
    Test player_standings() before reporting any match result.
    :param tournament: Tournament.
    :return:
    """
    tournament.delete_matches()
    tournament.delete_players()
    tournament.register_player("melpomene.murray@gmail.com", "Melpomene Murray")
    tournament.participate("melpomene.murray@gmail.com")
    tournament.register_player("randy.schwartz@gmail.com", "Randy Schwartz")
    tournament.participate("randy.schwartz@gmail.com")
    standings = tournament.player_standings()
    if len(standings) < 2:
        raise ValueError("Players should appear in standings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each player_standings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "106. Newly registered players appear in the standings with no matches."


def test_report_matches(tournament):
    """
    Test player_standings() after reporting match results.
    :param tournament: Tournament.
    :return:
    """
    tournament.delete_matches()
    tournament.delete_players()
    tournament.register_player("bruno.walton@gmail.com", "Bruno Walton")
    tournament.participate("bruno.walton@gmail.com")
    tournament.register_player("boots.oneal@gmail.com", "Boots O'Neal")
    tournament.participate("boots.oneal@gmail.com")
    tournament.register_player("cathy.burton@gmail.com", "Cathy Burton")
    tournament.participate("cathy.burton@gmail.com")
    tournament.register_player("diane.grant@gmail.com", "Diane Grant")
    tournament.participate("diane.grant@gmail.com")
    standings = tournament.player_standings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    tournament.report_match(id1, id2)
    tournament.report_match(id3, id4)
    standings = tournament.player_standings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "107. After a match, players have updated standings."


def test_pairing(tournament):
    """
    Test swiss_pairings().
    :param tournament: Tournament.
    :return:
    """
    tournament.delete_matches()
    tournament.delete_players()
    tournament.register_player("twilight.sparkle@gmail.com", "Twilight Sparkle")
    tournament.participate("twilight.sparkle@gmail.com")
    tournament.register_player("fluttershy@gmail.com", "Fluttershy")
    tournament.participate("fluttershy@gmail.com")
    tournament.register_player("applejack@gmail.com", "Applejack")
    tournament.participate("applejack@gmail.com")
    tournament.register_player("pinkie.pie@gmail.com", "Pinkie Pie")
    tournament.participate("pinkie.pie@gmail.com")
    standings = tournament.player_standings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    tournament.report_match(id1, id2)
    tournament.report_match(id3, id4)
    pairings = tournament.swiss_pairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swiss_pairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "108. After one match, players with one win are paired."


if __name__ == '__main__':
    print "Original tests start."
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Succeeded with the original test cases."
    print "==================================="
    print "Extra tests start with multiple tournaments scenario."
    conn = connect()
    tournament = Tournament(conn, "Full Stack Developer Cup")
    test_delete_matches(tournament)
    test_delete(tournament)
    test_count(tournament)
    test_register(tournament)
    test_register_count_delete(tournament)
    test_standings_before_matches(tournament)
    test_report_matches(tournament)
    test_pairing(tournament)
    tournament.close()
    print "Succeeded with extra test cases with multiple tournaments scenario."
    print "Success!  All tests pass!"
