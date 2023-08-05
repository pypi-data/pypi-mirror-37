# Django Stepped Queryset
This wrapper issues multiple queries to database when the input is too large to be accomodated in a single SQL(MSSQL has a restriction on the number of query parameters and MySQL has a limitation on the length of SQL). Multiple QuerySet are concatenated when evaluated.
