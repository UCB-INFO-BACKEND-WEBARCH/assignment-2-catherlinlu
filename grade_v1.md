# Assignment 2 Grading: lucatherlin

**Final Score: 78/100 (C+)**

## Summary
- Database Models: 17/20
- Task Endpoints: 16/30
- Category Endpoints: 12/15
- Background Tasks: 15/15
- Docker Compose: 18/20

## Detailed Results

### Database Models (17/20)

✅ **DB-01**: Task model has all required fields
   - Score: 8/8
   - All fields present: ['category_id', 'completed', 'created_at', 'description', 'due_date', 'id', 'title', 'updated_at']

✅ **DB-02**: Category model with unique name constraint
   - Score: 6/6
   - Correctly rejects duplicate category name (status 400)

❌ **DB-03**: Task-Category relationship (task belongs to category)
   - Score: 3/6
   - Deduction: Cannot GET task to verify relationship (-3 pts, major)

### Task Endpoints with Validation (16/30)

❌ **TASK-01**: GET /tasks returns list of all tasks
   - Score: 2/4
   - Deduction: Returns 500 instead of 200 (-2 pts, major)

❌ **TASK-02**: GET /tasks?completed=false filters by completion status
   - Score: 0/4
   - Deduction: Filter query parameter not supported (-4 pts, major)

❌ **TASK-03**: GET /tasks/:id returns single task with category info
   - Score: 0/3
   - Deduction: Returns 404 for existing task (-3 pts, major)

✅ **TASK-04**: GET /tasks/:id returns 404 when not found
   - Score: 2/2
   - Correctly returns 404

✅ **TASK-05**: POST /tasks creates task, returns 201
   - Score: 4/4
   - Creates task and returns 201 with task object

✅ **TASK-06**: POST /tasks validates input (title required, length limits)
   - Score: 4/4
   - Validation working: 4/4 tests passed

✅ **TASK-07**: Validation errors include structured messages
   - Score: 2/2
   - Structured error response: {"errors": {"title": ["Missing data for required field."]}}

❌ **TASK-08**: PUT /tasks/:id updates task, returns 200
   - Score: 0/3
   - Deduction: Returns 404 for PUT update (-3 pts, major)

✅ **TASK-09**: PUT /tasks/:id returns 404 when not found
   - Score: 1/1
   - Correctly returns 404

❌ **TASK-10**: DELETE /tasks/:id deletes task, returns 200 with message
   - Score: 0/2
   - Deduction: Returns 404 for DELETE (-2 pts, major)

✅ **TASK-11**: DELETE /tasks/:id returns 404 when not found
   - Score: 1/1
   - Correctly returns 404

### Category Endpoints (12/15)

✅ **CAT-01**: GET /categories returns categories with task_count
   - Score: 5/5
   - Returns 2 categories with task count

❌ **CAT-02**: GET /categories/:id returns category with its tasks
   - Score: 1/3
   - Deduction: Category not found (may not have been created) (-2 pts, major)

✅ **CAT-03**: POST /categories validates unique name and hex color
   - Score: 4/4
   - Category validation working: 4/4 tests passed

❌ **CAT-04**: DELETE /categories/:id prevents deletion with existing tasks
   - Score: 2/3
   - Returns 404 (partial credit)
   - Deduction: Unexpected status 404 for category delete with tasks (-1 pts, minor)

### Background Task Processing (15/15)

✅ **BG-01**: Redis and rq worker properly configured
   - Score: 4/4
   - Redis and worker services defined in docker-compose.yml

✅ **BG-02**: notification_queued: true when due_date within 24h
   - Score: 5/5
   - Refund +5 (manual review): POST handler correctly implements the 24h notification check and returns notification_queued in the response
   - Grader's own leniency rule (BG-04 passes → BG-02 full credit) would have applied automatically given the BG-04 refund

✅ **BG-03**: notification_queued: false when no due_date or > 24h
   - Score: 3/3
   - Correctly returns false for no due_date and distant due_date

✅ **BG-04**: Background job executes (worker logs show reminder)
   - Score: 3/3
   - Refund +2 (manual review): jobs.py correctly logs "Reminder: Task '{title}' is due soon!" per spec
   - Original auto-grader failure was downstream of BG-02 (no job queued for worker to process), not a worker-code defect

### Docker Compose (18/20)

✅ **DOCK-01**: docker-compose.yml defines all 4 services (app, db, redis, worker)
   - Score: 5/5
   - All 4 services defined: ['app', 'db', 'redis', 'worker']

❌ **DOCK-02**: docker-compose up --build runs without errors
   - Score: 6/8
   - docker-compose up --build succeeded, all containers running
   - Deduction: Docker config issue fixed for grading (broken YAML/missing entrypoint/missing compose) (-2 pts, minor)

✅ **DOCK-03**: All services connect properly (app to db+redis, worker to redis)
   - Score: 4/4
   - Connectivity verified through functional endpoint tests

✅ **DOCK-04**: API is accessible and functional on configured port
   - Score: 3/3
   - API accessible at http://127.0.0.1:5050 (port 5050)

## Strengths
- docker-compose.yml defines all 4 services (app, db, redis, worker)
- Redis and rq worker properly configured
- All services connect properly (app to db+redis, worker to redis)
- API is accessible and functional on configured port
- Task model has all required fields

## Areas for Improvement
- docker-compose up --build runs without errors: Docker config issue fixed for grading (broken YAML/missing entrypoint/missing compose)
- Task-Category relationship (task belongs to category): Cannot GET task to verify relationship
- GET /tasks returns list of all tasks: Returns 500 instead of 200
- GET /tasks?completed=false filters by completion status: Filter query parameter not supported
- GET /tasks/:id returns single task with category info: Returns 404 for existing task
- PUT /tasks/:id updates task, returns 200: Returns 404 for PUT update
- DELETE /tasks/:id deletes task, returns 200 with message: Returns 404 for DELETE
- GET /categories/:id returns category with its tasks: Category not found (may not have been created)
- DELETE /categories/:id prevents deletion with existing tasks: Unexpected status 404 for category delete with tasks
