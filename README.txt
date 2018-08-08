Change Log:

1. Fixed some minor bugs.
2. Added session for every customer through Bill_id.
3. Added col Bill_id in buys (int).
4. Altered buys table. Dropped ALL FK and PK.
5. Added S_no col in buys (primary key), auto_increment.
6. If a customer buys same product two times in same session it would not reflect in buys table (FIXED).
7. Changed navigation after error in entering cid in delete_cust().
