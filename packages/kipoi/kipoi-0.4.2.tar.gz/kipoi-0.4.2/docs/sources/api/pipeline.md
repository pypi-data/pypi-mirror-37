<h1 id="kipoi.pipeline.Pipeline">Pipeline</h1>

```python
Pipeline(self, model, dataloader_cls)
```
Runs model predictions from raw files:

```
raw files --(dataloader)--> data batches --(model)--> prediction
```

__Arguments__

- __model__: model returned by `kipoi.get_model`
- __dataloader_cls__: dataloader class returned by `kipoi.get_dataloader_factory`
        of `kipoi.get_model().default_dataloader`

<h2 id="kipoi.pipeline.Pipeline.predict_example">predict_example</h2>

```python
Pipeline.predict_example(self, batch_size=32, test_equal=False)
```
Run model prediction for the example file

__Arguments__

- __batch_size__: batch_size
- __test_equal__: currently not implemented
- __**kwargs__: Further arguments passed to batch_iter

<h2 id="kipoi.pipeline.Pipeline.predict">predict</h2>

```python
Pipeline.predict(self, dataloader_kwargs, batch_size=32, **kwargs)
```

__Arguments__

- __dataloader_kwargs__: Keyword arguments passed to the pre-processor
- __**kwargs__: Further arguments passed to batch_iter

__Returns__

`np.array, dict, list`: Predict the whole array

<h2 id="kipoi.pipeline.Pipeline.predict_generator">predict_generator</h2>

```python
Pipeline.predict_generator(self, dataloader_kwargs, batch_size=32, layer=None, **kwargs)
```
Prediction generator

__Arguments__

- __dataloader_kwargs__: Keyword arguments passed to the dataloader
- __batch_size__: Size of batches produced by the dataloader
- __layer__: If not None activation of specified layer will be returned. Only possible for models that are a
    subclass of `LayerActivationMixin`.
- __**kwargs__: Further arguments passed to batch_iter

__Yields__

- `dict`: model batch prediction

<h2 id="kipoi.pipeline.Pipeline.input_grad">input_grad</h2>

```python
Pipeline.input_grad(self, dataloader_kwargs, batch_size=32, filter_idx=None, avg_func=None, layer=None, final_layer=True, selected_fwd_node=None, pre_nonlinearity=False, **kwargs)
```
Get input gradients

__Arguments__

- __dataloader_kwargs__: Keyword arguments passed to the dataloader
- __batch_size__: Batch size used for the dataloader
- __filter_idx__: filter index of `layer` for which the gradient should be returned
- __avg_func__: String name of averaging function to be applied across filters in layer `layer`
- __layer__: layer from which backwards the gradient should be calculated
- __final_layer__: Use the final (classification) layer as `layer`
- __selected_fwd_node__: None - not supported by KerasModel at the moment
- __pre_nonlinearity__: Try to use the layer output prior to activation (will not always be possible in an
    automatic way)
- __**kwargs__: Further arguments passed to input_grad

__Returns__

`dict`: A dictionary of all model inputs and the gradients. Gradients are stored in key 'grads'

<h2 id="kipoi.pipeline.Pipeline.input_grad_generator">input_grad_generator</h2>

```python
Pipeline.input_grad_generator(self, dataloader_kwargs, batch_size=32, filter_idx=None, avg_func=None, layer=None, final_layer=True, selected_fwd_node=None, pre_nonlinearity=False, **kwargs)
```
Get input gradients

__Arguments__

- __dataloader_kwargs__: Keyword arguments passed to the dataloader
- __batch_size__: Batch size used for the dataloader
- __filter_idx__: filter index of `layer` for which the gradient should be returned
- __avg_func__: String name of averaging function to be applied across filters in layer `layer`
- __layer__: layer from which backwards the gradient should be calculated
- __final_layer__: Use the final (classification) layer as `layer`
- __selected_fwd_node__: None - not supported by KerasModel at the moment
- __pre_nonlinearity__: Try to use the layer output prior to activation (will not always be possible in an
    automatic way)
- __**kwargs__: Further arguments passed to input_grad

__Yields__

- `dict`: A dictionary of all model inputs and the gradients. Gradients are stored in key 'grads'

