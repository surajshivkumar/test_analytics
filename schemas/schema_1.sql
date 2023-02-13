create table overall_rev
(
    order_date                      timestamp, -- date
    revenue                               float,       -- Number of reviews created
    items                                 int,       -- Number of changes merged
    AOV                                   float,       -- Number of changes abandoned
    primary key(order_date)
);