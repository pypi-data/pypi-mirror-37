# sensu_plugins_aws_subnet

## Setup

```sh
pip install sensu_plugins_aws_subnet
```

- perform a check

```sh
sensu-check-aws-subnet -w 20 -c 10 -r us-west-2
```

## Build Project

```sh
make build
make upload
```

## Todo

- add test suites