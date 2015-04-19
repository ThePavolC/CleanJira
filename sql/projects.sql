SELECT
    p.id,
    p.pkey AS 'Project Key',
    p.pname AS 'Project Name',
    MAX(i.updated) AS 'Latest activity',
    COUNT(*) AS 'Number of Issues'
FROM
    jiraissue AS i,
    project AS p
WHERE
    i.project = p.id
GROUP BY p.id
HAVING MAX(i.updated) < '2013-01-01 00:00:00'
ORDER BY MAX(i.updated);
