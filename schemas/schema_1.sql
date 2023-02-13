create table overall_rev
(
    yulu_revenue_order_date                      timestamp, -- date
    yulu_revenue_revenue                               float,       -- Number of reviews created
    yulu_revenue_total_items                                 int,       -- Number of changes merged
    yulu_revenue_AOV                                   float,       -- Number of changes abandoned
    primary key(yulu_revenue_order_date)
);