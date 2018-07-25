# Frontend documentation

The web client is implemented as a SPA with vue.

## Holding data

We are using the single source of truth design pattern to maintain all
application status.

Notes:
- I thing its better to handle api calls on each component in order to
exclude meta values (such as loading states) from the actual
state and ease the overcomplicated schema of asynch vuex actions. Using
this aproach an action (or mutation) will be called to modified the
state when the asynchronous operations are performed elsewhere.