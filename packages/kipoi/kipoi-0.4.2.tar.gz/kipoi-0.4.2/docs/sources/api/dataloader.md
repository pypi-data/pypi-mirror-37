<h1 id="kipoi.get_dataloader_descr">get_dataloader_descr</h1>

```python
get_dataloader_descr(dataloader, source='kipoi')
```
Get dataloder description

__Arguments__

- __datalaoder__: dataloader's relative path/name in the source. 2nd column in the `kipoi.list_dataloader() `pd.DataFrame`.
- __source__: Model source. 1st column in the `kipoi.list_models()` `pd.DataFrame`.

<h1 id="kipoi.get_dataloader_factory">get_dataloader_factory</h1>

```python
get_dataloader_factory(dataloader, source='kipoi')
```
Loads the dataloader

__Arguments__

- __dataloader (str)__: dataloader name
- __source (str)__: source name

__Returns__

- Instance of class inheriting from `kipoi.data.BaseDataLoader` (like `kipoi.data.Dataset`)
       decorated with additional attributes.

__Methods__

- __batch_iter(batch_size, num_workers, **kwargs)__
     - Arguments
         - **batch_size**: batch size
         - **num_workers**: Number of workers to use in parallel.
         - ****kwargs**: Other kwargs specific to each dataloader
     - Yields
         - `dict` with `"inputs"`, `"targets"` and `"metadata"`
- __batch_train_iter(cycle=True, **kwargs)__
     - Arguments
         - **cycle**: if True, cycle indefinitely
         - ****kwargs**: Kwargs passed to `batch_iter()` like `batch_size`
     - Yields
         - tuple of ("inputs", "targets") from the usual dict returned by `batch_iter()`
- __batch_predict_iter(**kwargs)__
     - Arguments
         - ****kwargs**: Kwargs passed to `batch_iter()` like `batch_size`
     - Yields
         - "inputs" field from the usual dict returned by `batch_iter()`
- __load_all(**kwargs)__ - load the whole dataset into memory
     - Arguments
         - ****kwargs**: Kwargs passed to `batch_iter()` like `batch_size`
     - Returns
         - `dict` with `"inputs"`, `"targets"` and `"metadata"`
- **init_example()** - instantiate the dataloader with example kwargs
- **print_args()** - print information about the required arguments

__Appended attributes__

- **type** (str): dataloader type (class name)
- **defined_as** (str): path and dataloader name
- **args** (list of kipoi.specs.DataLoaderArgument): datalaoder argument description
- **info** (kipoi.specs.Info): general information about the dataloader
- **schema** (kipoi.specs.DataloaderSchema): information about the input/output
        data modalities
- **dependencies** (kipoi.specs.Dependencies): class specifying the dependencies.
      (implements `install` method for running the installation)
- **name** (str): model name
- **source** (str): model source
- **source_dir** (str): local path to model source storage
- **postprocessing** (dict): dictionary of loaded plugin specifications
- **example_kwargs** (dict): kwargs for running the provided example

