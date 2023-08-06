<h1 id="kipoi.get_model_descr">get_model_descr</h1>

```python
get_model_descr(model, source='kipoi')
```
Get model description

__Arguments__

- __model__: model's relative path/name in the source. 2nd column in the `kipoi.list_models() `pd.DataFrame`.
- __source__: Model source. 1st column in the `kipoi.list_models()` `pd.DataFrame`.

<h1 id="kipoi.get_model">get_model</h1>

```python
get_model(model, source='kipoi', with_dataloader=True)
```
Load the `model` from `source`, as well as the default dataloder to model.default_dataloder.

__Arguments__

- __model (str)__: model name
- __source (str)__:  source name
- __with_dataloader (bool)__: if True, the default dataloader is
    loaded to `model.default_dataloader` and the pipeline at `model.pipeline` enabled.

__Returns__

- Instance of class inheriting from `kipoi.models.BaseModel` (like `kipoi.models.KerasModel`)
   decorated with additional attributes.

__Methods__

- **predict_on_batch(x)**: Make model predictions given a batch of data `x`

__Appended attributes__

- **type** (`str`): model type (class name)
- **args** (`dict`): model args used to instantiate the model class
- **info** (`kipoi.specs.Info`): information about the author (etc)
- **schema** (`kipoi.specs.ModelSchema`): information about the input/outputdata modalities
- **dependencies** (`kipoi.specs.Dependencies`): class specifying the dependencies.
      (implements `install` method for running the installation)
- **default_dataloader** (class inheriting from `kipoi.data.BaseDataLoader`): default
       dataloader. None if `with_dataloader=False` was used.
- **name** (`str`): model name
- **source** (`str`): model source
- **source_dir** (`str`): local path to model source storage
- **postprocessing** (`dict`): dictionary of loaded plugin specifications
- **pipeline** (`kipoi.pipeline.Pipeline`): handle to a `Pipeline` object


