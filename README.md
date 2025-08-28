# Redis

This is a hack to get `redis` into a container using `pack` so it can be deployed on Toolforge.

It is slightly less terrible than the previous solution of dumping the pre-compiled binary onto NFS then executing it in a container.

Once T401075 / T363027 is resolved, this can be replaced.

## Logic
* `project.toml` handles installing the package from upstream
* `setup.py` creates a dummy python package which satisfies poetry
* `entrypoint.py` handles setting up the runtime (config)

## Testing locally
```
$ pack build --builder heroku/builder:24 external-redis
```

## Production configuration
Password for client access
```
$ toolforge envvars create REDIS_PASSWORD 'very secret'
```

Optional extra configuration keys:
```
$ toolforge envvars create REDIS_CONFIG '{""}'
```
