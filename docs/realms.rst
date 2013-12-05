======
Realms
======

All views in the same realm are considered the same in terms of rate limiting.
This allows you to rate-limit access to a collection of views as a while, such
as an API or registration process.

Each realm can have its own timeout, limit, respones code/message, and
whitelist.  If not specified for a realm, these will fall back to the defaults.


