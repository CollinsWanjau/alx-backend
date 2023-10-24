# 0x00. Pagination

## Learning Objectives

- How to paginate a dataset with simple page and page_size parameters
- How to paginate a dataset with hypermedia metadata
- How to paginate in a deletion-resilient manner

## Tasks

### [0. Simple helper function](./0-simple_helper_function.py)

Write a function named `index_range` that takes two integer arguments `page` and `page_size`.

The function should return a tuple of size two containing a start index and an end index corresponding to the range of indexes to return in a list for those particular pagination parameters.

- Page numbers are 1-indexed, i.e. the first page is page 1.



# REST API Design: Filtering, Sorting, and Pagination

## Pagination

### Offset Pagination

- Pagination is a common technique used to limit the returned rows in a result set.It is the simplest form of paging.

- LIMIT/Offset became popular with apps using sql dbs which already have LIMIT and OFFSET as part of the SQL SELECT statement.

- Limit/Offset Paging would look like this `GET /items?limit=20&offset=100`.This query would return the 20 rows starting with the 100th row.

- The problem with this approach is that it is not very efficient. If you want to get the 1000th row, you have to first get the first 999 rows and discard them.

#### Benefits

- It is easy to implement.

- Stateless on server.

- Works regardless of custom sort_by parameters.

#### Drawbacks

- It is not very efficient. If you want to get the 1000th row, you have to first get the first 999 rows and discard them.

- Not consistent when new items are inserted to the table (i.e. Page drift)This is especially noticeable when we are ordering items by newest first.

    - Query `GET /items?offset=0&limit=15`
    - 10 new items are added to the table.
    - Query `GET /items?offset=15&limit=15` the second page will only return 5 new items, as adding 10 new items moved the offset by 10.To fix this, the client would really need to offset by 25 for the second query `GET /items?offset=25&limit=15`, but the client has no way of knowing that 10 new items were added.

### Keyset Pagination

- Keyset pagination uses the filter values of the last page to fetch the next set of items.Those columns would be indexed.

#### Example
(Assume the query is ordered  created date descending)

1. Client makes the requests for most recent items `GET /items?limit=20`
2. On next page, client finds the minimum created date of 2021-01-20T00:00:00 from previously returned and then makes second query using as a filter: `GET /items?limit=20&created_at<2021-01-20T00:00:00`
3. On next page, client finds the minimum created date of 2021-01-20T00:00:00 from previously returned results and then makes third query using as a filter: `GET /items?limit=20&created_at<2021-01-20T00:00:00`

```sql
SELECT * FROM items WHERE created_at < '2021-01-20T00:00:00' ORDER BY id LIMIT 20
```

#### Benefits

- It is efficient. It is always O(1) to get the next page.

- It is consistent when new items are inserted to the table.

- Works with existing filters without additional backend logic.

#### Drawbacks

- Tight coupling of paging mechanism to filter and sorting.Forces API users to add filters even if no filters are needed.

- Does not work for low cardinality fields such as enum strings.

- Complicated for API users when using custom sort_by fields as the client needs to adjust the filter based on the sort_by field.

### Seek Pagination

- Seek pagination is similar to keyset pagination.By adding an after_id or start_id URL parameter, we can remove the tight coupling of paging mechanism to filter and sorting.

- Since unique identifiers are naturally high cardinality, we won't run into issues unlike if sorting by a low cardinality field like state enums or category name.

#### Example
(Assume the query is ordered by created date descending)

1. Client makes the requests for most recent items `GET /items?limit=20`
2. On next page, client finds the last id of `20` from previously returned and then makes second query using as a filter: `GET /items?limit=20&after_id=20`
3. On next page, client finds the last id of `40` from previously returned results and then makes third query using as a filter: `GET /items?limit=20&after_id=40`

```sql
SELECT * FROM items WHERE id > 20 ORDER BY id LIMIT 20
```

- The above example works fine if ordering is done by id, but what if we want to sort by an email field?For each request, the backend needs to first obtain the email value for the item who's identifier matches the after_id parameter.Then, the second query is performed using that value as a `where` filter.

- Let's consider the query `GET /items?limit=20&after_id=20&sort_by=email`.The backend would need two queries.

- The first query could be O(1) lookup with hash tables though to get the email pivot value,This is fed into the second query to only retrieve items whose email is greater than the pivot value(after_value).

- We sort by both columns, email and id, to ensure we have a stable sort incase two emails are the same.
This is critical for lower cardinality fields like email.

```sql
SELECT email AS AFTER_EMAIL FROM Items WHERE Id = 20
```

```sql
SELECT * FROM items WHERE email > AFTER_EMAIL OR (email = AFTER_EMAIL AND id > 20) ORDER BY email, id LIMIT 20
```

#### Benefits

- No coupling of pagination logic to filter logic.

- Consistent ordering even when newer items are inserted into the table.Works well when sorting by most recent first.

- Consistent performance regardless of page number.

#### Drawbacks

- More complex for backend to implement relative to offset based or keyset pagination.

- If items are deleted from the db, the start_id may not be valid id.

### Sorting

- Like filtering, sorting is an important feature of a REST API that returns alot of data.If you're returning a list of users, your API users may want to sort by name, age, or created date.

- To enable sorting, we can add a sort_by query parameter to our API.

#### Examples

- `GET /users?sort_by=asc(email)` and `GET /users?sort_by=desc(email)` would sort by email ascending and descending respectively.

- `GET /users?sort_by=+email` and `GET /users?sort_by=-email` would sort by email ascending and descending respectively.

- `GET /users?sort_by=email.asc` and `GET /users?sort_by=email.desc` would sort by email ascending and descending respectively.

- `GET /users?sort_by=email&email&order_by=asc` and `GET /users?sort_by=email&order_by=desc`.
