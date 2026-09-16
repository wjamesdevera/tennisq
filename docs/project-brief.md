# Tennis Q — Project Brief

## Problem

Open Play Tennis hosts currently have to manually decide which players should play next and keep track of who has already played. This can make it difficult to create fair matchups and give players reasonable playing time without constantly managing the queue.

## Goal

Build a web application that helps Open Play Tennis hosts manage players and automatically determine the next matchup based on a simple, defined queue system.

## Target Users

**Primary User**

- Open Play Tennis Host

**Secondary User**

- Tennis Players participating in an Open Play event

The MVP is designed primarily around the host's workflow. Players do not need their own accounts.

## Core Features

- Event creation and management
- Player pool management
- Player queue
- Matchup generation
- Match completion / play tracking

## MVP Fairness Rule

For the MVP, players who have waited the longest since their previous match receive priority for the next matchup.

The system does not attempt to determine player skill or create advanced skill-based matchmaking.

## MVP User Flow

1. Host creates an Open Play event.
2. Host adds players to the event.
3. Host starts the Open Play session.
4. System generates the next matchup.
5. Host records the match as completed.
6. Players are returned to the queue based on the queue rules.
7. Host generates the next matchup.
8. The process continues throughout the event.

## Success Criteria

- [ ] Host can successfully create an event.
- [ ] Host can add and remove players.
- [ ] Host can start an Open Play session.
- [ ] System can generate the next matchup.
- [ ] Host can record a completed match.
- [ ] Completed matches update the queue.
- [ ] Host can continue generating matchups without manually deciding who plays next.

## Technology

**Frontend:** Next.js

**Backend:** FastAPI

**Database:** PostgreSQL

**Infrastructure / Hosting:** Vercel & Render

## Out of Scope

- Player statistics and analytics
- Multiple court management
- Tournament/bracket management
- Player rankings/ELO
- Advanced skill-based matchmaking
- Event registration/payment
- Notifications
- Player messaging/social features
- Mobile application

## What Am I Explicitly NOT Building?

- A mobile application — web only.
- A tournament management system.
- A tennis ranking or statistics platform.
- A social network for tennis players.
- An advanced AI matchmaking system.
- A system that determines player skill.
- Multi-court support in the MVP.

## MVP Definition

The MVP is complete when an Open Play host can run an entire session by creating an event, adding players, generating matchups, recording completed matches, and continuing the queue without manually deciding who should play next.
