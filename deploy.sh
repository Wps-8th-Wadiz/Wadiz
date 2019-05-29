#!/usr/bin/env bash
# .secrets와 staging area에 추가
git add -f .secrets
git add -f ./front/fds10-wadiz


# eb deploy실행
eb deploy --profile fc-8th-eb --staged

eb ssh && cat /var/log/eb-activity.log

# .secrets 를 제거
git reset HEAD .secrets
git reset HEAD ./front/fds10-wadiz

git reset
