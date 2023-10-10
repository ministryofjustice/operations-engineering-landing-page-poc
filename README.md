# Operations Engineering Landing Page PoC

This is a PoC repository to test out adding users to the operations-engineering tools.

1. [Prerequisites](#prerequisites)
1. [Development](#development)
1. [Deployment](#deployment)

## Prerequisites

To develop, deploy or run this app you will need to install:

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Docker](https://www.docker.com/)
- [Helm](https://helm.sh/) and [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) _(Optional, for deploying to Cloud Platform)_

## Development

### Run application within Terminal

To run the application locally from the Terminal.

```bash
make local
```

Open a browser to http://127.0.0.1:4567/home

### Linting

To run the linter, run the following command:

```bash
make lint
```

### Testing

To run the tests, run the following command:

```bash
make test
```

### Formatting

To run the formatter, run the following command:

```bash
make format
```

## Deployment

### Development environment

The Cloud Platform namespace for this project is called `operations-engineering-landing-page-poc`.

You can see the development app running at: https://operations-engineering-landing-page-poc.cloud-platform.service.justice.gov.uk/

and access Cloud Platform's namespace using:

```bash
kubectl get pods -n operations-engineering-landing-page-poc
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact Us

If you have any questions or need further clarification, feel free to ask in the #ask-operations-engineering channel on Slack or email us at operations-engineering@digital.justice.gov.uk.
