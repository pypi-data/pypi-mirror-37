# snark-cli
Run low-cost GPUs under single command line.

## Run
Install through pip

```
pip install snark
```

Register an account at https://lab.snark.ai and login through CLI

```
snark login
```

Start a pod
```
snark start
> python train_mnist.py
```

## More Commands for management
List all running pods
```
snark ls
```

Continue working on a pod by attaching to to it again.
```
snark attach POD_ID
```

To stop a pod
```
snark stop POD_ID
```


## Development

### install
pip install -e .

### run
to run commands, you have to run snark-controller
```
snark-local login --username sergiy
snark-local create pod --pod_name sergiy_pod_1 --docker_image doesnt/matter
```
