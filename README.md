# Booking-Scheduler

## How to use API

### Update the data

1. Create a JSON data like this (all the fields are required)

```
{
	"slotKey" : "-M143wUQcjYMlVStmasasD",
	"bookingKey" : "-M143wUQcjYMlVStmSwSSS",
	"date" : "2020-06-20T00:00:00+05:00",
	"duration" : 1,
	"end" : "8am",
	"location" : "Orchid Country Club",
	"name" : "Ali",
	"pitch" : 2,
	"rate" : 95,
	"start" : "8am",
	"status" : "Paid",
	"sumittedDate" : "2020-02-27T13:17:09+08:00"
}
```
2. Then send a PUT requiest to this url <server-url>/booking/<id>/ with the above data in the body.
3. Please note that the values of <id> will be ones that I'm returning from my system.
  
### Delete the data

1. Create a JSON structure like this
```
{
	"booking_id" : "-M143wUQcjYMlVStmasasD",
	"submittedDate" : "2020-02-27T13:17:09+08:00"
}
```
2. Then send a delete request to this url <server-url>/booking/<id>/ with the above in the body.
3. Same as update. Please remember that the value of <id> will be the one that I'm returning from my system.
