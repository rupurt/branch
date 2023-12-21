# Branch

A streaming toolkit with bottomless storage

- [x] Embedded
- [ ] Single node
- [ ] Clustered
- [x] HTTP API
- [ ] Web UI
- [ ] Kafka gateway
- [ ] S3
- [x] GCS
- [ ] Azure blob storage
- [ ] MinIO
- [ ] R2
- [x] Local
- [x] Python bindings
- [ ] Elixir bindings
- [ ] Zig bindings
- [ ] C bindings

## Usage

### CLI

```shell
> branch --help

 Usage: branch [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                        │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation. │
│ --help                        Show this message and exit.                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ init                                                                                                         │
│ produce                                                                                                        │
│ consume                                                                                                        │
│ topics                                                                                                         │
│ server                                                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Create your configuration file by following the prompts

```shell
> branch init
...
```

Create a topic

```shell
> branch topics create \
    --topic=my-topic.v1 \
    --partitions=3
```

Produce a new record every second

```shell
> watch -n 1 \
    'branch produce --topic=my-topic.v1 --partition=0 --message=\'{"hello": "cli!", "now": "$(date --iso-8601=ns)"}\''
...
```

Consume records produced to `my-topic.v1`

```shell
> branch consume --topic=my-topic.v1
...
```

### Python

```python
# my-branch.py
import branch
from datetime import datetime

msg = '{"hello": "python!", "now": datetime.now()}'
producer_record = branch.ProducerRecord(topic="my-topic.v1", value=msg)
branch.produce(producer_record)
branch.consume("my-topic.v1")
```

```shell
> python my-branch.py
...
```

## Single node

```shell
> branch server start --port=9000 --ui-port=8999
...
```

## Clustered

```shell
> branch server start --host=0.0.0.0 --port=9001 --name=my-branch-1
...
> branch server start --host=0.0.0.0 --port=9002 --name=my-branch-2
...
```

## HTTP

```shell
> curl -X POST -d '{...}' http://localhost:9000/api/v1/produce
...
```

```shell
> curl http://localhost:9000/api/v1/consume
...
```

## Web UI

```shell
> open http://localhost:8999
```

## Development

This repository manages the dev environment as a [Nix flake](https://nixos.wiki/wiki/Flakes)
and requires [Nix to be installed](https://github.com/DeterminateSystems/nix-installer)

```shell
nix develop -c $SHELL
```

```shell
make all
```

```shell
make deps.install
make deps.install/dev
```

```shell
make deps.freeze
make deps.freeze/dev
```

```shell
make deps/reqs
make deps/outdated
make deps/check
```

```shell
make run
make run/server
```

```shell
make format
make format/check
```

```shell
make typecheck
```

```shell
make lint
```

```shell
make test
make test/watch
```

```shell
make coverage
```

```shell
make build
make build/pyinstaller
make build/nuitka
```

```shell
make exec
```

```shell
make clean
```

```shell
make compose.build
make compose.up
```

```shell
make docker.build/deps
make docker.build/run
```

## License

`branch` is released under the [MIT license](./LICENSE)
