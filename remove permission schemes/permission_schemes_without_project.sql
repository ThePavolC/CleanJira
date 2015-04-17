SELECT
    *
FROM
    permissionscheme
WHERE
    id NOT IN (SELECT
            s.id
        FROM
            nodeassociation AS n,
            project AS p,
            permissionscheme AS s
        WHERE
            n.source_node_entity = 'Project'
                AND n.source_node_id = p.id
                AND n.sink_node_entity = 'PermissionScheme'
                AND n.sink_node_id = s.id);
