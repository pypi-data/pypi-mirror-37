<h1 id="kipoi.writers">kipoi.writers</h1>

Writers used in `kipoi predict`

- TsvBatchWriter
- BedBatchWriter
- HDF5BatchWriter
- RegionWriter
- BedGraphWriter
- BigWigWriter

<h2 id="kipoi.writers.TsvBatchWriter">TsvBatchWriter</h2>

```python
TsvBatchWriter(self, file_path, nested_sep='/')
```
Tab-separated file writer

__Arguments__

- __file_path (str)__: File path of the output tsv file
- __nested_sep__: What separator to use for flattening the nested dictionary structure
    into a single key

<h3 id="kipoi.writers.TsvBatchWriter.batch_write">batch_write</h3>

```python
TsvBatchWriter.batch_write(self, batch)
```
Write a batch of data

__Arguments__

- __batch__: batch of data. Either a single `np.array` or a list/dict thereof.

<h2 id="kipoi.writers.BedBatchWriter">BedBatchWriter</h2>

```python
BedBatchWriter(self, file_path, metadata_schema, header=True)
```
Bed-file writer

__Arguments__

- __file_path (str)__: File path of the output tsv file
- __dataloader_schema__: Schema of the dataloader. Used to find the ranges object
- __nested_sep__: What separator to use for flattening the nested dictionary structure
    into a single key

<h3 id="kipoi.writers.BedBatchWriter.batch_write">batch_write</h3>

```python
BedBatchWriter.batch_write(self, batch)
```
Write a batch of data to bed file

__Arguments__

- __batch__: batch of data. Either a single `np.array` or a list/dict thereof.

<h2 id="kipoi.writers.HDF5BatchWriter">HDF5BatchWriter</h2>

```python
HDF5BatchWriter(self, file_path, chunk_size=10000, compression='gzip')
```
HDF5 file writer

__Arguments__

- __file_path (str)__: File path of the output tsv file
- __chunk_size (str)__: Chunk size for storing the files
- __nested_sep__: What separator to use for flattening the nested dictionary structure
    into a single key
- __compression (str)__: default compression to use for the hdf5 datasets.
- __see also__: <http://docs.h5py.org/en/latest/high/dataset.html#dataset-compression>

<h3 id="kipoi.writers.HDF5BatchWriter.batch_write">batch_write</h3>

```python
HDF5BatchWriter.batch_write(self, batch)
```
Write a batch of data to bed file

__Arguments__

- __batch__: batch of data. Either a single `np.array` or a list/dict thereof.

<h3 id="kipoi.writers.HDF5BatchWriter.close">close</h3>

```python
HDF5BatchWriter.close(self)
```
Close the file handle

<h3 id="kipoi.writers.HDF5BatchWriter.dump">dump</h3>

```python
HDF5BatchWriter.dump(file_path, batch)
```
In a single shot write the batch/data to a file and
close the file.

__Arguments__

- __file_path__: file path
- __batch__: batch of data. Either a single `np.array` or a list/dict thereof.

<h2 id="kipoi.writers.BedGraphWriter">BedGraphWriter</h2>

```python
BedGraphWriter(self, file_path)
```

__Arguments__

- __file_path (str)__: File path of the output bedgraph file

<h3 id="kipoi.writers.BedGraphWriter.region_write">region_write</h3>

```python
BedGraphWriter.region_write(self, region, data)
```
Write region to file.

__Arguments__

- __region__: Defines the region that will be written position by position. Example: `{"chr":"chr1", "start":0, "end":4}`.
- __data__: a 1D or 2D numpy array vector that has length "end" - "start". if 2D array is passed then
        `data.sum(axis=1)` is performed on it first.

<h3 id="kipoi.writers.BedGraphWriter.write_entry">write_entry</h3>

```python
BedGraphWriter.write_entry(self, chr, start, end, value)
```
Write region to file.

__Arguments__

- __region__: Defines the region that will be written position by position. Example: `{"chr":"chr1", "start":0, "end":4}`.
- __data__: a 1D or 2D numpy array vector that has length "end" - "start". if 2D array is passed then
        `data.sum(axis=1)` is performed on it first.

<h3 id="kipoi.writers.BedGraphWriter.close">close</h3>

```python
BedGraphWriter.close(self)
```
Close the file

<h2 id="kipoi.writers.BigWigWriter">BigWigWriter</h2>

```python
BigWigWriter(self, file_path)
```
BigWig entries have to be sorted so the generated values are cached in a bedgraph file.

__Arguments__

- __file_path (str)__: File path of the output tsv file

<h3 id="kipoi.writers.BigWigWriter.write_entry">write_entry</h3>

```python
BigWigWriter.write_entry(self, chr, start, end, value)
```
Write region to file.

__Arguments__

- __region__: Defines the region that will be written position by position. Example: `{"chr":"chr1", "start":0, "end":4}`.
- __data__: a 1D or 2D numpy array vector that has length "end" - "start". if 2D array is passed then
        `data.sum(axis=1)` is performed on it first.

<h3 id="kipoi.writers.BigWigWriter.close">close</h3>

```python
BigWigWriter.close(self)
```
Close the file

