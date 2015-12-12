# P4 Conference Central
## Overview
This project is based on Conference Central project, which is a part of
"Developing Scalable Apps in Python". Source codes for Conference handling are
taken from the following repository.

https://github.com/udacity/ud858/tree/master/Lesson_5/00_Conference_Central

I implemented Session/Featured User functions on top of the above source codes.
You can find my implementation mainly below line#590 in conference.py. I also
made some changes in a few other files accordingly. Please refer to Contents
section for details of changes.

App ID is conference-center-1138.

When you perform your tests with these APIs, please note you will have to
 define Conference with your google account since the application checks if
 the given user is authorized to update conference and its sessions. You can't
 update any conference/session created by other users.

## Contents
* app.yaml - Added /tasks/set_featured_speaker.
* conference.py - Session/Featured User functions are added below line#590.
* index.yaml - Added indexes for Session. 
* main.py - SetFeaturedSpeakerHandler and /tasks/set_featured_speaker are added.
* models.py - Added Session/Featured Speaker related models. Modified Profile
model so it can have wishlist of sessions.
* Other files should be equivalent to source codes given by "Developing Scalable
 Apps in Python".

## Task 1 : Add Sessions to Conference.
Session has Conference as parent and it stores conferenceKey as a property.
Session key is produced from session name and the parent conference web safe
key. This should work since Session name should be unique under the conference.

Session has speaker as a StringProperty. I did not define Speaker model since
 having speaker as a session's StringProperty is sufficient for this project.
 
The following endpoints are implemented:
* getConferenceSessions(websafeConferenceKey) -- Given a conference, return all 
sessions
* getConferenceSessionsByType(websafeConferenceKey, typeOfSession) Given a 
conference, return all sessions of a specified type (eg lecture, keynote, workshop)
* getSessionsBySpeaker(speaker) -- Given a speaker, return all sessions 
given by this particular speaker, across all conferences
* createSession(SessionForm, websafeConferenceKey) -- open only to the organizer
 of the conference
* updateSession(SessionForm, websafeConferenceKey) -- open only to the organizer
 of the conference

## Task 2 : Add Sessions to User Wishlist
User's session wishlist is open to all conferences. To add a session to the
user's wishlist, SessionKey should be provided. SessionKey can be retrieved by
getConferenceSessions(websafeConferenceKey).

* addSessionToWishlist(SessionKey) -- adds the session to the user's wishlist.
* getSessionsInWishlist() -- query for all the sessions in the user's wishlist.
* deleteSessionInWishlist(SessionKey) -- removes the session from the user's wishlist.

## Task 3: Work on indexes and queries
The following two queries are added.
* getConferenceSessionsByDate(websafeConferenceKey, date) -- Return all sessions
of the conference for the specified date.
* getConferenceSessionsByHighlights(websafeConferenceKey, highlights) -- Return 
all sessions of the conference with the specified highlights. It returns exact
match of highlights. Wildcard search is not supported.

When you don't like workshops and don't like sessions after 7pm, the query 
requires two inequalities. GAE limits inequality to one. One solution for this
issue is that it performs the query with typeOfSession and gets the set of
non-workshop sessions. Then, it checks startTime against the set of non-workshop
 sessions and returns the set of sessions, which starts before 7pm. This is
 implemented as:
 
 * getConferenceSessionsExcludedByTypeTime(websafeConferenceKey, SessionTypeTimeForm)

## Task 4 : Add a Task
When a new session is added to a conference or the session is updated, it adds
a task to Task Queue. The task reaches /tasks/set_featured_speaker and kicks off
ConferenceApi._cacheFeaturedSpeaker. ConferenceApi._cacheFeaturedSpeaker checks
all session for the conference and updates the memcache with featured speakers.
In case no featured speaker is found, it deletes the memcache for the conference.

The following endpoint is implemented.
* getFeaturedSpeaker(websafeConferenceKey) - returns the set of FeaturedSpeakerForm for
the specified conference.


