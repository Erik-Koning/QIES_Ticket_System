#!/bin/sh
python3 frontEnd.py <<EOF
login
agent
logout
login
planner
create service
10000
19800101
aaa
create service
10001
19800101
aab
logout
login
planner
sell ticket
10000
2
change ticket
10000
10001
1
cancel ticket
10000
1
delete service
10000
aaa
logout

EOF

python3 backOffice.py <<EOF
