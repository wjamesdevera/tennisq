# Requirements & Scope

## MVP Features

### 1. Event Creation & Management

- Host can create an Open Play event.
- Host can provide a name for the event.
- Host can start an Open Play session.
- Host can view the current event and its active players.
- An event represents one Open Play session.

### 2. Player Pool Management

- Host can add a player to the event.
- Host can remove a player from the event.
- Host can modify a player's name.
- Host can view all players currently registered for the event.
- A player must have a name to be added to the event.

### 3. Player Queue

- System maintains a queue of players waiting to play.
- Players who have waited longer receive higher priority.
- Players who have just completed a match are placed back into the queue.
- Host can view the current queue order.
- Queue order updates after each completed match.
- The system prevents players who are currently playing from being selected for another match.

### 4. Match Generation

- Host can request the next matchup.
- System generates a matchup using the current queue.
- A generated matchup contains the required number of players for a match.
- Selected players are temporarily removed from the waiting queue while the match is active.
- Host can view the currently active matchup.

### 5. Match Completion & Play Tracking

- Host can mark an active match as completed.
- System records which players participated in the completed match.
- Completing a match updates each participating player's queue position.
- Completed matches are associated with the current event.
- Host can view the current match status.

## MVP User Flow

The primary workflow is:

**Create Event → Add Players → Start Session → Generate Match → Complete Match → Update Queue → Generate Next Match**

The host should be able to repeat this process throughout an Open Play session without manually deciding which players should play next.

## Out of Scope

The following are explicitly excluded from the MVP:

- Player accounts
- Player statistics
- Match analytics
- Player rankings / ELO
- Skill-based matchmaking
- Tournament brackets
- Multiple court management
- Payments or event registration
- Notifications
- Player messaging
- Mobile application
- Advanced scheduling

## MVP Constraints

- The MVP supports a single Open Play session at a time.
- The MVP is designed primarily for the event host.
- Players do not interact directly with the application.
- Queue priority is based on waiting time / previous play history rather than player skill.
- The system does not attempt to determine whether a matchup is competitively balanced.

## MVP Completion Criteria

The MVP is considered complete when a host can:

1. Create an Open Play event.
2. Add and manage players.
3. Start the session.
4. Generate a matchup.
5. Complete the matchup.
6. Have the system update the queue automatically.
7. Generate the next matchup.

The host should be able to run a complete Open Play session using the application without manually maintaining the player queue.
