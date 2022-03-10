# dockermc

by [Joe Zawisa](https://github.com/joezawisa)

## About

This project makes it easy to run a [Minecraft](https://www.minecraft.net)
server in a [Docker](https://www.docker.com) container. You'll need
[Docker](https://www.docker.com) installed, but that's it.

You can access your server at `localhost:25565`. The server's files will be in
the `data` directory.

## Starting the Server

Just run this command to start the server with
[Docker Compose](https://docs.docker.com/compose/).

```
docker compose up
```

To run the application in detached mode (in the background), use the `-d` flag.

```
docker compose up -d
```

## Stopping the Server

Once the application is running, you can stop it by pressing `Ctl`-`C`. You can
also stop it via the
[Docker Dashboard](https://docs.docker.com/desktop/dashboard/) or with
[Docker Compose](https://docs.docker.com/compose/).

```
docker compose stop
```

## Customization

You can choose which [Minecraft](https://www.minecraft.net) version to run by
passing the `-v` option to the command in [`compose`](compose.yml) like
this.

```yml
command: [
    "-v",
    "latest"
]
```

The defult is the latest release.

To specify a manifest file to use, include the `-m` option.

```yml
command: [
    "-m",
    "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
]
```