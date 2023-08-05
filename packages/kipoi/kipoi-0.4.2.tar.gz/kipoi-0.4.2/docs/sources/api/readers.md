<h1 id="kipoi.readers">kipoi.readers</h1>

Readers useful for creating new dataloaders

- HDF5Reader

<h2 id="kipoi.readers.HDF5Reader">HDF5Reader</h2>

```python
HDF5Reader(self, file_path)
```
Read the HDF5 file. Convenience wrapper around h5py.File

__Arguments__

- __file_path__: File path to an HDF5 file

<h3 id="kipoi.readers.HDF5Reader.ls">ls</h3>

```python
HDF5Reader.ls(self)
```
Recursively list the arrays

<h3 id="kipoi.readers.HDF5Reader.load_all">load_all</h3>

```python
HDF5Reader.load_all(self, unflatten=True)
```
Load the whole file

__Arguments__

- __unflatten__: if True, nest/unflatten the keys.
      e.g. an entry `f['/foo/bar']` would need to be accessed
- __using two nested `get` call__: `f['foo']['bar']`

<h3 id="kipoi.readers.HDF5Reader.batch_iter">batch_iter</h3>

```python
HDF5Reader.batch_iter(self, batch_size=16, **kwargs)
```
Create a batch iterator over the whole file

__Arguments__

- __batch_size__: batch size
- __**kwargs__: ignored argument. Used for consistency with other dataloaders

<h3 id="kipoi.readers.HDF5Reader.open">open</h3>

```python
HDF5Reader.open(self)
```
Open the file

<h3 id="kipoi.readers.HDF5Reader.close">close</h3>

```python
HDF5Reader.close(self)
```
Close the file

<h3 id="kipoi.readers.HDF5Reader.load">load</h3>

```python
HDF5Reader.load(file_path, unflatten=True)
```
Load the data all at once (classmethod).

__Arguments__

- __file_path__: HDF5 file path
- __unflatten__: see `load_all`

